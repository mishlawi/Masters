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
    public Map<String, Boolean> routes;
    public int activeRoutes;

    public RouteTable(InetAddress server, String parent, int distance) {
        this.server = server;
        this.parent = parent;
        this.distance = distance;
        this.routes = new HashMap<>();
        this.activeRoutes = 0;
    }

    public void addRoute(String hostname) {
        this.routes.put(hostname, false);
    }

    public void deleteRoute(String hostname) {
        deactivateRoute(hostname);
        this.routes.remove(hostname);
    }

    public void activateRoute(String hostname) {
        if (this.routes.replace(hostname, true).equals(Boolean.FALSE)) {
            this.activeRoutes += 1;
        }
    }

    public void deactivateRoute(String hostname) {
        if (this.routes.replace(hostname, false).equals(Boolean.TRUE)) {
            this.activeRoutes -= 1;
        }
    }

}
