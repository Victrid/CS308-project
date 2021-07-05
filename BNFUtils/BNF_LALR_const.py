# This file defines the LALR tables and SDT actions to form an AST tree

# BNF of BNF

# S -> E | E S
# E -> INDUCT L
# L -> X | L BRANCH X
# X -> T | EPSILON
# T -> SYMBOL | T SYMBOL

from enum import Enum, auto

from BNFUtils.common import IDType, Action


class GrammarType(Enum):
    E = auto()
    L = auto()
    S = auto()
    T = auto()
    X = auto()

    Error = auto()


Reduce = [
    ("S'-> S", 1, GrammarType.Error, lambda s: None),
    ("E -> INDUCT L", 2, GrammarType.E, lambda induct, induct_list: (induct, induct_list)),
    ("L -> X", 1, GrammarType.L, lambda induction: [induction]),
    ("L -> L BRANCH X", 3, GrammarType.L, lambda induct_list, _, induction: induct_list + [induction]),
    ("S -> E", 1, GrammarType.S, lambda sentence: [sentence]),
    ("S -> S E", 2, GrammarType.S, lambda sentence, sentence_list: sentence + [sentence_list]),
    ("T -> SYMBOL", 1, GrammarType.T, lambda t: [t]),
    ("T -> T SYMBOL", 2, GrammarType.T, lambda t_list, t: t_list + [t]),
    ("X -> T", 1, GrammarType.X, lambda t: t),
    ("X -> EPSILON", 1, GrammarType.X, lambda epsilon: epsilon)
]

StateName = [
    "S' -> • S",
    "S -> E • ",
    "S' -> S • \nS  -> S • E",
    "E -> INDUCT • L",
    "S -> S E • ",
    "E -> INDUCT L •\nL -> L • BRANCH X",
    "T -> T • SYMBOL\nX -> T • ",
    "L -> X • ",
    "X -> EPSILON • ",
    "T -> SYMBOL • ",
    "L -> L BRANCH • X",
    "T -> T SYMBOL • ",
    "L -> L BRANCH X • "
]

Symbol: list[IDType] = [IDType.BRANCH, IDType.EPSILON,
                        IDType.INDUCT, IDType.SYMBOL, IDType.DOLLAR]

GrammarSymbol: list[GrammarType] = [GrammarType.E, GrammarType.L, GrammarType.S, GrammarType.T, GrammarType.X]

Action: list[
    tuple[tuple[Action, int], tuple[Action, int], tuple[Action, int], tuple[Action, int], tuple[Action, int]]] = [
    ((Action.err, 0), (Action.err, 0), (Action.sft, 3), (Action.err, 0), (Action.err, 3)),
    ((Action.err, 1), (Action.err, 1), (Action.rdu, 4), (Action.err, 1), (Action.rdu, 4)),
    ((Action.err, 2), (Action.err, 2), (Action.sft, 3), (Action.err, 2), (Action.acc, 0)),
    ((Action.err, 3), (Action.sft, 8), (Action.err, 3), (Action.sft, 9), (Action.err, 3)),
    ((Action.err, 4), (Action.err, 4), (Action.rdu, 5), (Action.err, 4), (Action.rdu, 5)),
    ((Action.sft, 10), (Action.err, 5), (Action.rdu, 1), (Action.err, 5), (Action.rdu, 1)),
    ((Action.rdu, 8), (Action.err, 6), (Action.rdu, 8), (Action.sft, 11), (Action.rdu, 8)),
    ((Action.rdu, 2), (Action.err, 7), (Action.rdu, 2), (Action.err, 7), (Action.rdu, 2)),
    ((Action.rdu, 9), (Action.err, 8), (Action.rdu, 9), (Action.err, 8), (Action.rdu, 9)),
    ((Action.rdu, 6), (Action.err, 9), (Action.rdu, 6), (Action.rdu, 6), (Action.rdu, 6)),
    ((Action.err, 10), (Action.sft, 8), (Action.err, 10), (Action.sft, 9), (Action.err, 10)),
    ((Action.rdu, 7), (Action.err, 11), (Action.rdu, 7), (Action.rdu, 7), (Action.rdu, 7)),
    ((Action.rdu, 3), (Action.err, 12), (Action.rdu, 3), (Action.err, 12), (Action.rdu, 3))
]

Goto: list[tuple[int, int, int, int, int]] = [
    (1, -1, 2, -1, -1),
    (-1, -1, -1, -1, -1),
    (4, -1, -1, -1, -1),
    (-1, 5, -1, 6, 7),
    (-1, -1, -1, -1, -1),
    (-1, -1, -1, -1, -1),
    (-1, -1, -1, -1, -1),
    (-1, -1, -1, -1, -1),
    (-1, -1, -1, -1, -1),
    (-1, -1, -1, -1, -1),
    (-1, -1, -1, 6, 12),
    (-1, -1, -1, -1, -1),
    (-1, -1, -1, -1, -1)
]
