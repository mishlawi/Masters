package com.threefour.overlay;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

import com.google.common.collect.ImmutableListMultimap;
import com.google.common.collect.ImmutableMultimap;
import com.google.common.collect.Maps;
import com.google.common.collect.Multimap;
import com.threefour.Constants;
import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.util.Print;

/**
 * Class that contains information about the node state in the overlay.
 */
public class Node {

    public final DatagramSocket socket;

    // mapping to get the name of the host from one of its addresses
    private final ImmutableMultimap<InetAddress, String> ADDRESS_TO_NAME_MAPPING;

    // state of links with neighbours
    private Map<String, Link> links;
    public Lock rlLinks;
    public Lock wlLinks;

    // route table
    protected RouteTable routeTable;
    public Lock rlRoutes;
    public Lock wlRoutes;

    public Node(DatagramSocket socket, Multimap<String, InetAddress> neighbours) {
        this.socket = socket;

        // TODO: there might be a more efficient way to do this
        this.ADDRESS_TO_NAME_MAPPING = new ImmutableListMultimap.Builder<String, InetAddress>()
                .putAll(neighbours)
                .build()
                .inverse();
        this.links = Maps.toMap(neighbours.keySet(), key -> new Link(neighbours.get(key)));

        ReadWriteLock linksRWLock = new ReentrantReadWriteLock();
        this.rlLinks = linksRWLock.readLock();
        this.wlLinks = linksRWLock.writeLock();

        this.routeTable = null;

        ReadWriteLock routesRWLock = new ReentrantReadWriteLock();
        this.rlRoutes = routesRWLock.readLock();
        this.wlRoutes = routesRWLock.writeLock();
    }

    /**
     * Returns the preferred address for a given host name.
     * 
     * @param name Name of the host.
     * @return Address associated with the given host.
     */
    public InetAddress getAddress(String name) {
        this.rlLinks.lock();
        try {
            return this.links.get(name).getAddress();
        } finally {
            this.rlLinks.unlock();
        }
    }

    /**
     * Returns the host name for a given address.
     * 
     * @param address Address of the host.
     * @return Name associated with the given address.
     */
    public String getName(InetAddress address) {
        // since the mapping returns a collection of strings, an iterator is
        // used to get the first element of it. in theory, the collection
        // should only have one element, so it should work just fine
        return this.ADDRESS_TO_NAME_MAPPING.get(address).iterator().next();
    }

    /**
     * Updates the timestamp of the link with the given neighbour.
     * 
     * @param name      Name of the neighbour.
     * @param timestamp Timestamp of the last recieved heartbeat.
     */
    public void updateTimestamp(String name, long timestamp) {
        this.wlLinks.lock();
        try {
            this.links.get(name).updateTimestamp(timestamp);
        } finally {
            this.wlLinks.unlock();
        }
    }

