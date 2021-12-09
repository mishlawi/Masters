package com.threefour.message;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;

/**
 * Type of Message.
 * 
 * 0b 0000 0001: Heartbeat
 * 0b 0000 0010: User input
 */
public class Type {

    public static final Type HEARTBEAT = new Type((byte) 1);
    public static final Type USER_INPUT = new Type((byte) 2);

    /**
     * Type's id.
     */
    private byte id;

    /**
     * Constructor for the Type.
     * 
     * @param id Type's id.
     */
    private Type(byte id) {
        this.id = id;
    }

    /**
     * Size, in bytes, of a Type.
     * 
     * @return Size of a Type.
     */
    int size() {
        return Byte.SIZE;
    }

    public boolean equals(Type t) {
        return t.id == this.id;
    }

    /**
     * Transfoms a Type into bytes and writes them into an output stream.
     * 
     * @param out Output stream to store bytes of Type.
     * @throws IOException
     */
    void serialize(DataOutputStream out) throws IOException {
        out.writeByte(this.id);
    }

    /**
     * Reads bytes from an input stream and transforms them into a Type.
     * 
     * @param in Input stream to read from.
     * @return New instance of a Type.
     * @throws IOException
     */
    static Type unserialize(DataInputStream in) throws IOException {
        byte id = in.readByte();

        return new Type(id);
    }
}
