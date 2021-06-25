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
    def sentence_printer(current_index, sentence):
        contents = []
        for item in sentence[current_index:]:
            if item[0] == IDType.INDUCT:
                contents.append(item[1])
                contents.append("->")
            elif item[0] == IDType.BRANCH:
                contents.append("|")
            elif item[0] == IDType.DOLLAR:
                contents.append("$")
            elif item[0] == IDType.EPSILON:
                contents.append("ϵ")
            elif item[0] == IDType.SYMBOL:
                contents.append(item[1])
        return "Current state sentence:\n" + " ".join(contents)

    @staticmethod
    def stack_printer(stack):
        lines = ["Current state stack:"]
        for item in stack:
            if type(item) is int:
                lines.append("status {}".format(item))
            else:
                lines.append(str(item))
        return "\n".join(lines)

    def __init__(self, state, state_name, stack, index, sentence):
        super().__init__(
            "Grammar not correct.\nError happened at state {} when parsing.\n"
            "State {} performs: {}\n{}\n{}".format(
                state, state, state_name,
                self.sentence_printer(index, sentence),
                self.stack_printer(stack)))
