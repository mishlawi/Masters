package com.threefour;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.IOException;
import java.net.InetAddress;
import java.util.Arrays;

import com.threefour.message.Announcement;
import com.threefour.video.VideoFrame;

import org.junit.Test;

public class AppTest {

    @Test
    public void announcementIsTheSameAfterSerialization() {
        try {
            var before = new Announcement((byte) 10, InetAddress.getByName("127.0.0.1"));
            var after = Announcement.fromBytes(before.toBytes());
            assertTrue("Announcement is different after serialization", before.equals(after));
        } catch (IOException e) {
            e.printStackTrace();
            fail("Exception thrown");
        }
    }

    @Test
    public void announcementSerializationWithNullServer() {
        try {
            var before = new Announcement((byte) 10, null);
            var after = Announcement.fromBytes(before.toBytes());
            assertTrue("Announcement is different after serialization", before.equals(after));
        } catch (IOException e) {
            e.printStackTrace();
            fail("Exception thrown");
        }
    }

    @Test
    public void frameIsTheSameAfterSerialization() {
        try {
            var before = new VideoFrame(10, new byte[] { 13, 42 });
            var after = VideoFrame.fromBytes(before.toBytes());
            assertTrue("Frame is different after serialization",
                    before.frameNum() == after.frameNum() && Arrays.equals(before.data(), after.data()));
        } catch (IOException e) {
            e.printStackTrace();
            fail("Exception thrown");
        }
    }

}
