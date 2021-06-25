from OPGUtils.common import Priority


def printer(table, terminal_table):
    lines = []

    def judge(item):
        if item == Priority.more:
            return ">"
        if item == Priority.less:
            return "<"
        if item == Priority.equal:
            return "="
        return ""

    lines.append("\t" + "\t".join(terminal_table))
    for line, body in zip(table, terminal_table):
        lines.append(body + "\t" + "\t".join([judge(item) for item in line]))
    return [line + "\n" for line in lines]
