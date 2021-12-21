package com.threefour.server.worker;

import java.io.FileNotFoundException;
import java.io.IOException;

import com.threefour.message.Message;
import com.threefour.message.Type;
import com.threefour.overlay.Node;
import com.threefour.util.Print;
import com.threefour.video.VideoFrame;
import com.threefour.video.Video;

public class Streamer implements Runnable {

    private Node node;

    private String filename;

    public Streamer(Node node, String filename) {
        this.node = node;
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
            VideoFrame frame;
            try {
                frame = video.getNextFrame();
            } catch (IOException e) {
                Print.printError("Could not retrieve next frame: " + e.getMessage());
                return;
            }

            // send frame
            try {
                var message = new Message(Type.DATA, frame.toBytes());
                this.node.floodRouteMessage(message);
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
