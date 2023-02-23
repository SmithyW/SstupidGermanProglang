from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree

from semantic import Semantic


class RightTerm(Semantic):
    # rightTerm -> mult operator rightTerm
    # rightTerm.f(n) = n * rightTerm.f(operator.f)

    # rightTerm -> div operator rightTerm
    # rightTerm.f(n) = n / rightTerm.f(operator.f)

    # rightTerm -> Epsilon
    # rightTerm.f(n) = n

    def __init__(self):
        super().__init__()

    def f(self, st: SyntaxTree, n: int):
        if len(st.childNodes) == 3:
            symbol: SyntaxTree = st.get_child(0)
            operator: SyntaxTree = st.get_child(1)
            right_term: SyntaxTree = st.get_child(2)

            match symbol.get_lexeme():
                case '*':
                    return n*right_term.value.f(right_term, operator.value.f(operator, self.UNDEFINED))
                case '/':
                    return n/right_term.value.f(right_term, operator.value.f(operator, self.UNDEFINED))
                case _:
                    return self.UNDEFINED
        else:
            return n
