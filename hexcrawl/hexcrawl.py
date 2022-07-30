#!/usr/bin/env python3

import curses
import random

INFO_COLUMNS = 40
LEGEND_ROWS = 8
LEGEND_COLUMNS = INFO_COLUMNS
MIN_SCREEN_ROWS = 18
MIN_SCREEN_COLUMNS = 67


class Hex:

    def __init__(self, tui, row, column, rows=5):
        self.tui = tui
        self.row = row
        self.column = column
        self.rows = rows
        self.columns = rows * 2 - 1
        self.name = f"{column},{row}"

        rand = random.randint(1, 6)
        if rand <= 3:
            self.terrain = "F"
            self.color = GREEN
        elif rand == 4 or rand == 5:
            self.terrain = "p"
            self.color = YELLOW
        elif rand == 6:
            self.terrain = "~"
            self.color = BLUE

    def draw(self, scr, row=None, column=None, border_color=0):

        if border_color == 0:
            border_color = WHITE

        if row is None:
            row = self.row

        if column is None:
            column = self.column

        if column % 2 == 0:
            row_offset = 0
        else:
            row_offset = 2

        row = row * 4 + row_offset
        column = column * 8 + 1

        # First (top) row_off
        scr.addstr(row, column + 1, "+-----+", border_color)
        middle = (self.columns - 1) // 2
        scr.addstr(row, column + middle, ",", WHITE)
        x_str = str(self.column + 1)
        x_str_len = len(x_str)
        scr.addstr(row, column + middle - x_str_len, x_str, CYAN)
        scr.addstr(row, column + middle + 1, str(self.row + 1), CYAN)

        # Second row
        scr.addstr(row + 1, column, "/", border_color)
        scr.addstr(row + 1, column + 1, self.terrain * 7, self.color)
        scr.addstr(row + 1, column + 8, "\\", border_color)
        # Third (middle) row
        scr.addstr(row + 2, column - 1, "+", border_color)
        scr.addstr(row + 2, column, self.terrain * 9, self.color)
        scr.addstr(row + 2, column + 9, "+", border_color)
        if random.randint(1, 10) == 1 and self.terrain != "~":
            scr.addstr(row + 2, column + 4, "#", WHITE)
        # Fourth row
        scr.addstr(row + 3, column, "\\", border_color)
        scr.addstr(row + 3, column + 1, self.terrain * 7, self.color)

        scr.addstr(row + 3, column + 8, "/", border_color)
        # Fifth row
        scr.addstr(row + 4, column + 1, "+-----+", border_color)


class TUI:

    def __init__(self, scr, rows=20, columns=30):
        self.scr = scr
        self.rows = rows
        self.columns = columns
        self.data = {}
        self.data["selected_hex"] = None
        self.setup(rows, columns)

    def setup(self, rows=0, columns=0):
        self.verify_screen_size()
        if rows == 0:
            rows = self.rows
        if columns == 0:
            columns = self.columns
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
        self.print(f"Screen size is {self.screen_rows} lines by "
                   f"{self.screen_columns} columns.")
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
        try:
            # If the pad already exists, then we got here because we're
            # resizing the screen. That requires explicit resizing of the
            # pad - at least, it doesn't work for me to just recreate it.
            if self.pad:
                self.pad.resize(self.pad_rows, self.pad_columns)
        except AttributeError:
            # self.pad doesn't exist, so this is the first time we've
            # run this function - create the pad.
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

    def get_adjacent_hexes(self, row, column):
        hexes = []

        for direction in ["up", "up_right", "down_right",
                          "down", "down_left", "up_left"]:
            hex = self.get_adjacent_hex(row, column, direction)
            if hex:
                hexes.append(hex)

        return hexes

    def get_adjacent_hex(self, row, column, direction):
        row_mod = 0
        column_mod = 0

        if column % 2 != 0:
            side_mod = 0
        else:
            side_mod = -1

        if direction == "up":
            row_mod = -1
        elif direction == "up_right":
            row_mod = side_mod
            column_mod = 1
        elif direction == "down_right":
            row_mod = side_mod + 1
            column_mod = 1
        elif direction == "down":
            row_mod = 1
        elif direction == "down_left":
            row_mod = side_mod + 1
            column_mod = -1
        elif direction == "up_left":
            row_mod = side_mod
            column_mod = -1
        else:
            self.print(f"get_adjacent_hex: illegal direction: {direction}")

        try:
            return self.hex[row + row_mod][column + column_mod]
        except IndexError:
            return None

    def draw(self):
        row = 0
        column = 0
        while row < self.rows:
            column = 0
            while column < self.columns:
                self.hex[row][column].draw(self.pad, row, column)
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
            elif key == curses.KEY_RESIZE:
                self.verify_screen_size()
                self.scr.clear()
                self.setup()
                self.scr.refresh()
                self.print("Screen has been resized.")
            elif key == ord("u"):
                self.unselect_hex()

            self.normalize_pos()

    def verify_screen_size(self):
        rows, columns = self.scr.getmaxyx()
        while rows < MIN_SCREEN_ROWS or columns < MIN_SCREEN_COLUMNS:
            self.scr.clear()
            if rows < MIN_SCREEN_ROWS:
                self.scr.addstr("Terminal is not tall enough. "
                                "Make it taller.\n")
            if columns < MIN_SCREEN_COLUMNS:
                self.scr.addstr("Terminal is too narrow. "
                                "Make it wider.\n")

            self.scr.getch()
            rows, columns = self.scr.getmaxyx()

    def select_hex(self, row, column):
        self.unselect_hex()

        selected_hex = self.hex[row][column]

        adjacent_hexes = self.get_adjacent_hexes(row, column)
        for hex in adjacent_hexes:
            hex.draw(self.pad, border_color=BLUE)

        selected_hex.draw(self.pad, border_color=MAGENTA)

        self.data["selected_hex"] = selected_hex

    def unselect_hex(self):
        unselected_hex = self.data["selected_hex"]
        self.data["selected_hex"] = None
        if not unselected_hex:
            return
        unselected_hex.draw(self.pad)  # Draw with default border_color = unselected.

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
    ui.select_hex(19, 29)
    ui.main_loop()
    # stdscr.refresh()


curses.wrapper(main)
