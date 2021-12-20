package com.threefour.server.worker;

import java.io.IOException;
import java.net.DatagramSocket;
import java.net.InetAddress;

import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.ott.data.RouteTable;
import com.threefour.ott.worker.Listener;
import com.threefour.overlay.Node;
import com.threefour.util.Print;

public class ServerListener extends Listener {

    public ServerListener(DatagramSocket socket, Node neighbours) {
        super(socket, neighbours);
        this.routeTable = new RouteTable(null, null, 0);
    }

    // --------------------
    // Changed methods
    // --------------------

    protected void activate(InetAddress address) {
        if (this.routeTable != null) {
            // activate child's route
            var hostname = neighbours.getName(address);
            this.routeTable.activateRoute(hostname);
            Print.printInfo("Route to " + hostname + " activated");
        }
    }

    protected void deactivate(InetAddress address) {
        if (this.routeTable != null) {
            // deactivate child's route
            var hostname = neighbours.getName(address);
            this.routeTable.deactivateRoute(hostname);
            Print.printInfo("Route to " + hostname + " deactivated");
        }
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
