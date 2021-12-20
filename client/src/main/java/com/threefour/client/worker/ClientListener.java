package com.threefour.client.worker;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.List;
import java.util.Map;
import java.util.concurrent.locks.ReadWriteLock;

import com.threefour.client.worker.GUI;
import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.ott.data.RouteTable;
import com.threefour.ott.worker.Listener;
import com.threefour.overlay.Node;
import com.threefour.util.Pair;
import com.threefour.util.Print;
import com.threefour.video.VideoFrame;

public class ClientListener extends Listener {

    List<VideoFrame> f;

    public ClientListener(List<VideoFrame> f, DatagramSocket socket, Node neighbors) {
        super(socket, neighbors);
        this.f = f;
    }

    // --------------------
    // Changed methods
    // --------------------

    @Override
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
                sendMessage(address, Message.MSG_RT_ACTIVATE);
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

    @Override
    protected void data(Message videoMsg) {
        byte[] payload = videoMsg.payload;

        try {
            f.add(VideoFrame.fromBytes(payload));
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    // --------------------
    // Disabled methods
    // --------------------

    @Override
    protected void userInput(InetAddress __a, Message __m) {
        return;
    }

}
