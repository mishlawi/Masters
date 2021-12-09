package com.threefour;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import com.threefour.util.Print;

public class App {

    // default port
    private static final int PORT = 12345;
    // set of socket connections to other neighbors
    private static Set<Socket> connections = new HashSet<>();
    // set of outputs to other neighbors
    private static Set<PrintWriter> outs = new HashSet<>();
    // lock of terminal output
    private static Lock sysOutLock = new ReentrantLock();

    // launches a thread that listens to new messages on the socket and prints
    // them on the standard output
    private static void startListener(Socket socket) throws IOException {
        var in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

        new Thread(() -> {
            try {
                while (true) {
                    var message = in.readLine();

                    if (message == null) {
                        System.exit(1);
                    }

                    sysOutLock.lock();
                    try {
                        System.out.println(socket.getInetAddress() + ": " + message);
                    } finally {
                        sysOutLock.unlock();
                    }
                }
            } catch (IOException e) {
                Print.printError("Error on socket " + socket.getInetAddress() + ": " + e.getMessage());
            }
        }).start();
    }

    // handle a new client connection
    private static void handleClient(Socket socket) throws IOException {
        connections.add(socket);
        outs.add(new PrintWriter(socket.getOutputStream(), true));
        startListener(socket);
    }

    public static void main(String[] args) {

        System.out.println("OTT - TCP version");

        // connect to neighbors
        for (var ip : args) {
            try {
                var addr = InetAddress.getByName(ip);
                handleClient(new Socket(addr, PORT));
                Print.printInfo("Connected to " + ip);
            } catch (IOException e) {
                Print.printError(ip + e.getMessage());
                System.exit(1);
            }
        }

        // open server socket
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {

            // launch dedicated thread for future neighbor connections
            new Thread(() -> {
                try {
                    while (true) {
                        var socket = serverSocket.accept();

                        sysOutLock.lock();
                        try {
                            Print.printInfo("New connection: " + socket.getInetAddress());
                        } finally {
                            sysOutLock.unlock();
                        }

                        handleClient(socket);
                    }
                } catch (SocketException e) {
                    Print.printInfo("The server socket was closed. Shutting down...");
                    System.exit(0);
                } catch (IOException e) {
                    Print.printError("Could not establish connection to client: " + e.getMessage());
                }
            }).start();

            // read user input
            BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
            String line;
            try {
                while ((line = in.readLine()) != null) {
                    // send input to all neighbors
                    for (var out : outs) {
                        out.println(line);
                        out.flush();
                    }
                }
            } catch (IOException e) {
                Print.printError("Could not read user input: " + e.getMessage());
            }

        } catch (IOException e) {
            Print.printError("Could not open server socket: " + e.getMessage());
            System.exit(1);
        }

        // close all sockets
        for (var socket : connections) {
            try {
                socket.close();
            } catch (IOException e) {
                Print.printWarning("Could not close socket: " + e.getMessage());
            }
        }

    }
}
