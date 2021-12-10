package com.threefour.ott.worker;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;

import com.threefour.Constants;
import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.util.Pair;
import com.threefour.util.Print;

public class Listener implements Runnable {

    private DatagramSocket socket;

    private Map<InetAddress, Pair<Boolean, Long>> neighbors;
    private Lock nbReadLock;
    private Lock nbWriteLock;

    public Listener(DatagramSocket socket,
            Map<InetAddress, Pair<Boolean, Long>> neighbors, ReadWriteLock nbRWLock) {
        this.socket = socket;
        this.neighbors = neighbors;
        this.nbReadLock = nbRWLock.readLock();
        this.nbWriteLock = nbRWLock.writeLock();
    }

    @Override
    public void run() {

        while (true) {

            var buffer = new byte[Constants.BUFFER_SIZE];
            var packet = new DatagramPacket(buffer, buffer.length);

            try {
                socket.receive(packet);
            } catch (IOException e) {
                Print.printError("Problem recieving packet: " + e.getMessage());
                continue;
            }

            try {

                Message message = Message.from_bytes(packet.getData());

                /** check message type **/

                // update neighbour's timestamp if it's an heartbeat
                if (message.type.equals(Type.HEARTBEAT)) {

                    nbWriteLock.lock();
                    try {
                        neighbors.put(packet.getAddress(), new Pair<>(true, System.currentTimeMillis()));
                    } finally {
                        nbWriteLock.unlock();
                    }

                    System.out.println("Received a heartbeat from: " + packet.getAddress());

                }

                // print message if it's a user input
                if (message.type.equals(Type.USER_INPUT)) {
                    var m = new String(message.payload, StandardCharsets.UTF_8);
                    System.out.println(packet.getAddress() + ": " + m);
                }

            } catch (IOException e) {
                Print.printError("Problem converting packet: " + e.getMessage());
            }

        }
    }

}
