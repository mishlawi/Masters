package com.threefour.overlay;

import java.net.InetAddress;
import java.util.HashMap;
import java.util.Map;

public class RouteTable {

    // TODO find a better way
    public final InetAddress server;

    public String parent;
    public int distance;

    // map of child nodes + route state
    public Map<String, Boolean> routes = new HashMap<>();

    public RouteTable(InetAddress server, String parent, int distance) {
        this.server = server;
        this.parent = parent;
        this.distance = distance;
    }

    public void addRoute(String hostname) {
        this.routes.put(hostname, false);
    }

    public void deleteRoute(String hostname) {
        this.routes.remove(hostname);
    }

    public void activateRoute(String hostname) {
        this.routes.replace(hostname, true);
    }

    public void deactivateRoute(String hostname) {
        this.routes.replace(hostname, false);
    }

}
