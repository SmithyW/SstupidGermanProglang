from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table import SymbolTable

from semantic import Semantic
from lex_token import TOKEN


class Statement(Semantic):
    # statement -> assignment eol # TODO: Implementieren

    # statement -> print eol # TODO: Implementieren

    # statement -> expression eol
    # statement.f = expression.f '!'

    def __init__(self):
        super().__init__()

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: any):
        expression: SyntaxTree = st.get_child(0)
        eol: SyntaxTree = st.get_child(1)

        if eol.token == TOKEN.EOL:
            return expression.value.p(expression, sym, arg1)

    def f(self, st: SyntaxTree, n: int):
        expression: SyntaxTree = st.get_child(0)
        eol: SyntaxTree = st.get_child(1)

        if eol.token == TOKEN.EOL:
            return expression.value.f(expression, self.UNDEFINED)
        else:
            # TODO: Semantic error (EOL expected)
            return self.UNDEFINED
