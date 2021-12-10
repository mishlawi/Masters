package com.threefour.message;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetAddress;

public record Announcement(byte distance, InetAddress server) {

    public byte[] toBytes() throws IOException {
        var byteStream = new ByteArrayOutputStream();
        var out = new DataOutputStream(byteStream);

        out.writeByte(distance);
        if (server != null) {
            out.write(server.getAddress());
        }

        return byteStream.toByteArray();
    }

    public static Announcement fromBytes(byte[] data) throws IOException {
        var in = new DataInputStream(new ByteArrayInputStream(data));

        var distance = in.readByte();

        InetAddress server = null;
        var addr = in.readAllBytes();
        if (addr.length > 0) {
            server = InetAddress.getByAddress(addr);
        }

        return new Announcement(distance, server);
    }

}
