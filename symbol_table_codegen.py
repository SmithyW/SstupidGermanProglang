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
        print("Idx | Op | Arg1 | Arg2")
        print("----|----|------|------")
        for x in range(len(self.table)):
            print(str(self.table[x]))


class SymbolTableEntry:

    def __init__(self, idx, op, arg1, arg2):
        self.index: int = idx
        self.operator: str = op
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        argument2 = "T" + str(self.arg2.index) if isinstance(self.arg2,
                                                             SymbolTableEntry) else str(self.arg2)
        argument1 = "T" + str(self.arg1.index) if isinstance(self.arg1,
                                                             SymbolTableEntry) else str(self.arg1)
        return f"{"T"+str(self.index).ljust(2)} | {self.operator.ljust(2)} | {argument1.ljust(4)} | {argument2.ljust(4)}"
