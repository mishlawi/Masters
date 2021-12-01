package com.threefour;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import com.threefour.util.Print;

public class AppUdp {

    // default port
    private static final int PORT = 12345;
    // default buffer size
    private static final int BUFFER_SIZE = 1024;

    public static void main(String[] args) {

        System.out.println("OTT - UDP version");

        // set of the addresses of neighbors
        Set<InetAddress> neighbors = new HashSet<>();
        // lock of the standard output
        Lock sysoutLock = new ReentrantLock();

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
        try (DatagramSocket socket = new DatagramSocket(PORT)) {

            // listen to messages
            new Thread(() -> {
                while (true) {
                    var buffer = new byte[BUFFER_SIZE];
                    var packet = new DatagramPacket(buffer, buffer.length);

                    try {
                        socket.receive(packet);
                    } catch (IOException e) {
                        Print.printError("Problem recieving packet: " + e.getMessage());
                        continue;
                    }

                    var message = new String(buffer, StandardCharsets.UTF_8);

                    sysoutLock.lock();
                    try {
                        System.out.println(packet.getAddress() + ": " + message);
                    } finally {
                        sysoutLock.unlock();
                    }
                }
            }).start();

            // read user input and send messages
            var reader = new BufferedReader(new InputStreamReader(System.in));
            String line;
            try {
                while ((line = reader.readLine()) != null) {
                    var buffer = line.getBytes(StandardCharsets.UTF_8);
                    var packet = new DatagramPacket(buffer, buffer.length);
                    packet.setPort(PORT);

                    for (var ip : neighbors) {
                        packet.setAddress(ip);
                        socket.send(packet);
                    }
                }
            } catch (IOException e) {
                Print.printError("Could not read user input: " + e.getMessage());
            }

        } catch (SocketException e) {
            Print.printError("Socket error: " + e.getMessage());
        }

    }
}
