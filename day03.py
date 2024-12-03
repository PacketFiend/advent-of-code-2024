#!/usr/bin/python3
import re

with open("day03-input") as file:
    data = file.read()

pattern = r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)'
matches = re.findall(pattern, data)

pattern = r'\d{1,3}'
total = 0
total_with_do = 0
adding = True
for match in matches:
    if match == "do()":
        adding = True
    elif match == "don't()":
        adding = False
    else:
        multiplicands = re.findall(pattern, match)
        product = int(multiplicands[0]) * int(multiplicands[1])
        if adding:
            total_with_do += product
        total += product

print("Part 1 solution is {}; part 2 solution is {}".format(total, total_with_do))
