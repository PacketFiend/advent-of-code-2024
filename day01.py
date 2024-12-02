#!/usr/bin/python3

import numpy as np
data = np.genfromtxt('day01-input', delimiter=r'   ')

col1 = data[:, 0]
col2 = data[:, 1]

col1 = np.sort(col1)
col2 = np.sort(col2)
total_difference = 0

for row1,row2 in zip(col1,col2):
    difference = abs(row1-row2)
    total_difference += difference

print("Total difference: {}".format(total_difference))

total_similarity = 0
for row in col1:
    occurrences = np.count_nonzero(col2 == row)
    similarity = row * occurrences
    total_similarity += similarity

print("Total similarity: {}".format(total_similarity))