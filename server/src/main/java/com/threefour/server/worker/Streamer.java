package com.threefour.server.worker;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

import com.threefour.Constants;
import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.overlay.Neighbours;
import com.threefour.util.Print;
import com.threefour.video.Frame;
import com.threefour.video.Video;

public class Streamer implements Runnable {

    private DatagramSocket socket;
    private Neighbours neighbours;

    private String filename;

    public Streamer(DatagramSocket socket, Neighbours neighbours, String filename) {
        this.socket = socket;
        this.neighbours = neighbours;
        this.filename = filename;
    }

    @Override
    public void run() {

        // initialize video
        Video video;
        try {
            video = new Video(filename);
        } catch (FileNotFoundException e) {
            Print.printError("Video " + filename + " not found.");
            return;
        }

        while (true) {

            if (video.hasEnded()) {
                video.reset();
            }

            // read frame
            Frame frame;
            try {
                frame = video.getNextFrame();
            } catch (IOException e) {
                Print.printError("Could not retrieve next frame: " + e.getMessage());
                return;
            }

            // send frame
            try {
                var message = new Message(Type.DATA, frame.toBytes()).to_bytes();
                var packet = new DatagramPacket(message, message.length);
                packet.setPort(Constants.PORT);

                var addresses = neighbours.getActiveAddresses();

                for (var addr : addresses) {
                    packet.setAddress(addr);
                    socket.send(packet);
                }
            } catch (IOException e) {
                Print.printError("Could not send frame: " + e.getMessage());
            }

            // sleep for frame interval
            try {
                Thread.sleep(video.framePeriod);
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }

    }

}
