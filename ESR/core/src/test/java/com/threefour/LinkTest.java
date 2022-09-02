package com.threefour;

import static org.junit.Assert.assertTrue;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.List;

import com.threefour.overlay.Link;

import org.junit.Before;
import org.junit.Test;

public class LinkTest {

    private List<InetAddress> addresses;
    private Link link;

    @Before
    public void setUp() throws UnknownHostException {
        this.addresses = List.of(
                InetAddress.getByName("10.0.0.1"),
                InetAddress.getByName("10.0.0.2"),
                InetAddress.getByName("10.0.0.3"));
        this.link = new Link(addresses);
    }

    @Test
    public void preferredAddressShouldGetSetCorrectly() {
        assertTrue(this.link.getAddress().equals(addresses.get(0)));
        this.link.setPreferredAddress(addresses.get(2));
        assertTrue("Preferred address not set correctly", this.link.getAddress().equals(addresses.get(2)));
    }

    @Test
    public void linkShouldGetActivatedAfterUpdatingTimestamp() {
        assertTrue(!this.link.isActive());
        this.link.updateTimestamp(1L);
        assertTrue("Link didn't get activated", this.link.isActive());
    }

    @Test
    public void preferredAddressShouldChangeAfterLinkDeactivation() {
        assertTrue(this.link.getAddress().equals(addresses.get(0)));
        this.link.deactivateLink();
        assertTrue("Preferred address did not change", this.link.getAddress().equals(addresses.get(1)));
    }

    @Test
    public void preferredAddressShouldLoopAfterReachingTheEnd() {
        assertTrue(this.link.getAddress().equals(addresses.get(0)));
        this.link.shiftPreferredAddress();
        this.link.shiftPreferredAddress();
        this.link.shiftPreferredAddress();
        assertTrue("Preferred address did not loop back", this.link.getAddress().equals(addresses.get(0)));
    }

}
