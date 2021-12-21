package com.threefour.overlay;

import java.net.DatagramSocket;
import java.net.InetAddress;

import com.google.common.collect.Multimap;
import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.util.Print;

public class ServerNode extends Node {

    public ServerNode(DatagramSocket socket, Multimap<String, InetAddress> neighbours) {
        super(socket, neighbours);
        this.routeTable = new RouteTable(null, null, 0);
    }

    // --------------------
    // Changed methods
    // --------------------

    public void activate(InetAddress address) {
        // if (this.routeTable != null) {
            // activate child's route
            var hostname = getName(address);
            this.wlRoutes.lock();
            try {
                this.routeTable.activateRoute(hostname);
            } finally {
                this.wlRoutes.unlock();
            }
            Print.printInfo("Route to " + hostname + " activated");
        // }
    }

    public void deactivate(InetAddress address) {
        // if (this.routeTable != null) {
            // deactivate child's route
            var hostname = getName(address);
            this.wlRoutes.lock();
            try {
                this.routeTable.deactivateRoute(hostname);
            } finally {
                this.wlRoutes.unlock();
            }
            Print.printInfo("Route to " + hostname + " deactivated");
        // }
    }

    // --------------------
    // Disabled methods
    // --------------------

    @Override
    public void announcement(InetAddress __ia, Announcement __a) {
        return;
    }

    @Override
    public void lost() {
        return;
    }

    @Override
    public void data(Message __) {
        return;
    }

}
