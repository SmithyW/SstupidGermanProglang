from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree

from semantic import Semantic


class Term(Semantic):
    # term -> operator rightTerm
    # term.f = rightTerm.f(operator.f)
    def __init__(self):
        super().__init__()

    def f(self, st: SyntaxTree, n: int):
        operator: SyntaxTree = st.get_child(0)
        right_term: SyntaxTree = st.get_child(1)

        return right_term.value.f(right_term, operator.value.f(operator, self.UNDEFINED))
