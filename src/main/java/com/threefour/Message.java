package com.threefour;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class Message {

    /**
     * Type of Message.
     * 
     * 0b 0000 0001: Heartbeat
     * 0b 0000 0010: User input
     */
    public static class Type
    {
        public static final Type HEARTBEAT  = new Type((byte) 1);
        public static final Type USER_INPUT = new Type((byte) 2);

        /**
         * Type's id.
         */
        private byte id;

        /**
         * Constructor for the Type.
         * @param id Type's id.
         */
        private Type(byte id) {
            this.id = id;
        }

        /**
         * Size, in bytes, of a Type.
         * @return Size of a Type. 
         */
        int size()
        {
            return Byte.SIZE;
        }

        public boolean equals(Type t)
        {
            return t.id == this.id; 
        }

        /**
         * Transfoms a Type into bytes and writes them into an output stream. 
         * @param out Output stream to store bytes of Type.
         * @throws IOException 
         */
        void serialize(DataOutputStream out) throws IOException
        {
            out.writeByte(this.id);
        }
        
        /**
         * Reads bytes from an input stream and transforms them into a Type.
         * @param in Input stream to read from.
         * @return New instance of a Type.
         * @throws IOException
         */
        static Type unserialize(DataInputStream in) throws IOException
        {
            byte id = in.readByte();
            
            return new Type(id);
        }
    }


    // Message's type
    public final Type type;
    // Message's payload
    public final byte[] payload;
    // Payload length of the Message
    public final int payload_length;

    /**
     * Constructor for a Message of type HEARTBEAT.
     */
    public Message()
    {
        this.type = Type.HEARTBEAT;
        this.payload_length = 0;
        this.payload = null;
    }

    /**
     * Constructor for a Message.
     * @param type Type of the FS Message protocol.
     * @param payload Bytes (payload) of the FS Message Protocol
     */
    public Message(Type type, byte[] payload)
    {
        this.type = type;
        if(payload == null)
        {
            this.payload_length = 0;
            this.payload = null;
        }
        else
        {
            this.payload_length = payload.length;
            this.payload = payload.clone();
        }
    }

    /**
     * Transfoms a Message into bytes and writes them into an output stream. 
     * @param out Output stream to store bytes of Message.
     * @throws IOException 
     */
    public void serialize(DataOutputStream out) throws IOException
    {
        this.type.serialize(out);
        byte[] payload_length_bytes = ByteBuffer.allocate(4).putInt(payload_length).array();
        out.writeByte(payload_length_bytes[2]);
        out.writeByte(payload_length_bytes[3]);

        if(payload_length > 0)
            out.write(this.payload);
    }

    /**
     * Transfoms a Message into bytes. 
     */
    public byte[] to_bytes() throws IOException
    {
        ByteArrayOutputStream res = new ByteArrayOutputStream();

        this.serialize(new DataOutputStream(res));

        return res.toByteArray();
    }

    /**
     * Reads bytes from an input stream and transforms them into a Message.
     * @param in Input stream to read from.
     * @return New instance of a Message.
     * @throws IOException
     */
    public static Message unserialize(DataInputStream in) throws IOException
    {   
        Type t = Type.unserialize(in);
        byte[] payload_length_bytes = { 0x00, 0x00, 0x00, 0x00 };
        payload_length_bytes[2] = in.readByte();
        payload_length_bytes[3] = in.readByte();
        int payload_length = ByteBuffer.wrap(payload_length_bytes).getInt();
        byte[] payload = in.readNBytes(payload_length);

        return new Message(t,payload);
    }

    /**
     * Reads bytes from a byte array and transforms them into a Message.
     * @param in Byte array to read from.
     * @return New instance of a Message.
     * @throws IOException
     */
    public static Message from_bytes(byte[] in) throws IOException
    {
        return Message.unserialize(new DataInputStream(new ByteArrayInputStream(in)));
    }
    
}
