package com.threefour.server.worker;

import java.io.IOException;

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

        while (true) {
            try {
                var message = new Message(Type.ANNOUNCEMENT, new Announcement((byte) 0, null).toBytes());
                this.node.floodAllMessage(message);
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
