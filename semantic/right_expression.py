from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree

from semantic import Semantic


class RightExpression(Semantic):
    # rightExpression -> plus term rightExpression
    # rightExpression.f(n) = n+rightExpression.f(term.f)

    # rightExpression -> minus term rightExpression
    # rightExpression.f(n) = n-rightExpression.f(term.f)

    # rightExpression -> Epsilon
    # rightExpression.f(n) = n
    def __init__(self):
        super().__init__()
        
    def f(self, st: SyntaxTree, n: int) -> int | str:
        if len(st.childNodes) == 3:
            symbol: SyntaxTree = st.get_child(0)
            term: SyntaxTree = st.get_child(1)
            right_expression: SyntaxTree = st.get_child(2)
            match symbol.get_lexeme():
                case '+':
                    return n + right_expression.value.f(right_expression, term.value.f(term, self.UNDEFINED))
                case '-':
                    return right_expression.value.f(right_expression, n - term.value.f(term, self.UNDEFINED))
                case _:
                    return self.UNDEFINED
        else:
            return n
