package com.threefour.ott;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

import com.threefour.Constants;
import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.ott.worker.*;
import com.threefour.util.Pair;
import com.threefour.util.Print;

public class Ott {

    // client's socket
    private static DatagramSocket socket = null;
    // map with neighbors' adresses, state and timestamp
    private static Map<InetAddress, Pair<Boolean, Long>> neighbors = new HashMap<>();

    // neighbors' map locks
    private static ReadWriteLock nbReadWriteLock = new ReentrantReadWriteLock();
    private static Lock nbWriteLock = nbReadWriteLock.writeLock();
    private static Lock nbReadLock = nbReadWriteLock.readLock();

    public static void main(String[] args) {

        System.out.println("OTT - Structured version");

        // parse the addresses of neighbors
        for (var ip : args) {
            try {
                var address = InetAddress.getByName(ip);

                nbWriteLock.lock();
                try {
                    neighbors.put(address, new Pair<>(false, 0L));
                } finally {
                    nbWriteLock.unlock();
                }
            } catch (UnknownHostException e) {
                Print.printError("Parsed unknown host " + ip + ": " + e.getMessage());
            }
        }

        // open socket
        try {
            socket = new DatagramSocket(Constants.PORT);
        } catch (SocketException e) {
            System.out.println("Socket error: " + e.getMessage());
        }

        // launch thread to listen to messages
        new Thread(new Listener(socket, neighbors, nbReadWriteLock)).start();

        // launch thread to send periodic heartbeats
        new Thread(new PulseSender(socket, neighbors, nbReadLock)).start();

        // launch thread to manage neighbors' pulse
        new Thread(new PulseChecker(neighbors, nbReadWriteLock)).start();

        // read user input and send messages
        var reader = new BufferedReader(new InputStreamReader(System.in));
        String line;
        try {
            while ((line = reader.readLine()) != null) {

                // create a message with user's input of the typer USER_INPUT
                var input = line.getBytes(StandardCharsets.UTF_8);
                byte[] userInput = (new Message(Type.USER_INPUT, input)).to_bytes();
                var packet = new DatagramPacket(userInput, userInput.length);
                packet.setPort(Constants.PORT);

                nbReadLock.lock();
                try {
                    neighbors.forEach((address, info) -> {
                        packet.setAddress(address);
                        try {
                            socket.send(packet);
                        } catch (IOException e) {
                            Print.printError("Could not send packet: " + e.getMessage());
                        }
                    });
                } finally {
                    nbReadLock.unlock();
                }

            }
        } catch (IOException e) {
            Print.printError("Could not read user input: " + e.getMessage());
        }
    }
}