    /**
     * Checks the timestamps of all currently active links for timeouts. If a
     * timeout has occurred, the link is set as deactivated.
     */
    public void updateLinkStates() {
        this.wlLinks.lock();
        try {
            for (var entry : this.links.entrySet()) {
                var name = entry.getKey();
                var link = entry.getValue();

                // if the link with the neighbour is "active"
                if (link.isActive() == true) {
                    long gap = System.currentTimeMillis() - link.getTimestamp();

                    // if the link timed out
                    if (gap > Constants.TIMEOUT) {
                        // then it is deactivated
                        link.deactivateLink();

                        this.wlRoutes.lock();
                        try {
                            if (this.routeTable != null) {
                                var active = this.routeTable.routes.get(name);

                                // and if it was a link with a child node
                                if (active != null) {
                                    // then it is deleted
                                    delete(getAddress(name));

                                    // if there are no more active routes
                                    if (this.routeTable.activeRoutes == 0) {
                                        // then the parent is notified
                                        if (this.routeTable.parent != null) {
                                            deactivate(getAddress(this.routeTable.parent));
                                        }
                                    }
                                }
                                // or if it was the link with the parent
                                else if (name.equals(this.routeTable.parent)) {
                                    // then the route is declared as lost
                                    lost();
                                }
                            }
                        } finally {
                            this.wlRoutes.unlock();
                        }
                    }
                }
            }
        } finally {
            this.wlLinks.unlock();
        }
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
    public void sendMessage(InetAddress address, Message message) throws IOException {
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
    public void floodMessage(Message message) throws IOException {

        var buf = message.to_bytes();
        var packet = new DatagramPacket(buf, buf.length);
        packet.setPort(Constants.PORT);

        this.rlLinks.lock();
        try {
            this.links.values()
                    .stream()
                    .filter(link -> link.isActive())
                    .map(link -> link.getAddress())
                    .filter(addr -> !(this.routeTable != null
                            && this.routeTable.parent.equals(getName(addr))))
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
            this.rlLinks.unlock();
        }
    }

    /**
     * Floods a message to all active routes.
     * 
     * @param message Message to be flooded.
     * @throws IOException
     */
    public void floodRouteMessage(Message message) throws IOException {

        var buf = message.to_bytes();
        var packet = new DatagramPacket(buf, buf.length);
        packet.setPort(Constants.PORT);

        this.rlRoutes.lock();
        try {
            this.routeTable.routes.entrySet()
                    .stream()
                    .filter(entry -> entry.getValue())
                    .map(entry -> getAddress(entry.getKey()))
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
            this.rlRoutes.unlock();
        }
    }

    /**
     * Floods a message to all neighbours (even the ones with a deactivated link).
     * 
     * @param message Message to be flooded.
     * @throws IOException
     */
    public void floodAllMessage(Message message) throws IOException, InterruptedException {

        var buf = message.to_bytes();
        var packet = new DatagramPacket(buf, buf.length);
        packet.setPort(Constants.PORT);

        this.rlLinks.lock();
        try {
            this.links.values()
                    .forEach(link -> {
                        packet.setAddress(link.getAddress());
                        try {
                            socket.send(packet);
                        } catch (IOException e) {
                            Print.printError("Could not send packet: " + e.getMessage());
                        }
                    });
        } finally {
            this.rlLinks.unlock();
        }

        Thread.sleep(Constants.HEARTBEAT_TIME);

    }

    // --------------------
    // Message processing
    // --------------------

    /**
     * Processes an heartbeat message.
     * 
     * @param address Address of the sender.
     */
    public void heartbeat(InetAddress address) {
        updateTimestamp(getName(address), System.currentTimeMillis());
    }

    /**
     * Processes a server announcement message.
     * 
     * @param address      Address of the sender (parent node).
     * @param announcement Announcement message.
     */
    public void announcement(InetAddress address, Announcement announcement) {

        // if the announcement comes directly from the server, its address
        // needs to be instantiated (because it starts at null, since the
        // server doesn't put its own address in the announcement)
        if (announcement.distance() == 0) {
            announcement = new Announcement((byte) 0, address);
        }
        // if the announcement has jumped too many nodes, it is dropped
        else if (announcement.distance() > Constants.ANNOUNCE_TTL) {
            return;
        }

        // Print.printInfo(address + ": " + announcement);

        this.wlRoutes.lock();
        try {
            // if this is the first announcement
            if (this.routeTable == null) {
                // create a new routing table with `address` as parent
                var server = announcement.server();
                var parent = getName(address);

                this.routeTable = new RouteTable(server, parent, announcement.distance());

                try {
                    // send RT_ADD to parent
                    sendMessage(address, Message.MSG_RT_ADD);
                    Print.printInfo("New routing table with " + parent + " as a parent");
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            // if not (and if the distance is shorter)
            else if (announcement.distance() < this.routeTable.distance) {
                var hostname = getName(address);

                // if the announcement doesn't come from the current parent
                if (!hostname.equals(this.routeTable.parent)) {
                    try {
                        // send current parent RT_DELETE
                        sendMessage(getAddress(this.routeTable.parent), Message.MSG_RT_DELETE);
                        // send new parent RT_ADD
                        sendMessage(address, Message.MSG_RT_ADD);
                        Print.printInfo(address + " is the new parent");
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                }

                this.routeTable.parent = hostname;
                this.routeTable.distance = announcement.distance();
            }
        } finally {
            this.wlRoutes.unlock();
        }

        // propagate announcement to other neighbours with +1 distance
        try {
            this.floodMessage(new Message(Type.ANNOUNCEMENT, announcement.increment().toBytes()));
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    public void ping(InetAddress address, Announcement announcement) {
        var name = getName(address);
        Print.printInfo("PING {jumps: " + announcement.distance() + ", name: " + name + "}");

        // propagate ping to child nodes with +1 distance
        try {
            this.floodRouteMessage(new Message(Type.PING, announcement.increment().toBytes()));
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    /**
     * Processes a route activation message.
     * 
     * @param address Address of the sender.
     */
    public void activate(InetAddress address) {

        // activate child's route
        var hostname = getName(address);
        this.wlRoutes.lock();
        try {
            this.routeTable.activateRoute(hostname);

            // if there were no routes active before
            if (this.routeTable.activeRoutes == 1) {
                try {
                    // sends activation message to parent
                    this.sendMessage(getAddress(this.routeTable.parent), Message.MSG_RT_ACTIVATE);
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                Print.printInfo("Sent activation message to " + this.routeTable.parent);
            }
        } finally {
            this.wlRoutes.unlock();
        }
        Print.printInfo("Route to " + hostname + " activated");

    }

    /**
     * Processes a route deactivation message.
     * 
     * @param address Address of the sender.
     */
    public void deactivate(InetAddress address) {

        // deactivate child's route
        var hostname = getName(address);
        this.wlRoutes.lock();
        try {
            this.routeTable.deactivateRoute(hostname);

            // if there are no more active links, then a deactivation message
            // is sent to the parent
            if (this.routeTable.activeRoutes == 0) {
                try {
                    this.sendMessage(getAddress(this.routeTable.parent), Message.MSG_RT_DEACTIVATE);
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                Print.printInfo("Sent deactivation message to " + this.routeTable.parent);
            }
        } finally {
            this.wlRoutes.unlock();
        }
        Print.printInfo("Route to " + hostname + " deactivated");

    }

    /**
     * Processes a route addition message.
     * 
     * @param address Address of the child node that wants to establish a route.
     */
    public void add(InetAddress address) {
        var hostname = getName(address);
        this.wlRoutes.lock();
        try {
            this.routeTable.addRoute(hostname);
        } finally {
            this.wlRoutes.unlock();
        }
        Print.printInfo("Established route to " + hostname);
    }

    /**
     * Processes a route deletion message.
     * 
     * @param address Address of the sender.
     */
    public void delete(InetAddress address) {

        // delete child's route
        var hostname = getName(address);
        this.wlRoutes.lock();
        try {
            this.routeTable.deleteRoute(hostname);

            // if there are no more active links, then a deactivation message
            // is sent to the parent
            if (this.routeTable.activeRoutes == 0) {
                try {
                    this.sendMessage(getAddress(this.routeTable.parent), Message.MSG_RT_DEACTIVATE);
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                Print.printInfo("Sent deactivation message to " + this.routeTable.parent);
            }
        } finally {
            this.wlRoutes.unlock();
        }
        Print.printInfo("Route to " + hostname + " deleted");

    }

    /**
     * Processes a route loss message.
     */
    public void lost() {

        try {
            // send lost message to children
            for (String hostname : this.routeTable.routes.keySet()) {
                this.sendMessage(getAddress(hostname), Message.MSG_RT_LOST);
                Print.printInfo("Sent lost message to " + hostname);
            }
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        this.wlRoutes.lock();
        try {
            // delete route table
            this.routeTable = null;
        } finally {
            this.wlRoutes.unlock();
        }

    }

    /**
     * Processes a data message.
     */
    public void data(Message message) {
        this.rlRoutes.lock();
        try {
            if (this.routeTable != null) {
                try {
                    // send data to children
                    for (var entry : this.routeTable.routes.entrySet()) {
                        if (entry.getValue()) {
                            this.sendMessage(getAddress(entry.getKey()), message);
                            Print.printInfo("Sent data message to " + entry.getKey());
                        }
                    }
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        } finally {
            this.rlRoutes.unlock();
        }
    }

}
