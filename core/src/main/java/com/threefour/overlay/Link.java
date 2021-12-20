package com.threefour.overlay;

import java.net.InetAddress;
import java.util.Collection;
import java.util.List;

/**
 * Class that defines the state of a link.
 * 
 * A link is a connection between two overlay nodes. Since one node in the
 * overlay can have multiple address in the underlay, a list of known addresses
 * is stored and one of them is elected the "preferred" address. That address
 * will only change when the link gets deactivated, it gets manually shifted
 * or is explicitly changed.
 */
public class Link {

    // available addresses in the underlay
    private List<InetAddress> addresses;
    // index of the address that the messages should be sent to
    private int preferredAddress;
    // state of the connection
    private boolean active;
    // timestamp of the last recieved heartbeat
    private long timestamp;

    /**
     * Creates an inactive LinkState.
     */
    public Link(Collection<InetAddress> addresses) {
        this.addresses = addresses.stream().toList();
        this.preferredAddress = 0;
        this.active = false;
        this.timestamp = 0;
    }

    /**
     * @return The timestamp of the last recieved heartbeat.
     */
    public long getTimestamp() {
        return this.timestamp;
    }

    /**
     * @return The preferred address of the link.
     */
    public InetAddress getAddress() {
        return this.addresses.get(preferredAddress);
    }

    /**
     * Indicates if the link is active.
     * 
     * @return `true` if the link is active, `false` if not.
     */
    public boolean isActive() {
        return this.active;
    }

    /**
     * Deactivates the link and picks a new preferred address.
     */
    public void deactivateLink() {
        this.active = false;
        this.timestamp = 0;
        this.shiftPreferredAddress();
    }

    /**
     * Shifts the preferred address.
     */
    public void shiftPreferredAddress() {
        this.preferredAddress = (this.preferredAddress + 1) % this.addresses.size();
    }

    /**
     * Sets the address that the link should use by default.
     * 
     * @param address Address to be set.
     */
    public void setPreferredAddress(InetAddress address) {
        this.preferredAddress = this.addresses.indexOf(address);
    }

    /**
     * Updates the timestamp and sets the link as active.
     * 
     * @param timestamp Timestamp of the last message recieved.
     */
    public void updateTimestamp(long timestamp) {
        this.active = true;
        this.timestamp = timestamp;
    }

}
