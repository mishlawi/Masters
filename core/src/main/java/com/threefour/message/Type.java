package com.threefour.message;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;

/**
 * Type of Message.
 */
public enum Type {

    // general types
    HEARTBEAT,
    USER_INPUT,
    ANNOUNCEMENT,
    DATA,

    // route related types
    RT_ADD,
    RT_DELETE,
    RT_ACTIVATE,
    RT_DEACTIVATE;

    // array of all possible type values (indexed by the .ordinal() value)
    private static final Type[] types = Type.values();

    /**
     * Transfoms a Type into bytes and writes them into an output stream.
     * 
     * @param out Output stream to store bytes of Type.
     * @throws IOException
     */
    void serialize(DataOutputStream out) throws IOException {
        // TODO: check if this is 100% correct
        out.writeByte(this.ordinal());
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
        return types[id];
    }

}
