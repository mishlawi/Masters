package com.threefour;

public class Constants {

    // default port
    public static final int PORT = 12345;
    // default buffer size (theoretical maximum UDP payload size)
    public static final int BUFFER_SIZE = 65507;

    // time gap between heartbeats (ms)
    public static final long HEARTBEAT_TIME = 1000L;
    // neighbours' timeout (ms)
    public static final long TIMEOUT = HEARTBEAT_TIME * 4;

    // time gap between announcements (ms)
    public static final long ANNOUNCE_TIME = 10000L;
    // number of jumps before the announcement is dropped
    public static final byte ANNOUNCE_TTL = 10;

}
