package com.threefour.ott.worker;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.locks.Lock;

import com.threefour.Constants;
import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.ott.data.RouteTable;
import com.threefour.overlay.Neighbours;
import com.threefour.util.Print;

public class Listener implements Runnable {

    protected DatagramSocket socket;

    protected Neighbours neighbours;

    protected RouteTable routeTable = null;

    public Listener(DatagramSocket socket, Neighbours neighbours) {
        this.socket = socket;
        this.neighbours = neighbours;
    }

    // --------------------
    // Message dispatch
    // --------------------

    /**
     * Send a message to a specified address.
     * 
     * @param address Address of the destination.
     * @param message Message to be sent.
     * @throws IOException
     */
    protected void sendMessage(InetAddress address, Message message) throws IOException {
        var buf = message.to_bytes();
        var packet = new DatagramPacket(buf, buf.length, address, Constants.PORT);
        socket.send(packet);
    }

    /**
     * Floods a message to all available neighbours (except parent).
     * 
     * @param message Message to be flooded.
     * @throws IOException
     */
    protected void floodMessage(Message message) throws IOException {
        var buf = message.to_bytes();
        var packet = new DatagramPacket(buf, buf.length);
        packet.setPort(Constants.PORT);

        this.neighbours.readLock.lock();
        try {
            neighbours.getActiveAddresses()
                    .stream()
                    .filter(addr -> !(this.routeTable != null
                            && this.routeTable.parent.equals(neighbours.getName(addr))))
                    .forEach(addr -> {
                        packet.setAddress(addr);
                        try {
                            socket.send(packet);
                        } catch (IOException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        }
                    });
        } finally {
            this.neighbours.readLock.unlock();
        }
    }

    // --------------------
    // Message processing
    // --------------------

    /**
     * Processes an heartbeat message.
     * 
     * @param address Address of the sender.
     */
    protected void heartbeat(InetAddress address) {
        this.neighbours.writeLock.lock();
        try {
            // TODO remove old commented code
            // neighbours.put(address, new Pair<>(true, System.currentTimeMillis()));
            neighbours.updateTimestamp(neighbours.getName(address), System.currentTimeMillis());
        } finally {
            this.neighbours.writeLock.unlock();
        }
        // Print.printInfo("Received a heartbeat from " + address);
    }

