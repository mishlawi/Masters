package com.threefour.video;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

public class Video {

    FileInputStream fis;
    String filename;
    int frameNum;

    // TODO might be better to not have this hardcoded
    public final int framePeriod = 100;
    public final int videoLength = 500;

    public Video(String filename) throws FileNotFoundException {
        this.fis = new FileInputStream(filename);
        this.filename = filename;
        this.frameNum = 0;
    }

    public boolean hasEnded() {
        return frameNum == videoLength;
    }

    public Frame getNextFrame() throws IOException {
        // read current frame size
        var frameSizeBytes = new byte[5];
        fis.read(frameSizeBytes, 0, 5);
        var frameSize = Integer.parseInt(new String(frameSizeBytes));

        // read current frame
        var frameBytes = new byte[frameSize];
        fis.read(frameBytes, 0, frameSize);

        return new Frame(frameNum++, frameBytes);
    }

    public void reset() {

        try {
            this.fis.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
        }

        try {
            this.fis = new FileInputStream(filename);
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
        }

        this.frameNum = 0;
    }

}
