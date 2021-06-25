from OPGUtils.common import Priority
import importlib

def printer(table, terminal_table):
    def judge(item):
        if item == Priority.more:
            return ">"
        if item == Priority.less:
            return "<"
        if item == Priority.equal:
            return "="
        return ""

    print("\t" + "\t".join(terminal_table))
    for line, body in zip(table, terminal_table):
        print(body +"\t"+ "\t".join([judge(item) for item in line]))
