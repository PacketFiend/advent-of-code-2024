#!/usr/bin/python3
from pprint import pprint
import sys

test_case_1 = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
10: 2 5 1
10: 2 5 6
""".strip().split('\n')

with open("day07-input", "r") as file:
    input_data = file.readlines()

calibration_data = []
for line in input_data:
    calibration_data.append(line.strip())


def find_combinations(original, index, ops_combos):
    if index == len(original):
        ops_combos.append(original)
        return ops_combos

    # Only replace if this is a placeholder character (i.e. not already replaced)
    if original[index] == "#":
        # Replace the character at the index with our new operator, and do it again
        for operator in mathematical_operators:
            original = original[:index] + operator + original[index+1:]
            find_combinations(original, index+1, ops_combos)
    else:
        # If it's not a placeholder, just move on to the next char
        find_combinations(original, index+1, ops_combos)

    return ops_combos


# This gets redefined later. A bit confusing...
mathematical_operators = [
    "+",
    # "-",
    # "/",
    "*",
]

lines_to_test = []
#for line in test_case_1:
for line in calibration_data:
    result = line.split(": ")[0]
    operands = line.split(": ")[1]
    num_ops = len(operands.split())-1
    result = int(result)
    operands = list(map(int, operands.split()))
    ops_combos = find_combinations("#"*num_ops, 0, [])
    lines_to_test.append((result, operands, ops_combos))

print("Total lines to test: {}".format(len(lines_to_test)))
true_equations = []

for result, operands, ops_combos in lines_to_test:
    result_tally = 0
    for i, operation in enumerate(ops_combos):
        equation_string = ""
        for j, operator in enumerate(operation):
            if j == 0:
                result_tally = operands[j]
                equation_string = str(operands[j])
            if operator == "+":
                result_tally += operands[j+1]
                equation_string = f"{equation_string} {operator} {operands[j+1]}"
            elif operator == "*":
                result_tally *= operands[j+1]
                equation_string = f"{equation_string} {operator} {operands[j+1]}"
        if result_tally == result:
            equation_string = f"{equation_string} = {result_tally}"
            true_equations.append((result_tally, equation_string, " ".join(map(str, operands))))
            break
print("Total matching results: {}".format(len(true_equations)))

results_to_add = [result[0] for result in true_equations]
print("Total results to add: {}".format(len(results_to_add)))

total = sum(result[0] for result in true_equations)
print("Sum of all possible true equations is {}".format(total))
