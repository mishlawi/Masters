package com.threefour.message;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class Message {

    // Message's type
    public final Type type;
    // Message's payload
    public final byte[] payload;
    // Payload length of the Message
    public final int payload_length;

    // Static messages
    public static final Message MSG_HEARTBEAT = new Message(Type.HEARTBEAT, null);
    public static final Message MSG_RT_ADD = new Message(Type.RT_ADD, null);
    public static final Message MSG_RT_DELETE = new Message(Type.RT_DELETE, null);
    public static final Message MSG_RT_ACTIVATE = new Message(Type.RT_ACTIVATE, null);
    public static final Message MSG_RT_DEACTIVATE = new Message(Type.RT_DEACTIVATE, null);
    public static final Message MSG_RT_LOST = new Message(Type.RT_LOST, null);

    /**
     * Constructor for a Message of type HEARTBEAT.
     */
    public Message() {
        this.type = Type.HEARTBEAT;
        this.payload_length = 0;
        this.payload = null;
    }

    /**
     * Constructor for a Message.
     * 
     * @param type    Type of the FS Message protocol.
     * @param payload Bytes (payload) of the FS Message Protocol
     */
    public Message(Type type, byte[] payload) {
        this.type = type;
        if (payload == null) {
            this.payload_length = 0;
            this.payload = null;
        } else {
            this.payload_length = payload.length;
            this.payload = payload.clone();
        }
    }

    /**
     * Transfoms a Message into bytes and writes them into an output stream.
     * 
     * @param out Output stream to store bytes of Message.
     * @throws IOException
     */
    public void serialize(DataOutputStream out) throws IOException {
        if (payload_length > 65535) {
            throw new IOException("Message exceeds maximum size of 65535: Has " + payload_length);
        }

        this.type.serialize(out);

        byte[] payload_length_bytes = ByteBuffer.allocate(4).putInt(payload_length).array();
        out.writeByte(payload_length_bytes[2]);
        out.writeByte(payload_length_bytes[3]);

        if (payload_length > 0)
            out.write(this.payload);
    }

    /**
     * Transfoms a Message into bytes.
     */
    public byte[] to_bytes() throws IOException {
        ByteArrayOutputStream res = new ByteArrayOutputStream();

        this.serialize(new DataOutputStream(res));

        return res.toByteArray();
    }

    /**
     * Reads bytes from an input stream and transforms them into a Message.
     * 
     * @param in Input stream to read from.
     * @return New instance of a Message.
     * @throws IOException
     */
    public static Message unserialize(DataInputStream in) throws IOException {
        Type t = Type.unserialize(in);
        byte[] payload_length_bytes = { 0x00, 0x00, 0x00, 0x00 };
        payload_length_bytes[2] = in.readByte();
        payload_length_bytes[3] = in.readByte();
        int payload_length = ByteBuffer.wrap(payload_length_bytes).getInt();
        byte[] payload = in.readNBytes(payload_length);

        return new Message(t, payload);
    }

    /**
     * Reads bytes from a byte array and transforms them into a Message.
     * 
     * @param in Byte array to read from.
     * @return New instance of a Message.
     * @throws IOException
     */
    public static Message from_bytes(byte[] in) throws IOException {
        return Message.unserialize(new DataInputStream(new ByteArrayInputStream(in)));
    }

}
