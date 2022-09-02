package com.threefour.util;

import java.util.ArrayList;
import java.util.List;

import com.beust.jcommander.Parameter;

public class Args {

    @Parameter(names = { "-f", "--file" }, description = "File where the neighbours are described", required = true)
    public String neighboursFile;

    @Parameter(names = { "-n", "--neighbour" }, description = "Neighbour host name", required = true)
    public List<String> neighbours = new ArrayList<>();

    @Parameter(names = { "-v", "--video" }, description = "Video to be sent (only applicable to the server)")
    public String video = "movie.Mjpeg";

    @Parameter(names = { "-h", "--help" }, description = "Shows this message", help = true)
    public boolean help;

}