#!/usr/bin/python3
from pprint import pprint
import sys

def in_grid(x, y):
    # Checks if the position we're checking is within the grid boundaries
    return 0 <= x < num_rows and 0 <= y < num_cols


def search(x, y, dx, dy, target):
    # Search for XMAS from starting position of (x,y) in direction (dx,dy)
    # We assume that if the loop completes successfully, a match was found
    positions = []
    for k in range(4):
        nx, ny = x+(k*dx), y+(k*dy)
        if not in_grid(nx, ny):
            return False, []
        if grid[nx][ny] != target[k]:
            return False, []
        positions.append((nx, ny))
    return True, positions


def colourize():
    matches = []
    total_matches = 0
    for i in range(num_rows):
        for j in range(num_cols):
            for dx, dy in directions:
                found, positions = search(i, j, dx, dy, "XMAS")
                if found:
                    matches.append((positions, "red"))
                    total_matches += 1
                found_reversed, position_reversed = search(i, j, dx, dy, "SAMX")
                if found_reversed:
                    matches.append((position_reversed, "white"))
                    total_matches += 1
    return matches, total_matches


def print_coloured_grid(grid, matches):
    num_rows, num_cols = len(grid), len(grid[0])
    coloured_grid = [list(row) for row in grid]

    for positions, colour in matches:
        ansi_colour = "\033[31m" if colour == "red" else "\033[37m"
        for x, y in positions:
            coloured_grid[x][y] = ansi_colour + grid[x][y] + "\033[0m"

    for row in coloured_grid:
        print("".join(row))


def print_coloured_x_matches(grid, x_pattern_matches):
    num_rows, num_cols = len(grid), len(grid[0])
    coloured_grid = [list(row) for row in grid]

    for match in x_pattern_matches:
        x, y = match
        positions = [
            (x-1, y-1),
            (x+1, y-1),
            (x, y),
            (x-1, y+1),
            (x+1, y+1)
        ]
        for px, py in positions:
            coloured_grid[px][py] = "\033[31m" + grid[px][py] + "\033[0m"

    for row in coloured_grid:
        print("".join(row))


def search_x_pattern(x, y, pattern_reductions):
    # Searches a given 3x3 grid for an X pattern formed by "MAS"
    # Used for part 2 X-MAS search

    positions = [
        (x-1, y-1),
        (x+1, y-1),
        (x, y),
        (x-1, y+1),
        (x+1, y+1)
    ]

    for nx, ny in positions:
        if not (0 <= nx < num_rows and 0 <= ny < num_cols):
            return False, []

    # Reduces the X pattern to a list, top to bottom and left to right. For example:
    # M . S
    # . A .
    # M . S
    # Becomes ["M", "S", "A", "M", "S"]
    # This needs to be matched against all possible reductions of the X pattern.

    word_pattern = [grid[y-1][x-1], grid[y-1][x+1], grid[y][x], grid[y+1][x-1], grid[y+1][x+1]]
    for pattern_reduction in pattern_reductions:
        # print("Word pattern: {}".format(word_pattern))
        # print("Pattern reduction: {}".format(list(pattern_reduction)))
        if word_pattern == list(pattern_reduction):
            # print("Match! {} equals {}".format("".join(word_pattern), pattern_reduction))
            return True, (y, x)
    # If we've finished the previous loop, no match was found
    return False, ()


def get_subsets():
    # Wrapper function to run search_x_pattern from all possible centre coordinates
    # Collects centre positions of all matching patterns and returns them for later highlighting
    matches = []
    pattern_reductions = [
        "MSAMS",
        "MMASS",
        "SMASM",
        "SSAMM",
    ]
    for i in range(1, num_rows-1):
        for j in range(1, num_cols-1):
            found, position = search_x_pattern(i, j, pattern_reductions)
            if found:
                matches.append(position)
    return matches


with open("day04-input", "r") as file:
    grid = [line.strip() for line in file.readlines()]
    word_length = 4
    # Used for part 1 word search
    directions = [
        (0, 1),     # Horizontal E
        #(0, -1),    # Horizontal W
        (1, 0),     # Vertical S
        #(-1, 0),    # Vertical N
        (1, 1),     # Diagonal SE
        #(1, -1),    # Diagonal SW
        (-1, 1),    # Diagonal NE
        #(-1, -1)    # Diagonal NW
    ]
num_rows, num_cols = len(grid), len(grid[0])
occurrences = []
for i in range(num_rows):
    for j in range(num_cols):
        for dx, dy in directions:
            if search(i, j, dx, dy, "XMAS"): # or search(i, j, dx, dy, "SAMX"):
                occurrences.append((i, j))

matches, total_matches = colourize()
print_coloured_grid(grid, matches)
print("Total XMAS matches: {}".format(total_matches))

new_matches = get_subsets()
print_coloured_x_matches(grid, new_matches)
print("Total X-MAS matches: {}".format(len(new_matches)))
