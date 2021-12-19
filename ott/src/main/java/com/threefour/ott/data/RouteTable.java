package com.threefour.ott.data;

import java.net.InetAddress;
import java.util.HashMap;
import java.util.Map;

public class RouteTable {

    public final InetAddress server;

    public InetAddress parent;
    public int distance;

    // map of child nodes + route state
    public Map<InetAddress, Boolean> routes = new HashMap<>();

    public RouteTable(InetAddress server, InetAddress parent, int distance) {
        this.server = server;
        this.parent = parent;
        this.distance = distance;
    }
    
    public void addRoute(InetAddress address) {
        this.routes.put(address, false);
    }

    public void deleteRoute(InetAddress address) {
        this.routes.remove(address);
    }

    public void activateRoute(InetAddress address) {
        this.routes.replace(address, true);
    }

    public void deactivateRoute(InetAddress address) {
        this.routes.replace(address, false);
    }

}
