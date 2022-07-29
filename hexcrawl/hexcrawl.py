#!/usr/bin/env python3

import curses
import random

INFO_COLUMNS = 40
LEGEND_ROWS = 8
LEGEND_COLUMNS = INFO_COLUMNS


class Hex:

    def __init__(self, tui, row, column, rows=5):
        self.tui = tui
        self.row = row
        self.column = column
        self.rows = rows
        self.columns = rows * 2 - 1

        rand = random.randint(1, 6)
        if rand <= 3:
            self.terrain = "F"
            self.color = GREEN
        elif rand == 4 or rand == 5:
            self.terrain = "."
            self.color = YELLOW
        elif rand == 6:
            self.terrain = "~"
            self.color = BLUE

    def draw(self, scr, row, col):

        # First (top) row_off
        scr.addstr(row, col + 1, "+-----+")
        middle = (self.columns - 1) // 2
        scr.addstr(row, col + middle, ",", WHITE)
        x_str = str(self.column + 1)
        x_str_len = len(x_str)
        scr.addstr(row, col + middle - x_str_len, x_str, CYAN)
        scr.addstr(row, col + middle + 1, str(self.row + 1), CYAN)

        # Second row
        scr.addstr(row + 1, col, "/", WHITE)
        scr.addstr(row + 1, col + 1, self.terrain * 7, self.color)
        scr.addstr(row + 1, col + 8, "\\", WHITE)
        # Third (middle) row
        scr.addstr(row + 2, col - 1, "+", WHITE)
        scr.addstr(row + 2, col, self.terrain * 9, self.color)
        scr.addstr(row + 2, col + 9, "+", WHITE)
        if random.randint(1, 10) == 1 and self.terrain != "~":
            scr.addstr(row + 2, col + 4, "#", WHITE)
        # Fourth row
        scr.addstr(row + 3, col, "\\", WHITE)
        scr.addstr(row + 3, col + 1, self.terrain * 7, self.color)

        scr.addstr(row + 3, col + 8, "/", WHITE)
        # Fifth row
        scr.addstr(row + 4, col + 1, "+-----+")


