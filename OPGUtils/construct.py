# Here constructs the FIRSTVT and the LASTVT.
from BNFUtils.common import IDType


def first_vt(grammar):
    first_vt_table = [set() for _ in range(len(grammar))]
    stack = []

    for induction in grammar:
        for sentence in induction[1]:
            # B -> aβ, a in FIRSTVT(B)
            if sentence[0][0] == IDType.TERMINAL:
                first_vt_table[induction[0][1]].add(sentence[0][1])
                stack.append(induction[0][1])
            # B -> Daβ, a in FIRSTVT(B)
            if len(sentence) > 1 and sentence[0][0] == IDType.NON_TERMINAL and sentence[1][0] == IDType.TERMINAL:
                first_vt_table[induction[0][1]].add(sentence[1][1])
                stack.append(induction[0][1])

    while len(stack):
        non_terminal = stack.pop()
        for induction in grammar:
            for sentence in induction[1]:
                # B -> Dβ, FIRSTVT(D) in FIRSTVT(B)
                if sentence[0][0] == IDType.NON_TERMINAL and sentence[0][1] == non_terminal:
                    if len(first_vt_table[sentence[0][1]].difference(first_vt_table[induction[0][1]])):
                        first_vt_table[induction[0][1]] = first_vt_table[induction[0][1]] | first_vt_table[
                            sentence[0][1]]
                        stack.append(induction[0][1])
                    pass
    return first_vt_table


def last_vt(grammar):
    last_vt_table = [set() for _ in range(len(grammar))]
    stack = []

    for induction in grammar:
        for sentence in induction[1]:
            # B -> βa, a in LASTVT(B)
            if sentence[-1][0] == IDType.TERMINAL:
                last_vt_table[induction[0][1]].add(sentence[-1][1])
                stack.append(induction[0][1])
            # B -> βaD, a in LASTVT(B)
            if len(sentence) > 1 and sentence[-1][0] == IDType.NON_TERMINAL and sentence[-2][0] == IDType.TERMINAL:
                last_vt_table[induction[0][1]].add(sentence[-2][1])
                stack.append(induction[0][1])

    while len(stack):
        non_terminal = stack.pop()
        for induction in grammar:
            for sentence in induction[1]:
                # B -> βD, LASTVT(D) in LASTVT(B)
                if sentence[-1][0] == IDType.NON_TERMINAL and sentence[-1][1] == non_terminal:
                    if len(last_vt_table[sentence[-1][1]].difference(last_vt_table[induction[0][1]])):
                        last_vt_table[induction[0][1]] = last_vt_table[induction[0][1]] | last_vt_table[
                            sentence[-1][1]]
                        stack.append(induction[0][1])
    return last_vt_table
