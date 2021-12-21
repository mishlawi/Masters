package com.threefour.ott.worker;

import java.io.IOException;

import com.threefour.message.Message;
import com.threefour.overlay.Node;

public class PulseSender implements Runnable {

    private Node node;

    public PulseSender(Node node) {
        this.node = node;
    }

    @Override
    public void run() {

        while (true) {
            try {
                this.node.floodAllMessage(Message.MSG_HEARTBEAT);
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }

    }

}
