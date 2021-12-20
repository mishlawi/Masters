package com.threefour.client.worker;

import com.threefour.video.VideoFrame;

import java.util.List;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.Timer;

public class GUI {

    List<VideoFrame> fps;

    // GUI variables
    JFrame f = new JFrame("Cliente de Testes");
    JButton playButton = new JButton("Play");
    JButton tearButton = new JButton("Teardown");
    JPanel mainPanel = new JPanel();
    JPanel buttonPanel = new JPanel();
    JLabel iconLabel = new JLabel();
    ImageIcon icon;
    Timer cTimer;

    public GUI(List<VideoFrame> fps) {
        this.fps = fps;

        // frame
        f.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                System.exit(0);
            }
        });

        // buttons
        buttonPanel.setLayout(new GridLayout(1, 0));
        buttonPanel.add(playButton);
        buttonPanel.add(tearButton);

        // handlers
        playButton.addActionListener(new playButtonListener());
        tearButton.addActionListener(new tearButtonListener());

        // Iiage display label
        iconLabel.setIcon(null);

        // frame layout
        mainPanel.setLayout(null);
        mainPanel.add(iconLabel);
        mainPanel.add(buttonPanel);
        iconLabel.setBounds(0, 0, 380, 280);
        buttonPanel.setBounds(0, 280, 380, 50);

        f.getContentPane().add(mainPanel, BorderLayout.CENTER);
        f.setSize(new Dimension(390, 370));
        f.setVisible(true);

        cTimer = new Timer(20, new clientTimerListener());
        cTimer.setInitialDelay(0);
        cTimer.setCoalesce(true);
    }

    // ------------------------------------
    // Button handlers
    // ------------------------------------

    class playButtonListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            // System.out.println("Play Button pressed !");
            cTimer.start();
        }
    }

    class tearButtonListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            // System.out.println("Teardown Button pressed !");
            cTimer.stop();
            System.exit(0);
        }
    }

    // ------------------------------------
    // Timer handler
    // ------------------------------------

    class clientTimerListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            // get an Image object from the payload bitstream
            VideoFrame x = fps.get(fps.size() - 1);
            Toolkit toolkit = Toolkit.getDefaultToolkit();
            Image image = toolkit.createImage(x.data(), 0, x.data().length);

            // display the image as an ImageIcon object
            icon = new ImageIcon(image);
            iconLabel.setIcon(icon);
        }
    }
}