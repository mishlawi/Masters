package com.threefour;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.IOException;
import java.net.InetAddress;

import com.threefour.message.Announcement;

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

}
