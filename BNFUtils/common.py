# This file defines type and exceptions.
from enum import Enum, auto


class IDType(Enum):
    INDUCT = auto()
    BRANCH = auto()
    SYMBOL = auto()
    EPSILON = auto()
    DOLLAR = auto()

    NON_TERMINAL = auto()
    TERMINAL = auto()
    UNUSED = auto()


class Action(Enum):
    err = auto()
    sft = auto()
    rdu = auto()
    acc = auto()


class BNFLexStageGrammarError(Exception):
    def __init__(self, message):
        super().__init__(message)


class BNFParseStageGrammarError(Exception):

    @staticmethod
    def item_tuple_printer(item):
        if item[0] == IDType.INDUCT:
            return [item[1], "->"]
        elif item[0] == IDType.BRANCH:
            return ["|"]
        elif item[0] == IDType.DOLLAR:
            return ["$"]
        elif item[0] == IDType.EPSILON:
            return ["ϵ"]
        elif item[0] == IDType.SYMBOL:
            return [item[1]]

    @staticmethod
    def sentence_printer(current_index, sentence):
        contents = []
        for item in sentence[current_index:]:
            contents += BNFParseStageGrammarError.item_tuple_printer(item)
        return "Current state sentence:\n" + " ".join(contents)

    @staticmethod
    def stack_printer(stack):
        lines = []
        for item in stack:
            if type(item) is int:
                lines.append("status({})".format(item))
            elif type(item) is tuple:
                lines += BNFParseStageGrammarError.item_tuple_printer(item)
            else:
                lines.append(str(item))
        return "Current state stack:\n" + " ".join(lines)

    def __init__(self, state, state_name, stack, index, sentence):
        super().__init__(
            "Grammar not correct.\nError happened at state {} when parsing.\n"
            "State {} performs: {}\n{}\n{}".format(
                state, state, state_name,
                self.sentence_printer(index, sentence),
                self.stack_printer(stack)))
