from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table_codegen import SymbolTable

from semantic import Semantic


class BoolExpression(Semantic):
    # boolExpression -> boolTerm rightBool
    def __init__(self):
        super().__init__()

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: any):
        bool_term: SyntaxTree = st.get_child(0)
        right_bool: SyntaxTree = st.get_child(1)

        return right_bool.value.p(right_bool, sym, bool_term.value.p(bool_term, sym, None))

    def f(self, st: SyntaxTree, n: int) -> int | str:
        bool_term: SyntaxTree = st.get_child(0)
        right_bool: SyntaxTree = st.get_child(1)
        return right_bool.value.f(right_bool, bool_term.value.f(bool_term, self.UNDEFINED))
