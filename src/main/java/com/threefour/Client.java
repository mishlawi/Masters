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
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import com.threefour.util.Print;
import com.threefour.Message.Type;

public class Client {

    // client's socket
    private static DatagramSocket socket = null;
    // map with neighbors' adresses and timestamp
    private static Map<InetAddress, Long> neighbors = new HashMap<>();
    // neighbors' map lock 
    private static Lock nbLock = new ReentrantLock();

    // lock of the standard output
    private static Lock sysoutLock = new ReentrantLock();

    /**
     * Adds a neighbour to a client.
     * @param address Neighbour's address.
    */
    private static void add_neighbour(InetAddress address) {

        nbLock.lock();
        try {
            neighbors.put(address,0L);
        }finally {nbLock.unlock();}

    }

    /**
     * Listens to socket messages.
     */
    private static void listen(){

        while (true) {

            var buffer = new byte[Constants.BUFFER_SIZE];
            var packet = new DatagramPacket(buffer, buffer.length);

            try {
                socket.receive(packet);
            } catch (IOException e) {
                Print.printError("Problem recieving packet: " + e.getMessage());
                continue;
            }

            try{

                Message message = Message.from_bytes(packet.getData());

                /** check message type **/

                // update neighbour's timestamp if it's an heartbeat
                if (message.type.equals(Type.HEARTBEAT)) {

                    neighbors.put(packet.getAddress(),System.currentTimeMillis());
                    System.out.println("Received a heartbeat from: " + packet.getAddress());

                }

                // print message if it's a user input
                if (message.type.equals(Type.USER_INPUT)) {
                
                    var m = new String(message.payload, StandardCharsets.UTF_8);

                    sysoutLock.lock();
                    try {
                        System.out.println(packet.getAddress() + ": " + m);
                    } finally {
                        sysoutLock.unlock();
                    }

                }

            } catch (IOException e) {
                Print.printError("Problem converting packet: " + e.getMessage());
            }    

        }

    }

    /**
     * This thread sends a heartbeat every Constant.HEARTBEAT_TIME miliseconds to every single neighbour.
     */
    public static void heartbeat()
    {
        try{

            byte[] heartbeat = (new Message()).to_bytes();
            DatagramPacket packet = new DatagramPacket(heartbeat, heartbeat.length);
            packet.setPort(Constants.PORT);

            while(socket != null)
            {
                neighbors.forEach((address,timestamp) -> {
                    packet.setAddress(address);
                    try {
                        socket.send(packet);
                    } catch (IOException e) {
                        Print.printError("Could not send packet: " + e.getMessage());
                    }
                });

                Thread.sleep(Constants.HEARTBEAT_TIME);

            }
        }
        catch(Exception e)
        {
            Print.printError("Could not send packet: " + e.getMessage());
        }

    }

    public static void main(String[] args) {

        // parse the addresses of neighbors
        for (var ip : args) {
            try {
                var address = InetAddress.getByName(ip);
                add_neighbour(address);
                
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

        // listen to messages
        new Thread(() -> {listen();}).start();

        // send heartbeats
        new Thread(() -> {heartbeat();}).start();

        // read user input and send messages
        var reader = new BufferedReader(new InputStreamReader(System.in));
        String line;
        try {
            while ((line = reader.readLine()) != null) {

                // create a message with user's input of the typer USER_INPUT
                var input = line.getBytes(StandardCharsets.UTF_8);
                byte[] userInput = (new Message(Type.USER_INPUT,input)).to_bytes();
                var packet = new DatagramPacket(userInput, userInput.length);
                packet.setPort(Constants.PORT);

                neighbors.forEach((address,timestamp) -> {
                    packet.setAddress(address);
                    try {
                        socket.send(packet);
                    } catch (IOException e) {
                        Print.printError("Could not send packet: " + e.getMessage());
                    }
                });

            }
        } catch (IOException e) {
            Print.printError("Could not read user input: " + e.getMessage());
        }

    }

}


