from .common import *


def lex(string: str) -> list[(IDType, str)]:
    lex_result = []
    induct = "->"
    branch = "|"
    epsilon = "ϵ"
    token_list = string.split()
    for item in token_list:
        if item == induct:
            lex_result.append((IDType.INDUCT, ""))
            continue
        if item == branch:
            lex_result.append((IDType.BRANCH, ""))
            continue
        if item == epsilon:
            lex_result.append((IDType.EPSILON, ""))
            continue
        lex_result.append((IDType.SYMBOL, item))
    lex_result.append((IDType.DOLLAR, ""))
    return lex_result


# BNF, by simple lexing, is even not a LALR(1) grammar, as we want to support
# multiple line form like this:
#      E -> A
#         | B
#         | CD
# without separating symbols, we need to combine INDUCT first (which is performing an extra lookahead).
# By this way we can guarantee it is LALR(1) grammar, used for former parsing.


def prepare(lexed_list: list[(IDType, str)]) -> list[(IDType, str)]:
    for index in range(len(lexed_list) - 1):
        if lexed_list[index + 1][0] == IDType.INDUCT:
            if lexed_list[index][0] == IDType.SYMBOL:
                lexed_list[index + 1] = (IDType.INDUCT, lexed_list[index][1])
                lexed_list[index] = (IDType.UNUSED, "")
            elif lexed_list[index][0] == IDType.INDUCT:
                raise BNFLexStageGrammarError(
                    "Wrong representation: {} -> ->".format(lexed_list[index][1]))
            elif lexed_list[index][0] == IDType.BRANCH:
                raise BNFLexStageGrammarError(
                    "Wrong representation: {} ->".format("|"))
            elif lexed_list[index][0] == IDType.EPSILON:
                raise BNFLexStageGrammarError(
                    "Wrong representation: {} ->".format("ϵ"))
            else:
                raise BNFLexStageGrammarError(
                    "Wrong representation: {} ->".format(lexed_list[index][1]))

    return list(filter(lambda x: x[0] != IDType.UNUSED, lexed_list))
