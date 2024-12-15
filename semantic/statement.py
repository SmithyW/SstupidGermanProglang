from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table_codegen import SymbolTable

from semantic import Semantic
from lex_token import TOKEN


class Statement(Semantic):
    # statement -> assignment eol

    # statement -> print eol # TODO: Implementieren

    # statement -> expression eol
    # statement.f = expression.f '!'

    def __init__(self):
        super().__init__()

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: any):
        if len(st.childNodes) == 2:
            expression: SyntaxTree = st.get_child(0)
            eol: SyntaxTree = st.get_child(1)

            if eol.token == TOKEN.EOL:
                return expression.value.p(expression, sym, arg1)

        elif len(st.childNodes) == 3:
            prnt: SyntaxTree = st.get_child(0)
            ident: SyntaxTree = st.get_child(1)
            eol: SyntaxTree = st.get_child(2)

            if eol.token == TOKEN.EOL:
                sym_entry = sym.add(
                    'aus', ident.value.p(ident, sym, arg1), None)
                return None

        elif len(st.childNodes) == 4:
            ident: SyntaxTree = st.get_child(0)
            assign: SyntaxTree = st.get_child(1)
            expression: SyntaxTree = st.get_child(2)
            eol: SyntaxTree = st.get_child(3)

            if eol.token == TOKEN.EOL:
                if assign.token == TOKEN.ASSIGN:
                    sym_entry = sym.add('=', ident.value.p(
                        ident, sym, arg1), expression.value.p(expression, sym, arg1))
                    return sym_entry
                else:
                    print("Expected Assign Symbol")
                    return None

        elif len(st.childNodes) == 5:
            var: SyntaxTree = st.get_child(0)
            ident: SyntaxTree = st.get_child(1)
            assign: SyntaxTree = st.get_child(2)
            expression: SyntaxTree = st.get_child(3)
            eol: SyntaxTree = st.get_child(4)

            if eol.token == TOKEN.EOL:
                if assign.token == TOKEN.ASSIGN:
                    sym_entry = sym.add('=', ident.value.p(
                        ident, sym, arg1), expression.value.p(expression, sym, arg1))
                    return sym_entry
                else:
                    print("Expected Assign Symbol")
                    return None

        print("Expected EOL")
        return None

    def f(self, st: SyntaxTree, n: int):
        expression: SyntaxTree = st.get_child(0)
        eol: SyntaxTree = st.get_child(1)

        if eol.token == TOKEN.EOL:
            return expression.value.f(expression, self.UNDEFINED)
        else:
            # TODO: Semantic error (EOL expected)
            return self.UNDEFINED
