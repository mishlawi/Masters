package com.threefour.server.worker;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Set;

import com.threefour.Constants;
import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.message.Type;

public class Announcer implements Runnable {

    private DatagramSocket socket;
    private Set<InetAddress> neighbors;

    public Announcer(DatagramSocket socket, Set<InetAddress> neighbors) {
        this.socket = socket;
        this.neighbors = neighbors;
    }

    @Override
    public void run() {
        try {
            var buf = new Message(Type.ANNOUNCEMENT, new Announcement((byte) 0, null).toBytes()).to_bytes();
            var packet = new DatagramPacket(buf, buf.length);
            packet.setPort(Constants.PORT);

            while (true) {

                for (var neighbor : neighbors) {
                    packet.setAddress(neighbor);
                    socket.send(packet);
                }

                try {
                    Thread.sleep(Constants.ANNOUNCE_TIME);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

            }
        } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }

    }

}
