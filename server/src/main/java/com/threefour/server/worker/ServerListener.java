package com.threefour.server.worker;

import java.net.DatagramSocket;
import java.net.InetAddress;

import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.ott.data.RouteTable;
import com.threefour.ott.worker.Listener;
import com.threefour.overlay.Neighbours;

public class ServerListener extends Listener {

    public ServerListener(DatagramSocket socket, Neighbours neighbours) {
        super(socket, neighbours);
        this.routeTable = new RouteTable(null, null, 0);
    }

    // --------------------
    // Disabled methods
    // --------------------

    @Override
    protected void announcement(InetAddress __ia, Announcement __a) {
        return;
    }

    @Override
    protected void userInput(InetAddress __a, Message __m) {
        return;
    }

    @Override
    protected void lost() {
        return;
    }

    @Override
    protected void data(Message __) {
        return;
    }

}
