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

    private DatagramSocket socket;

    private Map<InetAddress, Pair<Boolean, Long>> neighbors;
    private Lock nbReadLock;
    private Lock nbWriteLock;

    private RouteTable routeTable = null;

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
    private void sendMessage(InetAddress address, Message message) throws IOException {
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
    private void floodMessage(Message message) throws IOException {
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
    private void heartbeat(InetAddress address) {
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
    private void announcement(InetAddress address, Announcement announcement) {

        // if the announcement comes directly from the server, its address
        // to be instantiated (because it starts at null, since the server
        // doesn't put its own address in the announcement)
        if (announcement.distance() == 0) {
            announcement = new Announcement((byte) 0, address);
        }

        Print.printInfo("Got announcement: " + announcement);

        // if this is the first announcement
        if (this.routeTable == null) {
            // create a new routing table with `address` as parent
            this.routeTable = new RouteTable(announcement.server(), address, announcement.distance());

            try {
                // send RT_ADD to parent
                sendMessage(address, Message.MSG_RT_ADD);
                Print.printInfo(address + " is the first parent");
                // propagate announcement to other neighbors with +1 distance
                floodMessage(new Message(Type.ANNOUNCEMENT, announcement.increment().toBytes()));
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

            try {
                // propagate announcement to other neighbors with +1 distance
                floodMessage(new Message(Type.ANNOUNCEMENT, announcement.increment().toBytes()));
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        // if not any of the above, do nothing
    }

    /**
     * Processes an user input message.
     * 
     * @param address Address of the message source.
     * @param message User input message.
     */
    private void userInput(InetAddress address, Message message) {
        var m = new String(message.payload, StandardCharsets.UTF_8);
        Print.printInfo(address + ": " + m);
    }

    /**
     * Processes a route addition message.
     * 
     * @param address Address of the child node that wants to establish a route.
     */
    private void routeAdd(InetAddress address) {
        this.routeTable.addRoute(address);
        Print.printInfo("Established route to " + address);
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
                        // TODO: on step 4
                        break;
                    case RT_ADD:
                        routeAdd(address);
                        break;
                    case RT_DELETE:
                        // TODO
                        break;
                    case RT_ACTIVATE:
                        // TODO
                        break;
                    case RT_DEACTIVATE:
                        // TODO
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
