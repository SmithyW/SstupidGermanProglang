from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree
    from symbol_table_codegen import SymbolTable

from semantic import Semantic


class Program(Semantic):
    # program -> statement program
    # program.f = program.f(statement.f)

    # program -> statement
    # program.f = statement.f

    # program -> epsilon
    # program.f(n) = n

    def __init__(self):
        super().__init__()

    def p(self, st: SyntaxTree, sym: SymbolTable, arg1: any):
        if len(st.childNodes) == 2:
            statement: SyntaxTree = st.get_child(0)
            program: SyntaxTree = st.get_child(1)

            return program.value.p(program, sym, statement.value.p(statement, sym, arg1))

        elif len(st.childNodes) == 1:
            statement: SyntaxTree = st.get_child(0)
            return statement.value.p(statement, sym, arg1)
        else:
            return None

    def f(self, st: SyntaxTree, n: int):
        if len(st.childNodes) == 2:
            statement: SyntaxTree = st.get_child(0)
            program: SyntaxTree = st.get_child(1)
            return program.value.f(program, statement.value.f(statement, self.UNDEFINED))
        elif len(st.childNodes) == 1:
            statement: SyntaxTree = st.get_child(0)
            return statement.value.f(statement, self.UNDEFINED)
        else:
            return n

