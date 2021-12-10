package com.threefour.ott.worker;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Map;
import java.util.concurrent.locks.Lock;

import com.threefour.Constants;
import com.threefour.message.Message;
import com.threefour.util.Pair;
import com.threefour.util.Print;

public class PulseSender implements Runnable {

    private DatagramSocket socket;

    private Map<InetAddress, Pair<Boolean, Long>> neighbors;
    private Lock nbReadLock;

    public PulseSender(DatagramSocket socket,
            Map<InetAddress, Pair<Boolean, Long>> neighbors, Lock nbReadLock) {
        this.socket = socket;
        this.neighbors = neighbors;
        this.nbReadLock = nbReadLock;
    }

    @Override
    public void run() {
        try {

            byte[] heartbeat = (new Message()).to_bytes();
            DatagramPacket packet = new DatagramPacket(heartbeat, heartbeat.length);
            packet.setPort(Constants.PORT);

            while (socket != null) {
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

                Thread.sleep(Constants.HEARTBEAT_TIME);

            }
        } catch (Exception e) {
            Print.printError("Could not send packet: " + e.getMessage());
        }

    }

}
