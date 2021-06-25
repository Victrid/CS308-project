# This file provides checks.
# It would be faster if the step of checking are combined in one run, but we'd like to show the actual process, so we
# separate them to steps.

from BNFUtils.common import IDType
from OPGUtils.common import NonOPGError


# Original BNF does not add end_symbol for analysis

def end_symbol(grammar, symbol_table, terminal_table, init_symbol):
    new_terminal = len(terminal_table)
    terminal_table.append("$")
    new_induction = len(grammar)
    grammar = tuple(list(grammar) + [
        (
            (IDType.INDUCT, new_induction),
            (
                (
                    (IDType.TERMINAL, new_terminal),
                    (IDType.NON_TERMINAL, symbol_table.index(init_symbol)),
                    (IDType.TERMINAL, new_terminal),
                ),
            ),
        ),
    ])
    symbol_table.append("init_symbol")
    return grammar, terminal_table, symbol_table


def OPG_check(grammar):
    Epsilon_check(grammar)
    no_neighbor_non_terminal_check(grammar)


def Epsilon_check(grammar):
    for induction in grammar:
        for sentence in induction[1]:
            for word in sentence:
                if word[0] == IDType.EPSILON:
                    raise NonOPGError("EPSILON Mark in operator precedence grammar is not allowed.")
    return


def no_neighbor_non_terminal_check(grammar):
    for induction in grammar:
        for sentence in induction[1]:
            for index in range(len(sentence) - 1):
                if sentence[index][0] == IDType.NON_TERMINAL and sentence[index + 1][0] == IDType.NON_TERMINAL:
                    raise NonOPGError("Neighboring non-terminal in operator precedence grammar is not allowed.")
    return
