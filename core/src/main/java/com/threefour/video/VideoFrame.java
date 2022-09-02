package com.threefour.video;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;

public record VideoFrame(int frameNum, byte[] data) {

    public byte[] toBytes() throws IOException {
        var byteStream = new ByteArrayOutputStream();
        var out = new DataOutputStream(byteStream);

        out.writeInt(frameNum);
        out.write(data);

        return byteStream.toByteArray();
    }

    public static VideoFrame fromBytes(byte[] data) throws IOException {
        var in = new DataInputStream(new ByteArrayInputStream(data));

        var frameNum = in.readInt();
        var frameData = in.readAllBytes();

        return new VideoFrame(frameNum, frameData);
    }

}
