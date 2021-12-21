package com.threefour.server.worker;

import java.io.IOException;

import com.threefour.Constants;
import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.overlay.Node;

public class Announcer implements Runnable {

    private Node node;

    public Announcer(Node node) {
        this.node = node;
    }

    @Override
    public void run() {

        Message message;
        Message ping;
        try {
            message = new Message(Type.ANNOUNCEMENT, new Announcement((byte) 0, null).toBytes());
            ping = new Message(Type.PING, new Announcement((byte) 0, null).toBytes());
        } catch (IOException e2) {
            e2.printStackTrace();
            return;
        }

        while (true) {
            try {
                this.node.floodAllMessage(message);
                Thread.sleep(Constants.ANNOUNCE_TIME / 2);
                this.node.floodRouteMessage(ping);
                Thread.sleep(Constants.ANNOUNCE_TIME / 2);
            } catch (IOException e1) {
                // TODO Auto-generated catch block
                e1.printStackTrace();
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }

    }

}
