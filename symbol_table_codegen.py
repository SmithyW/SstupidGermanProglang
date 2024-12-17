from symbol_table import SymbolTable


class SymbolTableCodegen:

    def __init__(self, symbol_table: SymbolTable):
        self.table: list[SymbolTableEntry] = list()
        self.symbol_table = symbol_table
        self.temp_counter = 0

    def add(self, op: any, arg1: any, arg2: any):
        ident = None
        if (op in ['+', '-', '*', '/']):
            self.temp_counter += 1
        if type(arg1) == str:
            if self.symbol_table.search(arg1):
                arg1 = self.symbol_table.get_index(arg1)
                if op == "=":
                    ident = arg1
        if type(arg2) == str:
            if self.symbol_table.search(arg2):
                arg2 = self.symbol_table.get_index(arg2)

        new_entry = SymbolTableEntry(
            len(self.table), op, arg1, arg2, ident if ident else "T"+str(self.temp_counter))
        self.table.append(new_entry)
        return new_entry

    def print(self):
        print("Idx | Op | Arg1 | Arg2")
        print("----|----|------|------")
        for _, x in enumerate(self.table):
            print(str(x))


class SymbolTableEntry:

    def __init__(self, idx, op, arg1, arg2, place):
        self.index: int = idx
        self.operator: str = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.place = place

    def __str__(self):
        argument2 = str(self.arg2.place) if isinstance(self.arg2,
                                                       SymbolTableEntry) else str(self.arg2)
        argument1 = str(self.arg1.place) if isinstance(self.arg1,
                                                       SymbolTableEntry) else str(self.arg1)
        if argument1 == self.place:
            argument1 = ""
        return f"{str(self.place).ljust(3)} | {self.operator.ljust(2)} | {argument1.ljust(4)} | {argument2.ljust(4)}"
