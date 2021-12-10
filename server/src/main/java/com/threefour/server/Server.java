package com.threefour.server;

import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.HashSet;
import java.util.Set;

import com.threefour.Constants;
import com.threefour.server.worker.Announcer;
import com.threefour.util.Print;

public class Server {
    public static void main(String[] args) {

        System.out.println("Running server...");

        Set<InetAddress> neighbors = new HashSet<>();
        DatagramSocket socket = null;

        // parse the addresses of neighbors
        for (var ip : args) {
            try {
                var address = InetAddress.getByName(ip);
                neighbors.add(address);
            } catch (UnknownHostException e) {
                Print.printError("Parsed unknown host " + ip + ": " + e.getMessage());
            }
        }

        // open socket
        try {
            socket = new DatagramSocket(Constants.PORT);
        } catch (SocketException e) {
            Print.printError("Socket error: " + e.getMessage());
            System.exit(1);
        }

        // launch thread to send periodic info (currently main thread)
        new Announcer(socket, neighbors).run();

        // launch thread to send frames
        // later
    }
}
