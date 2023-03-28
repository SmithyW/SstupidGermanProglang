from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table_codegen import SymbolTable

from semantic import Semantic


class Boolean(Semantic):

    def __init__(self):
        super().__init__()

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: any):
        return 'T' if st.tokenObj.lexeme == 'WAHR' else 'F'

    def f(self, st: SyntaxTree, n: int):
        return bool(st.tokenObj.lexeme)
