from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table_codegen import SymbolTable

from semantic import Semantic


class Term(Semantic):
    # term -> operator rightTerm
    # term.f = rightTerm.f(operator.f)
    def __init__(self):
        super().__init__()

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: any):
        operator: SyntaxTree = st.get_child(0)
        right_term: SyntaxTree = st.get_child(1)

        return right_term.value.p(right_term, sym, operator.value.p(operator, sym, None))

    def f(self, st: SyntaxTree, n: int):
        operator: SyntaxTree = st.get_child(0)
        right_term: SyntaxTree = st.get_child(1)

        return right_term.value.f(right_term, operator.value.f(operator, self.UNDEFINED))