class TUI:
    def __init__(self, scr, rows=20, columns=30):
        self.scr = scr
        self.rows = rows
        self.columns = columns
        self.printed_before = False
        self.scr.clear()
        self.setup_screen_size()
        self.setup_pad(rows, columns, self.screen_rows - 1,
                       self.screen_columns - 40 - 1)
        info_rows = self.screen_rows - LEGEND_ROWS
        self.setup_info(info_rows, 40)
        self.setup_legend(LEGEND_ROWS, LEGEND_COLUMNS)
        self.setup_dividers()
        self.setup_hexes()
        self.print("1234567890" * 4)
        self.print("Welcome to Hexcrawl!")
        self.print("Setup complete.")
        self.print(f"Pad is {self.pad_display_columns} characters wide.")
        self.legend.addstr("Use arrow keys to scroll the map.")
        self.legend.refresh()

        # for i in range(50):
        #     self.print(str(i))

    def setup_screen_size(self):
        self.screen_rows, self.screen_columns = self.scr.getmaxyx()
        self.row_pos = 0
        self.column_pos = 0

    def setup_pad(self, rows, columns, display_rows, display_columns):
        self.pad_rows = rows * 4 + 3
        self.pad_columns = columns * 8 + 3
        self.pad_display_rows = display_rows
        self.pad_display_columns = display_columns
        self.pad = curses.newpad(self.pad_rows, self.pad_columns)
        self.pad.keypad(True)

    def setup_info(self, rows, columns):
        self.info_rows = rows
        self.info_columns = columns
        self.info = curses.newwin(self.info_rows - 2, self.info_columns,
                                  1,
                                  self.screen_columns - self.info_columns)
        self.info.scrollok(True)

    def setup_legend(self, rows, columns):
        self.legend_rows = rows
        self.legend_columns = columns
        self.legend = curses.newwin(rows, columns,
                                    self.screen_rows - rows,
                                    self.screen_columns - self.info_columns)

    def setup_dividers(self):
        # Vertical line
        for row in range(self.screen_rows):
            self.scr.addstr(row, self.pad_display_columns, "|", MAGENTA)

        # Top of screen line
        for column in range(0, self.screen_columns):
            self.scr.addstr(0, column, "-", MAGENTA)

        # Legend line
        for column in range(self.pad_display_columns + 1,
                            self.screen_columns):
            self.scr.addstr(self.info_rows - 1, column, "-", MAGENTA)

        # World heading
        title_column = self.pad_display_columns // 2 - 3
        self.scr.addstr(0, title_column, "World", GREEN)
        self.scr.addstr(0, title_column - 2, "[ ", MAGENTA)
        self.scr.addstr(0, title_column + 5, " ]", MAGENTA)

        # Info heading
        title_column = self.screen_columns - self.info_columns // 2 - 2
        self.scr.addstr(0, title_column, "Info", GREEN)
        self.scr.addstr(0, title_column - 2, "[ ", MAGENTA)
        self.scr.addstr(0, title_column + 4, " ]", MAGENTA)

        # Legend heading
        self.scr.addstr(self.info_rows - 1, self.pad_display_columns + 17,
                        " Legend ", GREEN)
        self.scr.addstr(self.info_rows - 1, self.pad_display_columns + 16,
                        "[", MAGENTA)
        self.scr.addstr(self.info_rows - 1, self.pad_display_columns + 25,
                        "]", MAGENTA)

        # Pluses at intersections
        self.scr.addstr(0, self.pad_display_columns, "+", MAGENTA)
        self.scr.addstr(self.info_rows - 1, self.pad_display_columns, "+",
                        MAGENTA)
        self.scr.refresh()

    def setup_hexes(self):
        self.hex = []
        row = 0

        while row < self.rows:
            hex_row = []
            column = 0
            while column < self.columns:
                hex_row.append(Hex(self, row, column))
                column += 1
            self.hex.append(hex_row)
            row += 1

    def draw(self):
        row = 0
        column = 0
        while row < self.rows:
            column = 0
            while column < self.columns:
                if column % 2 == 0:
                    row_offset = 0
                else:
                    row_offset = 2
                self.hex[row][column].draw(self.pad, (row * (5-1)) +
                                           row_offset, column * (9-1) + 1)
                column += 1
            row += 1

    def normalize_pos(self):
        if self.column_pos < 0:
            self.column_pos = 0
        elif self.column_pos > self.pad_columns - self.pad_display_columns:
            self.column_pos = self.pad_columns - self.pad_display_columns
        if self.row_pos < 0:
            self.row_pos = 0
        elif self.row_pos > self.pad_rows - self.pad_display_rows:
            self.row_pos = self.pad_rows - self.pad_display_rows

    def main_loop(self):
        while True:
            self.pad.refresh(self.row_pos, self.column_pos, 1, 0,
                             self.screen_rows - 1, self.screen_columns -
                             self.info_columns - 2)

            key = self.pad.getch()

            if key == curses.KEY_LEFT:
                self.column_pos -= 2
            elif key == curses.KEY_RIGHT:
                self.column_pos += 2
            elif key == curses.KEY_DOWN:
                self.row_pos += 1
            elif key == curses.KEY_UP:
                self.row_pos -= 1
            elif key == ord('q'):
                return True

            self.normalize_pos()

    def print(self, text):
        if self.printed_before:
            text = "\n" + text
        self.info.addstr(text)
        self.info.refresh()
        if len(text) % self.info_columns != 0:
            self.printed_before = True


def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE,  curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN,  curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_CYAN, curses.COLOR_BLUE)

    global WHITE
    global BLUE
    global CYAN
    global GREEN
    global YELLOW
    global MAGENTA
    global RED
    global CYAN_BLUE

    WHITE = curses.color_pair(1)
    BLUE = curses.color_pair(2)
    CYAN = curses.color_pair(3)
    GREEN = curses.color_pair(4)
    YELLOW = curses.color_pair(5)
    MAGENTA = curses.color_pair(6)
    RED = curses.color_pair(7)
    CYAN_BLUE = curses.color_pair(9)

    ui = TUI(stdscr)
    ui.draw()
    ui.main_loop()
    stdscr.refresh()


curses.wrapper(main)
