#!/usr/bin/python3

import os
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
import time
import os
from pprint import pprint
import sys
import random


def get_terminal_size():
    size = os.get_terminal_size()
    rows = size.lines - 2 # Allow room for info bars
    cols = size.columns - 2
    return rows, cols


class Guard:
    total_movements = 0
    occupied_positions = []
    initial_position = ()
    position = (0, 0)
    repr = "X"
    direction = "N"
    obstructions = {"#", "O"}
    direction_deltas = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

    def __init__(self, layout, initial_position):
        self.lab = lab
        self.position = initial_position
        self.initial_position = initial_position
        self.layout = layout
        self.previous_states = set()
        self.occupied_positions = set()
        self.repr = ">"


    def reset(self, lab):
        self.position = self.initial_position
        self.total_movements = 0
        self.previous_states = set()
        self.direction = "N"
        self.occupied_positions = set()
        lab.change_guard_position(self.initial_position)

    def next(self):
        y, x = self.position
        if self.direction == "N":
            if y == 0:
                return "X"
            else:
                return self.lab.layout[y-1][x]
        elif self.direction == "E":
            if x == len(self.layout[0])-1:
                return "X"
            else:
                return self.lab.layout[y][x+1]
        elif self.direction == "S":
            if y == len(self.layout)-1:
                return "X"
            else:
                return self.lab.layout[y+1][x]
        elif self.direction == "W":
            if x == 0:
                return "X"
            else:
                return self.lab.layout[y][x-1]

    def turn(self):
        if self.direction == "N":
            self.direction = "E"
            self.repr = ">"
        elif self.direction == "E":
            self.direction = "S"
            self.repr = "v"
        elif self.direction == "S":
            self.direction = "W"
            self.repr = "<"
        elif self.direction == "W":
            self.direction = "N"
            self.repr = "^"

    def move(self):
        loopy = False
        exited = False
        # Check if we've left the lab
        if self.next() == "X":
            exited = True
        else:
            # Check if there's a column where the guard would next move to. If there is, then turn right.
            if self.next() in self.obstructions:
                self.turn()
            else:
                delta_y, delta_x = self.direction_deltas[self.direction]
                y, x = self.position
                self.position = (y+delta_y, x+delta_x)
                self.total_movements += 1
                if (self.position, self.direction) in self.previous_states:
                    # We found a loop
                    loopy = True
                else:
                    self.occupied_positions.add(self.position)
                    self.previous_states.add((self.position, self.direction))
        return self.position, exited, loopy


