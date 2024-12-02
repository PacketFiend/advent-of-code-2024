#!/usr/bin/python3
import numpy as np

def check_report(report):

    direction = None
    for i in range(report.size - 1):
        report_is_safe = True
        current_level = int(report[i])
        next_level = int(report[i+1])
        difference = next_level - current_level
        if difference > 0:
            current_direction = "increasing"
        elif difference < 0:
            current_direction = "decreasing"
        else:
            current_direction = "stagnant"
            report_is_safe = False
            break
        if direction is not None:
            if direction != current_direction:
                report_is_safe = False
                break
        direction = current_direction

        if not 1 <= abs(difference) <= 3:
            report_is_safe = False
            break
    return report_is_safe

reports = []

with open('day02-input', 'r') as data:
    safe_levels = 0
    for line in data:
        elements = line.strip().split()
        reports.append(np.array(elements, dtype=int))

for report in reports:
    safe = check_report(report)
    if safe:
        safe_levels += 1
    else:
        for i, level in enumerate(report):
            new_report = np.delete(report, i)
            safe = check_report(new_report)
            if safe:
                safe_levels += 1
                break
print("Total safe levels: {}".format(safe_levels))
