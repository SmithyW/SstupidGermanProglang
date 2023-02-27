from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table import SymbolTable


class Semantic:

    def __init__(self):
        self.UNDEFINED = 0x10000001

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: any):
        return self.UNDEFINED

    def f(self, st: SyntaxTree, n: int):
        return self.UNDEFINED

