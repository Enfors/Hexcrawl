#!/usr/bin/env python3

import curses
import random


class Hex:

    def __init__(self, map, row, column, rows=5):
        self.map = map
        self.row = row
        self.column = column
        self.rows = rows
        self.columns = rows * 2 - 1

        rand = random.randint(0, 2)
        if rand == 0:
            self.terrain = "F"
            self.color = GREEN
        elif rand == 1:
            self.terrain = "."
            self.color = YELLOW
        elif rand == 2:
            self.terrain = "~"
            self.color = CYAN

    def draw(self, scr, row, col):

        # First (top) row_off
        scr.addstr(row, col + 1, "+-----+")
        middle = (self.columns - 1) // 2
        scr.addstr(row, col + middle, ",", WHITE)
        x_str = str(self.column + 1)
        x_str_len = len(x_str)
        scr.addstr(row, col + middle - x_str_len, x_str, BLUE)
        scr.addstr(row, col + middle + 1, str(self.row + 1), BLUE)

        # Second row
        scr.addstr(row + 1, col, "/", WHITE)
        scr.addstr(row + 1, col + 1, self.terrain * 7, self.color)
        scr.addstr(row + 1, col + 8, "\\", WHITE)
        # Third (middle) row
        scr.addstr(row + 2, col - 1, "+", WHITE)
        scr.addstr(row + 2, col, self.terrain * 9, self.color)
        scr.addstr(row + 2, col + 9, "+", WHITE)
        # Fourth row
        scr.addstr(row + 3, col, "\\", WHITE)
        scr.addstr(row + 3, col + 1, self.terrain * 7, self.color)

        scr.addstr(row + 3, col + 8, "/", WHITE)
        # Fifth row
        scr.addstr(row + 4, col + 1, "+-----+")


class Map:
    def __init__(self, scr, rows=5, columns=5):
        self.rows = rows
        self.columns = columns
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

    def draw(self, scr):
        row = 0
        column = 0

        while row < self.rows:
            column = 0
            while column < self.columns:
                if column % 2 == 0:
                    row_offset = 0
                else:
                    row_offset = 2
                self.hex[row][column].draw(scr, (row * (5-1)) + row_offset,
                                           column * (9-1) + 1)
                column += 1
            row += 1


def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE,  curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN,  curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_CYAN, curses.COLOR_BLUE)

    global WHITE
    global BLUE
    global CYAN
    global GREEN
    global YELLOW
    global MAGENTA
    global CYAN_BLUE

    WHITE = curses.color_pair(1)
    BLUE = curses.color_pair(2)
    CYAN = curses.color_pair(3)
    GREEN = curses.color_pair(4)
    YELLOW = curses.color_pair(5)
    MAGENTA = curses.color_pair(6)
    CYAN_BLUE = curses.color_pair(9)

    stdscr.clear()
    map = Map(stdscr, 10, 21)
    map.draw(stdscr)
    stdscr.refresh()
    stdscr.getch()


curses.wrapper(main)
