package com.threefour;

public class Constants {

    // default port
    public static final int PORT = 12345;
    // default buffer size
    public static final int BUFFER_SIZE = 1024;

    // time gap between heartbeats (ms)
    public static final long HEARTBEAT_TIME = 1000L;
    // neighbours' timeout (ms)
    public static final long TIMEOUT = HEARTBEAT_TIME * 4;

}
