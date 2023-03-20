import inspect


class SymbolTableCodegen:

    def __init__(self):
        self.table: list[SymbolTableEntry] = list()

    def add(self, op: any, arg1: any, arg2: any):
        new_entry = SymbolTableEntry(len(self.table), op, arg1, arg2)
        self.table.append(new_entry)
        return new_entry

    def print(self):
        for x in range(len(self.table)):
            print(str(self.table[x]))


class SymbolTableEntry:

    def __init__(self, idx, op, arg1, arg2):
        self.index: int = idx
        self.operator = op
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        argument2 = "#" + str(self.arg2.index) if isinstance(self.arg2, SymbolTableEntry) else str(self.arg2)
        argument1 = "#" + str(self.arg1.index) if isinstance(self.arg1, SymbolTableEntry) else str(self.arg1)
        return "{0} {1} {2} {3}".format(str(self.index), self.operator, argument1, argument2)
