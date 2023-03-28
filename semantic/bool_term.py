from __future__ import annotations
from typing import TYPE_CHECKING

from lex_token import TOKEN

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table_codegen import SymbolTable

from semantic import Semantic


class BoolTerm(Semantic):
    # boolTerm -> comparison
    #    | boolean
    #    | ident
    #    | (boolExpression)
    # term -> operator rightTerm
    # term.f = rightTerm.f(operator.f)
    def __init__(self):
        super().__init__()

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: any):
        if len(st.childNodes) == 1:
            ch: SyntaxTree = st.get_child(0)
            return ch.value.p(ch, sym, arg1)
        elif len(st.childNodes) == 3:
            bool_expression: SyntaxTree = st.get_child(0)
            return bool_expression.value.p(bool_expression, sym, arg1)
        else:
            return arg1

    def f(self, st: SyntaxTree, n: int):
        operator: SyntaxTree = st.get_child(0)
        right_term: SyntaxTree = st.get_child(1)

        return right_term.value.f(right_term, operator.value.f(operator, self.UNDEFINED))