    /**
     * Processes a server announcement message.
     * 
     * @param address      Address of the sender (parent node).
     * @param announcement Announcement message.
     */
    protected void announcement(InetAddress address, Announcement announcement) {

        // if the announcement comes directly from the server, its address
        // needs to be instantiated (because it starts at null, since the
        // server doesn't put its own address in the announcement)
        if (announcement.distance() == 0) {
            announcement = new Announcement((byte) 0, address);
        }

        Print.printInfo(address + ": " + announcement);

        // if this is the first announcement
        if (this.routeTable == null) {
            // create a new routing table with `address` as parent
            var server = announcement.server();
            var parent = neighbours.getName(address);
            this.routeTable = new RouteTable(server, parent, announcement.distance());

            try {
                // send RT_ADD to parent
                sendMessage(address, Message.MSG_RT_ADD);
                Print.printInfo(parent + " is the first parent");
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        // if not (and if the distance is shorter)
        else if (announcement.distance() < this.routeTable.distance) {
            var hostname = neighbours.getName(address);

            // if the announcement comes from the current parent
            if (hostname.equals(this.routeTable.parent)) {
                // update its distance
                this.routeTable.distance = announcement.distance();
            } else {
                try {
                    // send current parent RT_DELETE
                    sendMessage(neighbours.getAddress(this.routeTable.parent), Message.MSG_RT_DELETE);
                    // send new parent RT_ADD
                    sendMessage(address, Message.MSG_RT_ADD);
                    Print.printInfo(address + " is the new parent");
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                // update values
                this.routeTable.parent = hostname;
                this.routeTable.distance = announcement.distance();
            }

        }

        // propagate announcement to other neighbours with +1 distance
        try {
            floodMessage(new Message(Type.ANNOUNCEMENT, announcement.increment().toBytes()));
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    /**
     * Processes an user input message.
     * 
     * @param address Address of the message source.
     * @param message User input message.
     */
    protected void userInput(InetAddress address, Message message) {
        var m = new String(message.payload, StandardCharsets.UTF_8);
        Print.printInfo(address + ": " + m);
    }

    /**
     * Processes a route addition message.
     * 
     * @param address Address of the child node that wants to establish a route.
     */
    protected void add(InetAddress address) {
        var hostname = neighbours.getName(address);
        this.routeTable.addRoute(hostname);
        Print.printInfo("Established route to " + hostname);
    }

    /**
     * Processes a route activation message.
     * 
     * @param address Address of the sender.
     */
    protected void activate(InetAddress address) {

        if (this.routeTable != null) {

            // activate child's route
            var hostname = neighbours.getName(address);
            this.routeTable.activateRoute(hostname);
            Print.printInfo("Route to " + hostname + " activated");

            try {
                // sends activation message to parent
                sendMessage(neighbours.getAddress(this.routeTable.parent), Message.MSG_RT_ACTIVATE);
                Print.printInfo("Sent activation message to " + this.routeTable.parent);
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        }

    }

    /**
     * Processes a route deactivation message.
     * 
     * @param address Address of the sender.
     */
    protected void deactivate(InetAddress address) {

        if (this.routeTable != null) {

            // deactivate child's route
            var hostname = neighbours.getName(address);
            this.routeTable.deactivateRoute(hostname);
            Print.printInfo("Route to " + hostname + " deactivated");

            try {
                // sends deactivation message to parent
                sendMessage(neighbours.getAddress(this.routeTable.parent), Message.MSG_RT_DEACTIVATE);
                Print.printInfo("Sent deactivation message to " + this.routeTable.parent);
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        }

    }

    /**
     * Processes a route deletion message.
     * 
     * @param address Address of the sender.
     */
    protected void delete(InetAddress address) {

        if (this.routeTable != null) {
            // delete child's route
            var hostname = neighbours.getName(address);
            this.routeTable.deleteRoute(hostname);
            Print.printInfo("Route to " + hostname + " deleted");
        }

    }

    /**
     * Processes a route loss message.
     */
    protected void lost() {

        if (this.routeTable != null) {

            try {

                // send lost message to children
                for (String hostname : this.routeTable.routes.keySet()) {
                    sendMessage(neighbours.getAddress(hostname), Message.MSG_RT_LOST);
                    Print.printInfo("Sent lost message to " + hostname);
                }

            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

            // delete route table
            routeTable = null;

        }

    }

    /**
     * Processes a data message.
     */
    protected void data(Message message) {

        if (this.routeTable != null) {

            try {

                // send data to children
                for (var entry : this.routeTable.routes.entrySet()) {
                    if (entry.getValue()) {
                        sendMessage(neighbours.getAddress(entry.getKey()), message);
                        Print.printInfo("Sent data message to " + entry.getKey());
                    }
                }

            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        }

    }

    // --------------------
    // Thread runner
    // --------------------

    @Override
    public void run() {

        while (true) {

            var buffer = new byte[Constants.BUFFER_SIZE];
            var packet = new DatagramPacket(buffer, buffer.length);

            try {
                socket.receive(packet);
            } catch (IOException e) {
                Print.printError("Problem recieving packet: " + e.getMessage());
                continue;
            }

            try {

                var message = Message.from_bytes(packet.getData());
                var address = packet.getAddress();

                switch (message.type) {
                    case HEARTBEAT:
                        heartbeat(address);
                        break;
                    case USER_INPUT:
                        userInput(address, message);
                        break;
                    case ANNOUNCEMENT:
                        announcement(address, Announcement.fromBytes(message.payload));
                        break;
                    case DATA:
                        data(message);
                        break;
                    case RT_ADD:
                        add(address);
                        break;
                    case RT_DELETE:
                        delete(address);
                        break;
                    case RT_ACTIVATE:
                        activate(address);
                        break;
                    case RT_DEACTIVATE:
                        deactivate(address);
                        break;
                    case RT_LOST:
                        lost();
                        break;
                    default:
                        Print.printError("Unhandled message type in Listener: " + message.type.name());
                        break;
                }

            } catch (IOException e) {
                e.printStackTrace();
                Print.printError("Problem converting packet: " + e.getMessage());
            }

        }
    }

}
