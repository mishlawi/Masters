package com.threefour.client;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.stream.Collectors;
import java.net.UnknownHostException;

import com.beust.jcommander.JCommander;
import com.beust.jcommander.ParameterException;
import com.google.common.collect.ArrayListMultimap;
import com.google.common.collect.Multimap;
import com.threefour.Constants;
import com.threefour.client.worker.ClientListener;
import com.threefour.client.worker.GUI;
import com.threefour.ott.worker.PulseChecker;
import com.threefour.ott.worker.PulseSender;
import com.threefour.overlay.Neighbours;
import com.threefour.util.Args;
import com.threefour.util.Pair;
import com.threefour.util.Print;
import com.threefour.video.VideoFrame;

import org.yaml.snakeyaml.Yaml;

public class Client {

    private static DatagramSocket socket = null;
    private static Map<InetAddress, Pair<Boolean, Long>> neighbors = new HashMap<>();

    // map locks vizinhos

    private static ReadWriteLock nbReadWriteLock = new ReentrantReadWriteLock();
    private static Lock nbWriteLock = nbReadWriteLock.writeLock();
    private static Lock nbReadLock = nbReadWriteLock.readLock();

    public static void main(String[] argv) throws SocketException {

        // parse arguments
        var args = new Args();
        var jc = JCommander.newBuilder().addObject(args).build();
        try {
            jc.parse(argv);
        } catch (ParameterException e) {
            Print.printError(e.getMessage());
            return;
        }

        // print help message, it case the flag was activated
        if (args.help) {
            jc.usage();
            return;
        }

        Print.printInfo("Running OTT...");

        Multimap<String, InetAddress> ns = ArrayListMultimap.create();

        // parse neighbours file
        Yaml yaml = new Yaml();
        try (InputStream is = new FileInputStream(new File(args.neighboursFile))) {
            var list = (ArrayList<LinkedHashMap<String, Object>>) yaml.load(is);

            for (var node : list) {
                var name = (String) node.get("name");

                if (args.neighbours.contains(name)) {
                    var addresses = ((ArrayList<String>) node.get("addresses")).stream()
                            .map(ip -> {
                                try {
                                    return InetAddress.getByName(ip);
                                } catch (UnknownHostException e) {
                                    Print.printError("Problem parsing address " + ip + ": " + e.getMessage());
                                }
                                return null;
                            }).collect(Collectors.toList());
                    ns.putAll(name, addresses);
                }
            }
        } catch (IOException e1) {
            Print.printError("Problem parsing YAML file " + args.neighboursFile + ": " + e1.getMessage());
            return;
        }

        Print.printInfo("Parsed neighbours: " + ns);
        Neighbours neighbours = new Neighbours(ns);
        List<VideoFrame> frame = new ArrayList<>();

        // open socket
        try (DatagramSocket socket = new DatagramSocket(Constants.PORT)) {

            // launch thread to listen to messages
            new Thread(new ClientListener(frame, socket, neighbours)).start();

            // launch thread to send periodic heartbeats
            new Thread(new PulseSender(socket, neighbours)).start();

            // launch graphical interface
            new GUI(frame);

            // launch thread to manage neighbours' pulses
            new Thread(new PulseChecker(neighbours)).run();

        } catch (SocketException e) {
            Print.printError("Socket error: " + e.getMessage());
            return;
        }

    }
}