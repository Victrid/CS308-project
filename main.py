#!/bin/python

# Written with Python 3.9.5

import sys
from BNFUtils import lex
from BNFUtils.BNF_LALR_const import Symbol, Action, Goto, Reduce, GrammarSymbol, StateName
from BNFUtils.LALR_parse import parse
from BNFUtils.static import static_analysis


def main():
    lines = sys.stdin.readlines()
    t = "".join(lines)
    lex_result = lex.prepare(lex.lex(t))
    print(static_analysis(parse(lex_result, GrammarSymbol, StateName, Symbol, Reduce, Action, Goto)))


if __name__ == "__main__":
    main()
