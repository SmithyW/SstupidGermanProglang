from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table_codegen import SymbolTable

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

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: any):
        if len(st.childNodes) == 3:
            symbol: SyntaxTree = st.get_child(0)
            term: SyntaxTree = st.get_child(1)
            right_expression: SyntaxTree = st.get_child(2)

            match symbol.get_lexeme():
                case '+':
                    sym_entry = sym.add('+', arg1, term.value.p(term, sym, None))
                    return right_expression.value.p(right_expression, sym, sym_entry)
                case '-':
                    sym_entry = sym.add('-', arg1, term.value.p(term, sym, None))
                    return right_expression.value.p(right_expression, sym, sym_entry)
                case _:
                    return arg1
        else:
            return arg1

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
