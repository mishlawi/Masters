package com.threefour.server.worker;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

import com.threefour.Constants;
import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.overlay.Neighbours;

public class Announcer implements Runnable {

    private DatagramSocket socket;
    private Neighbours neighbours;

    public Announcer(DatagramSocket socket, Neighbours neighbours) {
        this.socket = socket;
        this.neighbours = neighbours;
    }

    @Override
    public void run() {
        try {
            var buf = new Message(Type.ANNOUNCEMENT, new Announcement((byte) 0, null).toBytes()).to_bytes();
            var packet = new DatagramPacket(buf, buf.length);
            packet.setPort(Constants.PORT);

            while (true) {

                var addresses = neighbours.getActiveAdresses();

                for (var neighbor : addresses) {
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
