import inspect

from symbol_table import SymbolTable


class SymbolTableCodegen:

    def __init__(self, symbol_table: SymbolTable):
        self.table: list[SymbolTableEntry] = list()
        self.symbol_table = symbol_table

    def add(self, op: any, arg1: any, arg2: any):
        if type(arg1) == str:
            if self.symbol_table.search(arg1):
                arg1 = self.symbol_table.get_index(arg1)
        if type(arg2) == str:
            if self.symbol_table.search(arg2):
                arg2 = self.symbol_table.get_index(arg2)

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
