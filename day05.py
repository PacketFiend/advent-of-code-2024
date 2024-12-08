#!/usr/bin/python3
import sys
import math
from pprint import pprint

def evauluate_rule(pages, rule):
    rule0_index = pages.index(rule[0])
    rule1_index = pages.index(rule[1])
    # print("Update: {}; Ruleset: {}".format(update, ruleset))
    # print("Rule 0 index: {}; Rule 1 index: {}".format(rule0_index, rule1_index))
    return rule0_index <= rule1_index
    # if rule0_index <= rule1_index:
    #     # print("Rule is valid")
    #     # print("")
    #     return True
    # else:
    #     # print("Rule is invalid. Page {} appears before page {}".format(rules[1], rules[0]))
    #     # print("")
    #     return False


def evaluate_all_rules(pages, rules):
    # print("Begin evaluate_all_rules()")
    for ruleset in rules:
        # print("Pages:{}\nRules:{}".format(pages,rules))
        rule = ruleset.strip().split("|")
        if rule[0] in pages and rule[1] in pages:
            rule0_index = pages.index(rule[0])
            rule1_index = pages.index(rule[1])
            rule_is_valid = (rule0_index <= rule1_index)
            if not rule_is_valid:
                return False
    return True


def reorder_pages(pages, rules):
    global swaps
    # print("Begin reorder_pages()")
    update_is_valid = False
    new_page_order = pages[:]

    for ruleset in rules:
        rule = ruleset.strip().split("|")
        if rule[0] in pages and rule[1] in pages:
            rule0_index = new_page_order.index(rule[0])
            rule1_index = new_page_order.index(rule[1])
            if rule0_index >= rule1_index:
                # print("Reordering pages {} according to rule {}".format("\t".join(p for p in new_page_order), rule))
                new_page_order[rule0_index],new_page_order[rule1_index] = pages[rule1_index], pages[rule0_index]
                swaps += 1
                # print("Reordered pages:{}".format("\t".join(p for p in new_page_order)))
                # print("")
                update_is_valid = evaluate_all_rules(new_page_order, rules)
                if not update_is_valid:
                    # print("Not valid yet. Recursing...")
                    # print("Sending \t{}".format("\t".join(p for p in new_page_order)))
                    new_page_order = reorder_pages(new_page_order[:], rules)
    # print("Returning \t{}".format("\t".join(p for p in new_page_order)))
    # print("End reorder_pages()")
    return new_page_order

global swaps
swaps = 0
updates, reordered_updates, rules = [], [], []
update_is_valid = True
valid_updates = []
invalid_updates = []
middle_page_number_sum = 0

with open("day05-input", "r") as file:
    data = file.readlines()

for line in data:
    if "|" in line:
        rules.append(line.strip())
    elif "," in line:
        updates.append(line.strip())
    else:
        pprint("Invalid input encountered: {}".format(line))

for update in updates:
    # print("Evaluating {}".format(update))
    pages = update.strip().split(",")
    for ruleset in rules:
        # print("Evaluating rule {}".format(rule))
        rule = ruleset.strip().split("|")
        # print(rule_order)
        if rule[0] in pages and rule[1] in pages:
            update_is_valid = evauluate_rule(pages, rule)
            if not update_is_valid:
                # print("Update {} is invalid, because of rule {}".format(update, rule))
                invalid_updates.append(update)
                break
        else:
            # print(f"Either {rule[0]} or {rule[1]} is not in {update_order}")
            pass
    if update_is_valid:
        # print("{} is a valid update, with {} pages".format(update, len(update_order)))
        valid_updates.append(update)

for update in valid_updates:
    pages = update.strip().split(",")
    middle_index = math.ceil((len(pages)-1)/2.0)
    # print("The middle page in {} is {}".format(update, pages[middle_index]))
    middle_page_number_sum += int(pages[middle_index])
print("The sum of all middle page numbers (from already valid updates) is {}".format(middle_page_number_sum))

# print("There are {} invalid updates to reorder.".format(len(invalid_updates)))
i = 0
for update in invalid_updates:
    i+=1
    update_is_valid = True
    pages = update.strip().split(",")
    # print("Pages: {}".format(pages))
    reordered_pages = pages[:]
    # print("*************NEW UPDATE****************")
    # print("Reordering pages {}".format("\t".join(p for p in pages)))
    reordered_pages = reorder_pages(reordered_pages, rules)
    # print("New page order: {}".format(reordered_pages))
    if evaluate_all_rules(reordered_pages,rules):
        # print("Page order is now valid")
        reordered_updates.append(reordered_pages)
    else:
        print("Page order is still invalid")

for update in reordered_updates:
    if not update_is_valid:
        print("{} is still not valid".format(update))

middle_page_number_sum = 0
for update in reordered_updates:
    middle_index = math.ceil((len(update)-1)/2.0)
    # print("The middle page in {} is {}".format(update, update[middle_index]))
    middle_page_number_sum += int(update[middle_index])
print("The sum of all middle page numbers (from reordered updates) is {}".format(middle_page_number_sum))
print("Total swaps: {}".format(swaps))
