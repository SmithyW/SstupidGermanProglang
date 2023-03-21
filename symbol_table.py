from lex_token import Token, TOKEN


class SymbolTable:

    def __init__(self):
        self.table: list[SymbolTableEntry] = list()

    def insert(self, token: Token, el_type: TOKEN):
        new_entry = SymbolTableEntry(len(self.table), token.lexeme, token, el_type)
        self.table.append(new_entry)
        return new_entry

    def search(self, term: str):
        found_entry = list(filter(lambda t: t.name == term, self.table))
        if len(found_entry) == 0:
            return False
        return found_entry[0]

    def get_index(self, term: str) -> str:
        for idx, x in enumerate(self.table):
            if x.name == term:
                return f"id{x.index}"
        return "id#ERR"

    def print(self):
        for x in range(len(self.table)):
            print(str(self.table[x]))


class SymbolTableEntry:

    def __init__(self, idx, name: str, token: Token, sym_type: TOKEN):
        self.index: int = idx
        self.name: str = name
        self.token = token
        self.sym_type = sym_type

    def __str__(self):
        return "{0} {1} {2} {3}".format(str(self.index), self.name, self.token.token, self.sym_type)
