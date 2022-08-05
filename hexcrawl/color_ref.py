#!/usr/bin/env python3

import curses


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    stdscr.scrollok(True)
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    for i in range(1, 17):
        stdscr.addstr(f"{i:>4}", curses.color_pair(i))
    stdscr.addstr("\n")

    for row in range(0, 20):
        for column in range(0, 12):
            num = row * 12 + column + 17
            # stdscr.addstr(f"row: {row}, block: {block}, i: {i}\n")
            stdscr.addstr(f"{str(num):>4}", curses.color_pair(num))
            # stdscr.addstr(str(num) + "\n")
        stdscr.addstr("\n")

    stdscr.getch()


curses.wrapper(main)
