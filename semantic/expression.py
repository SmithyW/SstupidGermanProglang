from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table_codegen import SymbolTable

from semantic import Semantic


class Expression(Semantic):
    # expression -> term rightExpression
    def __init__(self):
        super().__init__()

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: any):
        term: SyntaxTree = st.get_child(0)
        right_expression: SyntaxTree = st.get_child(1)

        return right_expression.value.p(right_expression, sym, term.value.p(term, sym, None))

    def f(self, st: SyntaxTree, n: int) -> int | str:
        term: SyntaxTree = st.get_child(0)
        right_expression: SyntaxTree = st.get_child(1)
        return right_expression.value.f(right_expression, term.value.f(term, self.UNDEFINED))
