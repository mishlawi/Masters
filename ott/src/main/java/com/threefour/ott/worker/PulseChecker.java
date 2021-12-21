package com.threefour.ott.worker;

import com.threefour.Constants;
import com.threefour.overlay.Node;
import com.threefour.util.Print;

public class PulseChecker implements Runnable {

    private Node node;

    public PulseChecker(Node node) {
        this.node = node;
    }

    @Override
    public void run() {

        while (true) {
            this.node.updateLinkStates();

            try {
                Thread.sleep(Constants.TIMEOUT);
            } catch (Exception e) {
                Print.printError("Could not fall asleep: " + e.getMessage());
            }
        }

    }

}
