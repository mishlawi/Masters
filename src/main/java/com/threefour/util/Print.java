package com.threefour.util;

import com.diogonunes.jcolor.AnsiFormat;
import static com.diogonunes.jcolor.Ansi.colorize;
import static com.diogonunes.jcolor.Attribute.*;

public class Print {

    private static AnsiFormat fError = new AnsiFormat(RED_TEXT(), BOLD());
    private static AnsiFormat fInfo = new AnsiFormat(BLUE_TEXT(), BOLD());
    private static AnsiFormat fWarning = new AnsiFormat(YELLOW_TEXT(), BOLD());

    public static void printError(String message) {
        System.err.println("[%s] %s".formatted(colorize("ERROR", fError), message));
    }

    public static void printInfo(String message) {
        System.out.println("[%s] %s".formatted(colorize("INFO", fInfo), message));
    }

    public static void printWarning(String message) {
        System.err.println("[%s] %s".formatted(colorize("WARNING", fWarning), message));
    }

}
