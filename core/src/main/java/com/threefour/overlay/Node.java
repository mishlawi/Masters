package com.threefour.overlay;

import java.net.InetAddress;
import java.util.List;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.stream.Collectors;

import com.google.common.collect.ImmutableListMultimap;
import com.google.common.collect.ImmutableMultimap;
import com.google.common.collect.Maps;
import com.google.common.collect.Multimap;
import com.threefour.Constants;

/**
 * Class that contains information about the node state in the overlay.
 */
public class Node {

    // mapping to get the name of the host from one of its addresses
    private final ImmutableMultimap<InetAddress, String> ADDRESS_TO_NAME_MAPPING;

    // state of neighbours
    private Map<String, Link> links;
    public Lock readLock;
    public Lock writeLock;

    public Node(Multimap<String, InetAddress> neighbours) {
        // TODO: there might be a more efficient way to do this
        this.ADDRESS_TO_NAME_MAPPING = new ImmutableListMultimap.Builder<String, InetAddress>()
                .putAll(neighbours)
                .build()
                .inverse();
        this.links = Maps.toMap(neighbours.keySet(), key -> new Link(neighbours.get(key)));

        ReadWriteLock linksRWLock = new ReentrantReadWriteLock();
        this.readLock = linksRWLock.writeLock();
        this.writeLock = linksRWLock.readLock();
    }

    /**
     * @return List of the addresses of the active neighbors.
     */
    public List<InetAddress> getAllAddresses() {
        return this.links.values()
                .stream()
                .map(link -> link.getAddress())
                .collect(Collectors.toList());
    }

    /**
     * @return List of the addresses of the active neighbors.
     */
    public List<InetAddress> getActiveAddresses() {
        return this.links.values()
                .stream()
                .filter(link -> link.isActive())
                .map(link -> link.getAddress())
                .collect(Collectors.toList());
    }

    /**
     * Returns the preferred address for a given host name.
     * 
     * @param name Name of the host.
     * @return Address associated with the given host.
     */
    public InetAddress getAddress(String name) {
        return this.links.get(name).getAddress();
    }

    /**
     * Returns the host name for a given address.
     * 
     * @param address Address of the host.
     * @return Name associated with the given address.
     */
    public String getName(InetAddress address) {
        // since the mapping returns a collection of strings, an iterator is
        // used to get the first element of it. in theory, the collection
        // should only have one element, so it should work just fine
        return this.ADDRESS_TO_NAME_MAPPING.get(address).iterator().next();
    }

    /**
     * Deactivates the link with the neighbour of the given name.
     * 
     * @param name Name of the neighbour.
     */
    public void deactivateLink(String name) {
        this.links.get(name).deactivateLink();
    }

    /**
     * Updates the timestamp of the link with the given neighbour.
     * 
     * @param name      Name of the neighbour.
     * @param timestamp Timestamp of the last recieved heartbeat.
     */
    public void updateTimestamp(String name, long timestamp) {
        this.links.get(name).updateTimestamp(timestamp);
    }

    /**
     * Checks the timestamps of all currently active links for timeouts. If a
     * timeout has occurred, the link is set as deactivated.
     */
    public void updateLinkStates() {
        for (var link : this.links.values()) {
            // if the neighbour is active
            if (link.isActive() == true) {
                long gap = System.currentTimeMillis() - link.getTimestamp();

                if (gap > Constants.TIMEOUT) {
                    // neighbours.put(address, new Pair<>(false, info.getValue()));
                    link.deactivateLink();
                }
            }
        }
    }

}
