from BNFUtils.common import IDType
from OPGUtils.common import Priority, OPGAmbiguousError


def fill_table(table, firstvt, lastvt, grammar):
    def mark(state, a, b):
        if table[a][b] != Priority.undefined and table[a][b] != state:
            raise OPGAmbiguousError("This OPG is ambiguous!")
        table[a][b] = state

    for induction in grammar:
        for sentence in induction[1]:
            for i in range(len(sentence) - 1):
                if sentence[i][0] == IDType.TERMINAL and sentence[i + 1][0] == IDType.TERMINAL:
                    mark(Priority.equal, sentence[i][1], sentence[i + 1][1])
                if sentence[i][0] == IDType.TERMINAL and sentence[i + 1][0] == IDType.NON_TERMINAL:
                    for term in firstvt[sentence[i + 1][1]]:
                        mark(Priority.less, sentence[i][1], term)
                if sentence[i][0] == IDType.NON_TERMINAL and sentence[i + 1][0] == IDType.TERMINAL:
                    for term in lastvt[sentence[i][1]]:
                        mark(Priority.more, term, sentence[i + 1][1])
                if i != len(sentence) - 2 and sentence[i][0] == IDType.TERMINAL and \
                        sentence[i + 2][0] == IDType.TERMINAL and sentence[i + 1][0] == IDType.NON_TERMINAL:
                    mark(Priority.equal, sentence[i][1], sentence[i + 2][1])
    return
