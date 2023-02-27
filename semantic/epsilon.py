from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table import SymbolTable

from semantic import Semantic


class Epsilon(Semantic):

    def __init__(self):
        super().__init__()

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: None):
        return arg1

    def f(self, st: SyntaxTree, n: int):
        return n
