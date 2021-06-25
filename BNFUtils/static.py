# This file provides static analysis and checks.
# It would be faster if the step of checking are combined in one run, but we'd like to show the actual process, so we
# separate them to steps.
from .common import *


def static_analysis(parse_result):
    tree, terminal_table, symbol_table, init_symbol = type_tagging(parse_result)
    tree = combine_inductions(tree)
    tree = remove_identical_branches(tree)
    return tree, terminal_table, symbol_table, init_symbol


def type_tagging(parse_result):
    symbol_table = []
    all_table = []
    for induction in parse_result:
        symbol_table.append(induction[0][1])
        all_table.append(induction[0][1])
        for sentence in induction[1]:
            for word in sentence:
                if word[0] != IDType.EPSILON:
                    all_table.append(word[1])
    init_symbol = symbol_table[0]
    symbol_table = set(symbol_table)
    all_table = set(all_table)
    terminal_table = all_table.difference(symbol_table)
    symbol_table = list(symbol_table)
    terminal_table = list(terminal_table)
    linted = []
    for induction in parse_result:
        new_induction = []
        for sentence in induction[1]:
            new_sentence = []
            for word in sentence:
                if word[0] == IDType.EPSILON:
                    new_sentence.append((IDType.EPSILON, 0))
                elif word[1] in symbol_table:
                    new_sentence.append(
                        (IDType.NON_TERMINAL, symbol_table.index(word[1])))
                elif word[1] in terminal_table:
                    new_sentence.append(
                        (IDType.TERMINAL, terminal_table.index(word[1])))
            new_induction.append(tuple(new_sentence))
        linted.append(((IDType.INDUCT, symbol_table.index(
            induction[0][1])), tuple(new_induction)))
    return tuple(linted), terminal_table, symbol_table, init_symbol


def remove_identical_branches(parse_result):
    linted = []
    for induction in parse_result:
        induction_sets: set = set()
        count = 0
        for sentence in induction[1]:
            induction_sets.add(sentence)
            count += 1
        if len(induction_sets) < count:
            print("WARNING: identical branches found. Removed.")
        linted.append((induction[0], tuple(induction_sets)))
    return tuple(linted)


def combine_inductions(parse_result):
    induction_dict: dict = {}
    for induction in parse_result:
        if induction[0] in induction_dict:
            induction_dict[induction[0]] = tuple(list(induction_dict[induction[0]]) + list(induction[1]))
        else:
            induction_dict[induction[0]] = induction[1]
    return tuple(induction_dict.items())
