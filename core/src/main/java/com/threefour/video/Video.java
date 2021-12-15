package com.threefour.video;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

public class Video {

    FileInputStream fis;
    int frameNum;

    public Video(String filename) throws FileNotFoundException {
        this.fis = new FileInputStream(filename);
        this.frameNum = 0;
    }

    public Frame getNextFrame() throws IOException {
        // read current frame size
        var frameSizeBytes = new byte[5];
        fis.read(frameSizeBytes, 0, 5);
        var frameSize = Integer.parseInt(new String(frameSizeBytes));

        // read current frame
        var frameBytes = new byte[frameSize];
        fis.read(frameBytes, 0, frameSize);

        return new Frame(frameNum, frameBytes);
    }

}
