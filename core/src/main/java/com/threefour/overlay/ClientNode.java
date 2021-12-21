package com.threefour.overlay;

import java.io.IOException;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.List;

import com.google.common.collect.Multimap;
import com.threefour.Constants;
import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.util.Print;
import com.threefour.video.VideoFrame;

public class ClientNode extends Node {

    List<VideoFrame> frames;

    public ClientNode(List<VideoFrame> frames, DatagramSocket socket, Multimap<String, InetAddress> neighbours) {
        super(socket, neighbours);
        this.frames = frames;
    }

    // --------------------
    // Changed methods
    // --------------------

    @Override
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

        Print.printInfo(address + ": " + announcement);

        this.wlRoutes.lock();
        try {
            // if this is the first announcement
            if (this.routeTable == null) {
                // create a new routing table with `address` as parent
                var server = announcement.server();
                var parent = getName(address);

                this.wlRoutes.lock();
                try {
                    this.routeTable = new RouteTable(server, parent, announcement.distance());
                } finally {
                    this.wlRoutes.unlock();
                }

                try {
                    // send RT_ADD to parent
                    sendMessage(address, Message.MSG_RT_ADD);
                    sendMessage(address, Message.MSG_RT_ACTIVATE);
                    Print.printInfo(parent + " is the first parent");
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            // if not (and if the distance is shorter)
            else if (announcement.distance() < this.routeTable.distance) {
                var hostname = this.getName(address);

                // if the announcement doesn't come from the current parent
                if (!hostname.equals(this.routeTable.parent)) {
                    try {
                        // send current parent RT_DELETE
                        sendMessage(this.getAddress(this.routeTable.parent), Message.MSG_RT_DELETE);
                        // send new parent RT_ADD
                        sendMessage(address, Message.MSG_RT_ADD);
                        Print.printInfo(address + " is the new parent");
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                }

                // for safety reasons, the activation message is always sent 
                // upon updating routes
                try {
                    sendMessage(address, Message.MSG_RT_ACTIVATE);
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
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

    @Override
    public void lost() {
        this.wlRoutes.lock();
        try {
            // delete route table
            this.routeTable = null;
        } finally {
            this.wlRoutes.unlock();
        }
    }

    @Override
    public void data(Message videoMsg) {
        byte[] payload = videoMsg.payload;

        try {
            this.frames.add(VideoFrame.fromBytes(payload));
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

}