class Lab():
    layout = []
    viewport = []
    initial_guard_position = ()

    def __init__(self, lab):
        self.layout = []
        self.guard_position = (0, 0)
        for y, line in enumerate(lab):
            if "^" in line:
                # This is the guard's initial position
                self.guard_position = (y, line.index("^"))
                line = line.replace("^", ".")
            elif "O" in line:
                self.obstruction = (y, line.index("O"))
            self.layout.append(line)
        self.initial_guard_position = self.guard_position

    def change_guard_position(self, position):
        self.guard_position = position

    def show_lab(self, viewport_size, infobar):
        y, x = self.guard_position
        print(infobar)
        table = Table(show_header=False, box=None)
        self.viewport = self.get_viewport(viewport_size)
        for row in self.viewport:
            table.add_row("".join(row))
        return table

    def print_lab(self):
        for i, y in enumerate(lab.layout):
            if "O" in y:
                y = y.replace("O", "\033[33m" + "O" + "\033[0m")
            print(f"{i}: ", y)

    def get_viewport(self, viewport_size, obstruction=None):
        rows, cols = viewport_size
        row, col = self.guard_position
        lab_rows = len(self.layout)
        lab_cols = len(self.layout[0])

        top = max(0, row - rows//2)
        bottom = min(lab_rows, row+(rows//2)+1)
        left = max(0, col - cols//2)
        right = min(lab_cols, col+cols+1)

        viewport = [list(row[left:right]) for row in self.layout[top:bottom]]
        viewport_guard_y = row-top
        viewport_guard_x = col-left
        viewport[viewport_guard_y][viewport_guard_x] = "[bold red]" + guard.repr + "[/bold red]"
        for y, line in enumerate(viewport):
            if "O" in line:
                x = line.index("O")
                line[x] = "[bold yellow]" + "O" + "[/bold yellow]"

        return viewport


def walk_lab(lab, guard, visual, print_lab, obstruction=None, delay=0):

    exited = False
    wait_time = delay
    if print_lab:
        lab.print_lab()

    if visual:
        with Live(console=console, refresh_per_second=10000) as live:
            loopy = False
            while not exited and not loopy:
                time.sleep(wait_time)
                if obstruction is not None:
                    obstruction_pos_y, obstruction_pos_x = obstruction
                    guard_pos_y, guard_pos_x = guard.position
                    if -5 < guard_pos_y-obstruction_pos_y < 5 and -5 < guard_pos_x-obstruction_pos_x < 5:
                        wait_time = 0.5
                    else:
                        wait_time = delay
                lab.guard_position, exited, loopy = guard.move()
                viewport_size = get_terminal_size()
                infobar = Text(f"Viewport size: {viewport_size} | Direction: {guard.direction} | Position: {guard.position}"
                               f" | Total movements: {guard.total_movements}"
                               f" | Occupied positions: {len(guard.occupied_positions)}"
                               f" | Next: {guard.next()}")
                live.update(lab.show_lab(viewport_size, infobar))
    else:
        loopy = False
        while not exited and not loopy:
            lab.guard_position, exited, loopy = guard.move()

    return guard.total_movements, guard.occupied_positions, loopy


console = Console()
initial_layout = []
loopy_obstructions = []

with open("day06-input", "r") as file:
    data = file.readlines()
    for line in data:
        initial_layout.append(line.strip())

test_case_1 = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip().split("\n")

test_case_2 = """
.#................
..#...............
..................
.^................
..................
""".strip().split("\n")

# Test cases
lab = Lab(test_case_1)
guard = Guard(lab.layout, lab.guard_position)
for y in range(len(lab.layout)):
    for x in range(len(lab.layout[0])):
        lab = Lab(test_case_1)
        guard.reset(lab)
        guard.lab.layout = lab.layout
        lab.layout[y] = lab.layout[y][:x] + "O" + lab.layout[y][x+1:]
        total_movements, occupied_positions, loopy = walk_lab(lab, guard, False, False, None, 0.1)
        if loopy:
            loopy_obstructions.append((y, x))
assert len(loopy_obstructions) == 6

lab = Lab(test_case_2)
guard = Guard(lab.layout, lab.guard_position)
guard.reset(lab)
guard.lab.layout = lab.layout
total_movements, occupied_positions, loopy = walk_lab(lab, guard, True, False, None, 1.0)
assert len(occupied_positions) == 4

# PART 1
lab = Lab(initial_layout)
guard = Guard(lab.layout, lab.guard_position)
guard.reset(lab)
guard.lab.layout = lab.layout
walk_lab(lab, guard, False, False)
print("Total occupied positions: {}".format(len(guard.occupied_positions)))
print("Total movements: {}".format(guard.total_movements))

# PART 2
lab = Lab(initial_layout)
guard = Guard(lab.layout, lab.guard_position)
guard.reset(lab)
guard.lab.layout = lab.layout
loopy_obstructions = []
random_x = None
random_y = None
for y in range(len(lab.layout)):
    print("Walking lab with new obstructions along row {}".format(y))
    for x in range(len(lab.layout[0])):
        obstruction = (y, x)
        lab = Lab(initial_layout)
        guard.reset(lab)
        if lab.layout[y][x] != "#" and (y, x) != guard.position:
            # print("Walking lab with obstacle at ({},{})".format(y, x))
            lab.layout[y] = lab.layout[y][:x] + "O" + lab.layout[y][x+1:]   # Silly immutable strings...
            guard.lab.layout = lab.layout
            total_movements, occupied_positions, loopy = walk_lab(lab, guard, False, False, obstruction, 0)
            if loopy:
                loopy_obstructions.append((y, x))
                print("Found a loop with new obstruction at {}!".format(obstruction))

print("Number of obstruction positions that would cause the Gallivant to go loopy: {}".format(len(loopy_obstructions)))
print("THE END.")
