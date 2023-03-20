from lex_token import Token


class SymbolTable:

    def __init__(self):
        self.table: list[SymbolTableEntry] = list()

    def insert(self, token: Token):
        new_entry = SymbolTableEntry(len(self.table), token, '')
        self.table.append(new_entry)
        return new_entry

    def print(self):
        for x in range(len(self.table)):
            print(str(self.table[x]))


class SymbolTableEntry:

    def __init__(self, idx, token: Token, sym_type):
        self.index: int = idx
        self.token = token
        self.sym_type = sym_type

    def __str__(self):
        return "{0} {1} {2} {3}".format(str(self.index), self.token.lexeme)
