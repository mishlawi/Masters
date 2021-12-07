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
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.concurrent.locks.ReentrantLock;

import com.threefour.util.Print;
import com.threefour.util.Pair;
import com.threefour.Message.Type;

public class Client {

    // client's socket
    private static DatagramSocket socket = null;
    // map with neighbors' adresses, state and timestamp
    private static Map<InetAddress, Pair<Boolean,Long>> neighbors = new HashMap<>();

    // neighbors' map locks
    private static ReadWriteLock nbReadWriteLock = new ReentrantReadWriteLock();
    private static Lock nbWriteLock = nbReadWriteLock.writeLock();
    private static Lock nbReadLock = nbReadWriteLock.writeLock();

    // lock of the standard output
    private static Lock sysoutLock = new ReentrantLock();


    /**
     * Adds a neighbour to a client.
     * @param address Neighbour's address.
    */
    private static void add_neighbour(InetAddress address) {

        nbWriteLock.lock();
        try {
            neighbors.put(address,new Pair<>(false, 0L));
        }finally {nbWriteLock.unlock();}

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

                    nbWriteLock.lock();
                    try{
                        neighbors.put(packet.getAddress(),new Pair<>(true,System.currentTimeMillis()));
                    } finally{nbWriteLock.unlock();}

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
                nbReadLock.lock();
                try{
                    neighbors.forEach((address,info) -> {
                        packet.setAddress(address);
                        try {
                            socket.send(packet);
                        } catch (IOException e) {
                            Print.printError("Could not send packet: " + e.getMessage());
                        }
                    });
                } finally {nbReadLock.unlock();}

                Thread.sleep(Constants.HEARTBEAT_TIME);

            }
        }
        catch(Exception e)
        {
            Print.printError("Could not send packet: " + e.getMessage());
        }

    }


    /**
     * Check neighbour's state.
     */
    public static void check_pulse(){

        while(true) {

            nbReadLock.lock();
            try{
                
                neighbors.forEach((address,info) -> {
                    
                    // if the neighbour is active
                    if(info.getKey() == true){
                        
                        long gap = System.currentTimeMillis() - info.getValue();
                        
                        if(gap > Constants.TIMEOUT){
                            nbWriteLock.lock();
                            try{neighbors.put(address,new Pair<>(false, info.getValue()));}
                            finally{nbWriteLock.unlock();}
                            Print.printInfo(address + ": Got inactivated");
                        }
                        
                    }
                    
                });
            } finally {nbReadLock.unlock();}
            
            try{Thread.sleep(Constants.TIMEOUT);}
            catch(Exception e)
            {
                Print.printError("Could not fall asleep: " + e.getMessage());
            }
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

        // check neighbour's pulse
        new Thread(() -> {check_pulse();}).start();

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

                nbReadLock.lock();
                try{
                    neighbors.forEach((address,info) -> {
                        packet.setAddress(address);
                        try {
                            socket.send(packet);
                        } catch (IOException e) {
                            Print.printError("Could not send packet: " + e.getMessage());
                        }
                    });
                } finally{nbReadLock.unlock();}
                
            }
        } catch (IOException e) {
            Print.printError("Could not read user input: " + e.getMessage());
        }

    }

}