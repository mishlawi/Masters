package com.threefour.ott.worker;

import java.io.IOException;
import java.net.DatagramPacket;

import com.threefour.Constants;
import com.threefour.message.Announcement;
import com.threefour.message.Message;
import com.threefour.overlay.Node;
import com.threefour.util.Print;

public class Listener implements Runnable {

    protected Node node;

    public Listener(Node node) {
        this.node = node;
    }

    @Override
    public void run() {

        var buffer = new byte[Constants.BUFFER_SIZE];
        var packet = new DatagramPacket(buffer, buffer.length);

        while (true) {

            try {
                this.node.socket.receive(packet);
            } catch (IOException e) {
                Print.printError("Problem recieving packet: " + e.getMessage());
                e.printStackTrace();
                return;
            }

            try {

                var message = Message.from_bytes(packet.getData());
                var address = packet.getAddress();

                switch (message.type) {
                    case HEARTBEAT:
                        this.node.heartbeat(address);
                        break;
                    case ANNOUNCEMENT:
                        this.node.announcement(address, Announcement.fromBytes(message.payload));
                        break;
                    case DATA:
                        this.node.data(message);
                        break;
                    case RT_ADD:
                        this.node.add(address);
                        break;
                    case RT_DELETE:
                        this.node.delete(address);
                        break;
                    case RT_ACTIVATE:
                        this.node.activate(address);
                        break;
                    case RT_DEACTIVATE:
                        this.node.deactivate(address);
                        break;
                    case RT_LOST:
                        this.node.lost();
                        break;
                    default:
                        Print.printError("Unhandled message type in Listener: " + message.type.name());
                        break;
                }

            } catch (IOException e) {
                e.printStackTrace();
                Print.printError("Problem converting packet: " + e.getMessage());
            }

        }
    }

}
