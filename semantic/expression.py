from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree

from semantic import Semantic


class Expression(Semantic):
    # expression -> term rightExpression
    def __init__(self):
        super().__init__()

    def f(self, st: SyntaxTree, n: int) -> int | str:
        term: SyntaxTree = st.get_child(0)
        right_expression: SyntaxTree = st.get_child(1)
        return right_expression.value.f(right_expression, term.value.f(term, self.UNDEFINED))
