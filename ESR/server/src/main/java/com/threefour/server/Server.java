package com.threefour.server;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.stream.Collectors;

import com.beust.jcommander.JCommander;
import com.beust.jcommander.ParameterException;
import com.google.common.collect.ArrayListMultimap;
import com.google.common.collect.Multimap;
import com.threefour.Constants;
import com.threefour.intermediator.worker.Listener;
import com.threefour.intermediator.worker.PulseChecker;
import com.threefour.intermediator.worker.PulseSender;
import com.threefour.overlay.ServerNode;
import com.threefour.server.worker.Announcer;
import com.threefour.server.worker.Streamer;
import com.threefour.util.Args;
import com.threefour.util.Print;

import org.yaml.snakeyaml.Yaml;

public class Server {

    public static void main(String[] argv) {

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

        Print.printInfo("Running server...");

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

        // open socket
        try (DatagramSocket socket = new DatagramSocket(Constants.PORT)) {

            ServerNode node = new ServerNode(socket, ns);

            // launch thread to send periodic heartbeats
            new Thread(new PulseSender(node)).start();

            // launch thread to manage node' pulses
            new Thread(new PulseChecker(node)).start();

            // launch thread to listen to messages
            new Thread(new Listener(node)).start();

            // launch thread to send periodic info
            new Thread(new Announcer(node)).start();

            // send frames
            new Streamer(node, args.video).run();

        } catch (SocketException e) {
            Print.printError("Socket error: " + e.getMessage());
            return;
        }

    }

}