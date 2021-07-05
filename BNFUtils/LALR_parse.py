from typing import Any

from .common import *
from .common import Action


# A parser implemented in LALR

def parse(sentence, grammar_symbol, state_name, symbol, reduce, action, goto):
    def do_error(current_index, current_stack, state_argument):
        raise BNFParseStageGrammarError(state_argument, state_name[state_argument], current_stack, current_index,
                                        sentence)

    def do_accept(current_stack):
        final_parse_result = current_stack[-2]
        accept = True
        return accept, final_parse_result

    def do_reduce(current_stack, aux_stack, state_argument):
        reduce_items = []
        for _ in range(reduce[state_argument][1]):
            current_stack.pop()
            reduce_items.append(current_stack.pop())
            aux_stack.pop()
            aux_stack.pop()
        new_state: int = goto[current_stack[-1]][grammar_symbol.index(reduce[state_argument][2])]
        current_stack.append(reduce[state_argument][3](*reversed(reduce_items)))
        aux_stack.append(reduce[state_argument][2])
        current_stack.append(new_state)
        aux_stack.append(new_state)

    def do_shift(current_index, current_stack, aux_stack, state_argument):
        current_stack.append(sentence[current_index])
        aux_stack.append(sentence[current_index])
        current_stack.append(state_argument)
        aux_stack.append(state_argument)
        current_index += 1
        return current_index

    def do_action(current_index: int, current_stack: list[int, Any], aux_stack: list[int, str, Any]):
        final_parse_result = None
        accept: bool = False
        state_action, state_argument = action[current_stack[-1]][symbol.index(sentence[current_index][0])]
        if state_action == Action.err:
            do_error(current_index, aux_stack, state_argument)
        elif state_action == Action.sft:
            current_index = do_shift(current_index, current_stack, aux_stack, state_argument)
        elif state_action == Action.rdu:
            do_reduce(current_stack, aux_stack, state_argument)
        elif state_action == Action.acc:
            accept, final_parse_result = do_accept(current_stack)
        return accept, current_index, final_parse_result

    acc = False
    result = None
    stack = [0]
    # Used for error pretty print
    auxiliary_stack = [0]
    index = 0
    while not acc:
        acc, index, result = do_action(index, stack, auxiliary_stack)

    return result
