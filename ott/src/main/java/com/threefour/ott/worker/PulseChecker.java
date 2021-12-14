package com.threefour.ott.worker;

import java.net.InetAddress;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;

import com.threefour.Constants;
import com.threefour.util.Pair;
import com.threefour.util.Print;

public class PulseChecker implements Runnable {

    private Map<InetAddress, Pair<Boolean, Long>> neighbors;
    private Lock nbReadLock;
    private Lock nbWriteLock;

    public PulseChecker(Map<InetAddress, Pair<Boolean, Long>> neighbors,
            ReadWriteLock nbRWLock) {
        this.neighbors = neighbors;
        this.nbReadLock = nbRWLock.readLock();
        this.nbWriteLock = nbRWLock.writeLock();
    }

    @Override
    public void run() {
        while (true) {

            nbReadLock.lock();
            try {

                neighbors.forEach((address, info) -> {

                    // if the neighbour is active
                    if (info.getKey() == true) {

                        long gap = System.currentTimeMillis() - info.getValue();

                        if (gap > Constants.TIMEOUT) {
                            nbWriteLock.lock();
                            try {
                                neighbors.put(address, new Pair<>(false, info.getValue()));
                            } finally {
                                nbWriteLock.unlock();
                            }
                            Print.printInfo(address + ": Got inactivated");
                        }

                    }

                });
            } finally {
                nbReadLock.unlock();
            }

            try {
                Thread.sleep(Constants.TIMEOUT);
            } catch (Exception e) {
                Print.printError("Could not fall asleep: " + e.getMessage());
            }
        }
    }

}
