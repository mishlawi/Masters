package com.threefour;

import static org.junit.Assert.assertTrue;

import java.net.InetAddress;
import java.net.UnknownHostException;

import com.google.common.collect.ArrayListMultimap;
import com.google.common.collect.Multimap;
import com.threefour.overlay.Node;

import org.junit.Before;
import org.junit.Test;

public class NeighboursTest {

    // private List<InetAddress> addresses;
    private Node neighbours;

    @Before
    public void setUp() throws UnknownHostException {
        Multimap<String, InetAddress> nodes = ArrayListMultimap.create();
        nodes.put("server1", InetAddress.getByName("10.0.0.1"));
        nodes.put("server1", InetAddress.getByName("10.0.0.2"));
        nodes.put("server1", InetAddress.getByName("10.0.0.3"));
        nodes.put("server2", InetAddress.getByName("10.0.1.1"));
        nodes.put("server2", InetAddress.getByName("10.0.1.2"));
        nodes.put("server2", InetAddress.getByName("10.0.1.3"));
        this.neighbours = new Node(nodes);
    }

    @Test
    public void nameShouldBeTheSameAfterConversion() {
        var before = "server2";
        var after = this.neighbours.getName(this.neighbours.getAddress(before));
        assertTrue("Name is different after conversion", before.equals(after));
    }

    @Test
    public void addressConversionShouldResultInCorrectName() throws UnknownHostException {
        var expected = "server1";
        var obtained = this.neighbours.getName(InetAddress.getByName("10.0.0.3"));
        assertTrue("Name does not correspond to the address", expected.equals(obtained));
    }

}
