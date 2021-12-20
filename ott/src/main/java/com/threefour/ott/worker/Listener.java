package com.threefour.ott.worker;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;

import com.threefour.Constants;
import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.ott.data.RouteTable;
import com.threefour.util.Pair;
import com.threefour.util.Print;

public class Listener implements Runnable {

    protected DatagramSocket socket;

    protected Map<InetAddress, Pair<Boolean, Long>> neighbors;
    protected Lock nbReadLock;
    protected Lock nbWriteLock;

    protected RouteTable routeTable = null;

    public Listener(DatagramSocket socket,
            Map<InetAddress, Pair<Boolean, Long>> neighbors, ReadWriteLock nbRWLock) {
        this.socket = socket;
        this.neighbors = neighbors;
        this.nbReadLock = nbRWLock.readLock();
        this.nbWriteLock = nbRWLock.writeLock();
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
     * Floods a message to all available neighbors (except parent).
     * 
     * @param message Message to be flooded.
     * @throws IOException
     */
    protected void floodMessage(Message message) throws IOException {
        var buf = message.to_bytes();
        var packet = new DatagramPacket(buf, buf.length);
        packet.setPort(Constants.PORT);

        this.nbReadLock.lock();
        try {
            neighbors.entrySet()
                    .stream()
                    .filter((entry) -> entry.getValue().getKey()
                            && !(this.routeTable != null && this.routeTable.parent.equals(entry.getKey())))
                    .forEach((entry) -> {
                        packet.setAddress(entry.getKey());
                        try {
                            socket.send(packet);
                        } catch (IOException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        }
                    });
        } finally {
            this.nbReadLock.unlock();
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
        nbWriteLock.lock();
        try {
            neighbors.put(address, new Pair<>(true, System.currentTimeMillis()));
        } finally {
            nbWriteLock.unlock();
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
            this.routeTable = new RouteTable(announcement.server(), address, announcement.distance());

            try {
                // send RT_ADD to parent
                sendMessage(address, Message.MSG_RT_ADD);
                Print.printInfo(address + " is the first parent");
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        // if not (and if the distance is shorter)
        else if (announcement.distance() < this.routeTable.distance) {
            // if the announcement comes from the current parent
            if (address.equals(this.routeTable.parent)) {
                // update its distance
                this.routeTable.distance = announcement.distance();
            } else {
                try {
                    // send current parent RT_DELETE
                    sendMessage(this.routeTable.parent, Message.MSG_RT_DELETE);
                    // send new parent RT_ADD
                    sendMessage(address, Message.MSG_RT_ADD);
                    Print.printInfo(address + " is the new parent");
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                // update values
                this.routeTable.parent = address;
                this.routeTable.distance = announcement.distance();
            }

        }

        // propagate announcement to other neighbors with +1 distance
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
        this.routeTable.addRoute(address);
        Print.printInfo("Established route to " + address);
    }

    /**
     * Processes a route activation message.
     * 
     * @param address Address of the sender.
     */
    protected void activate(InetAddress address) {

        if (this.routeTable != null) {

            // activate child's route
            this.routeTable.activateRoute(address);
            Print.printInfo("Route to " + address + " activated");

            try {
                // sends activation message to parent
                sendMessage(this.routeTable.parent, Message.MSG_RT_ACTIVATE);
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
            this.routeTable.deactivateRoute(address);
            Print.printInfo("Route to " + address + " deactivated");

            try {
                // sends deactivation message to parent
                sendMessage(this.routeTable.parent, Message.MSG_RT_DEACTIVATE);
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
            this.routeTable.deleteRoute(address);
            Print.printInfo("Route to " + address + " deleted");
        }

    }

    /**
     * Processes a route loss message.
     */
    protected void lost() {

        if (this.routeTable != null) {

            try {

                // send lost message to children
                for (InetAddress address : this.routeTable.routes.keySet()) {
                    sendMessage(address, Message.MSG_RT_LOST);
                    Print.printInfo("Sent lost message to " + address);
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
                        sendMessage(entry.getKey(), message);
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
