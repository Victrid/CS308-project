#!/bin/python

# Written with Python 3.9.5
import argparse
import sys

from BNFUtils.BNF_LALR_const import Symbol, Action, Goto, Reduce, GrammarSymbol, StateName
from BNFUtils.LALR_parse import parse
from BNFUtils.lex import lex
from BNFUtils.lex import prepare
from BNFUtils.static import static_analysis
from OPGUtils.common import Priority
from OPGUtils.construct import first_vt, last_vt
from OPGUtils.filltable import fill_table
from OPGUtils.printer import printer
from OPGUtils.static import OPG_check, end_symbol


def main():
    args = parse_arguments()

    if not args.trace:
        sys.tracebacklimit = 0

    if args.input_file is None:
        inputf = sys.stdin
    else:
        inputf = open(args.input_file, "r")
    lines = inputf.readlines()
    t = "".join(lines)

    lex_result = prepare(lex(t))
    grammar, terminal_table, symbol_table, init_symbol = static_analysis(
        parse(lex_result, GrammarSymbol, StateName, Symbol, Reduce, Action, Goto))

    grammar, terminal_table, symbol_table = end_symbol(grammar, symbol_table, terminal_table, init_symbol)
    OPG_check(grammar)
    firstvt = first_vt(grammar)
    lastvt = last_vt(grammar)
    table = [[Priority.undefined for _ in range(len(terminal_table))] for _ in range(len(terminal_table))]
    fill_table(table, firstvt, lastvt, grammar)

    lines = printer(table, terminal_table)
    if args.output_file is None:
        outputf = sys.stdout
    else:
        outputf = open(args.output_file, "w+")
    outputf.writelines(lines)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate the OPG Table.')
    parser.add_argument("-i", "--input-file", dest="input_file", default=None,
                        help="Specify input file.")
    parser.add_argument("-o", "--output-file", dest="output_file", default=None,
                        help="Specify output file.")
    parser.add_argument("--need-traceback", dest="trace", action="store_true", default=False,
                        help="Show the traceback when error occurs.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
