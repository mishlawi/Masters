package com.threefour.ott.worker;

import com.threefour.Constants;
import com.threefour.overlay.Neighbours;
import com.threefour.util.Print;

public class PulseChecker implements Runnable {

    private Neighbours neighbours;

    public PulseChecker(Neighbours neighbours) {
        this.neighbours = neighbours;
    }

    @Override
    public void run() {
        while (true) {

            this.neighbours.updateLinkStates();

            try {
                Thread.sleep(Constants.TIMEOUT);
            } catch (Exception e) {
                Print.printError("Could not fall asleep: " + e.getMessage());
            }

        }
    }

}
