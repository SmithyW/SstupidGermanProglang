from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lex_token import Token
    from syntax_tree import SyntaxTree

from lexer import TOKEN
from semantic import *

# Grammatik:
# program -> statement program | epsilon
# statement -> (assignment | expression | print) eol
#
# assignment -> var ident assign expression
# assignment -> ident assign expression
# print -> print ident
# expression -> term rightExpression
#
#
#
# rightExpression -> plus term rightExpression
# rightExpression -> minus term rightExpression
# rightExpression -> Epsilon
# term -> operator rightTerm
# rightTerm -> mult operator rightTerm
# rightTerm -> div operator rightTerm
# rightTerm -> Epsilon
# operator -> openPar expression closePar | num | ident


class Parser:
    """
    Aufbau aller Funktionen von Nichtterminalsymbolen ist gleich
    Verschiedene Sets in Form eines Arrays für jedes mögliche vorkommende
    Terminalsymbol erstellen.
    Falls notwendig, look_ahead_sets erstellen.

    Andhand der Grammatik werden die einzelnen Abläufe implementiert.
    Implementierung als rekursiver Abstieg.

    """

    def __init__(self, tokens):
        self.tokens: list[Token] = tokens
        self.current_token_pointer: int = 0
        self.parse_tree: SyntaxTree | None = None

    def parse(self, parse_tree: SyntaxTree):
        # Parsen wird an dieser Stelle mit dem übergebenen initialen
        # Syntaxtbaums gestartet
        if self.program(parse_tree):
            return True
        else:
            self.syntax_error("Fehler in Programm")
            return False

    # program -> statement program | statement
    def program(self, st: SyntaxTree) -> bool:
        eof_set = [TOKEN.EOF]
        if self.statement(st.insert_subtree(TOKEN.STATEMENT, Statement())):
            if not self.match(eof_set, st):
                return self.program(st.insert_subtree(TOKEN.PROGRAM, Program()))
            else:
                return True
        else:
            self.syntax_error("Fehler in Ausdruck")
            return False

    # statement -> (assignment | print | expression) eol
    # statement -> var ident assign expression eol
    # statement -> print ident eol
    # statement -> expression eol
    def statement(self, st: SyntaxTree) -> bool:
        var_set = [TOKEN.STR, TOKEN.INT, TOKEN.BOOLEAN]
        print_set = [TOKEN.PRINT]
        ident_set = [TOKEN.IDENT]
        eol_set = [TOKEN.EOL]
        assign_set = [TOKEN.ASSIGN]

        if self.match(var_set, st):
            if self.match(ident_set, st):
                if self.match(assign_set, st):
                    if self.expression(st.insert_subtree(TOKEN.EXPRESSION, get_semantic_function(TOKEN.EXPRESSION))):
                        if self.match(eol_set, st):
                            return True
                        else:
                            self.syntax_error("EOL Zeichen erwartet")
                            return False
                    else:
                        self.syntax_error("Fehler in Ausdruck")
                        return False
                else:
                    self.syntax_error("Zuweisungszeichen erwartet")
                    return False
            else:
                self.syntax_error("Variable erwartet")
                return False
        elif self.match(ident_set, st):
            if self.match(assign_set, st):
                if self.expression(st.insert_subtree(TOKEN.EXPRESSION, get_semantic_function(TOKEN.EXPRESSION))):
                    if self.match(eol_set, st):
                        return True
                    else:
                        self.syntax_error("EOL Zeichen erwartet!!!")
                        return False
                else:
                    self.syntax_error("Fehler in Ausdruck")
                    return False
            else:
                self.syntax_error("Zuweisungszeichen erwartet")
                return False
        elif self.match(print_set, st):
            if self.match(ident_set, st):
                if self.match(eol_set, st):
                    return True
                else:
                    self.syntax_error("EOL Zeichen erwartet!!!")
                    return False
            else:
                self.syntax_error("Variable erwartet")
                return False
        elif self.expression(st.insert_subtree(TOKEN.EXPRESSION, get_semantic_function(TOKEN.EXPRESSION))):
            if self.match(eol_set, st):
                return True
            else:
                self.syntax_error("EOL Zeichen erwartet!!!")
                return False
        else:
            self.syntax_error("Fehler in Ausdruck")
            return False

    # expression -> term rightExpression
    def expression(self, st: SyntaxTree) -> bool:
        return \
            self.term(st.insert_subtree(TOKEN.TERM, get_semantic_function(TOKEN.TERM))) \
            and self.right_expression(
                st.insert_subtree(TOKEN.RIGHT_EXPRESSION, get_semantic_function(TOKEN.RIGHT_EXPRESSION)))

    # rightExpression -> plus term rightExpression
    # rightExpression -> minus term rightExpression
    # rightExpression -> Epsilon
    def right_expression(self, st: SyntaxTree) -> bool:
        add_set = [TOKEN.ADD]
        sub_set = [TOKEN.SUB]

        if self.match(add_set, st):
            return \
                self.term(st.insert_subtree(TOKEN.TERM, get_semantic_function(TOKEN.TERM))) \
                and self.right_expression(
                    st.insert_subtree(TOKEN.RIGHT_EXPRESSION, get_semantic_function(TOKEN.RIGHT_EXPRESSION)))
        elif self.match(sub_set, st):
            return \
                self.term(st.insert_subtree(TOKEN.TERM, get_semantic_function(TOKEN.TERM))) \
                and self.right_expression(
                    st.insert_subtree(TOKEN.RIGHT_EXPRESSION, get_semantic_function(TOKEN.RIGHT_EXPRESSION)))
        else:
            st.insert_subtree(
                TOKEN.EPSILON, get_semantic_function(TOKEN.EPSILON))
            return True

    # term -> operator rightTerm
    def term(self, st: SyntaxTree) -> bool:
        return \
            self.operator(st.insert_subtree(TOKEN.OPERATOR, get_semantic_function(TOKEN.OPERATOR))) \
            and self.right_term(st.insert_subtree(TOKEN.RIGHT_TERM, get_semantic_function(TOKEN.RIGHT_TERM)))

    # rightTerm -> mult operator rightTerm
    # rightTerm -> div operator rightTerm
    # rightTerm -> Epsilon
    def right_term(self, st: SyntaxTree) -> bool:
        mul_set = [TOKEN.MUL]
        div_set = [TOKEN.DIV]

        if self.match(mul_set, st):
            return \
                self.operator(st.insert_subtree(TOKEN.OPERATOR, get_semantic_function(TOKEN.OPERATOR))) \
                and self.right_term(st.insert_subtree(TOKEN.RIGHT_TERM, get_semantic_function(TOKEN.RIGHT_TERM)))
        elif self.match(div_set, st):
            return \
                self.operator(st.insert_subtree(TOKEN.OPERATOR, get_semantic_function(TOKEN.OPERATOR))) \
                and self.right_term(st.insert_subtree(TOKEN.RIGHT_TERM, get_semantic_function(TOKEN.RIGHT_TERM)))
        else:
            st.insert_subtree(
                TOKEN.EPSILON, get_semantic_function(TOKEN.EPSILON))
            return True

    # operator -> openPar expression closePar | num | ident | boolExpression
    def operator(self, st: SyntaxTree) -> bool:
        open_par_set = [TOKEN.OPEN_PAR]
        close_par_set = [TOKEN.CLOSE_PAR]
        num_set = [TOKEN.NUMBER]
        ident_set = [TOKEN.IDENT]

        if self.match(open_par_set, st):
            if self.expression(st.insert_subtree(TOKEN.EXPRESSION, get_semantic_function(TOKEN.EXPRESSION))):
                if self.match(close_par_set, st):
                    return True
                else:
                    self.syntax_error("Schließende Klammer erwartet")
                    return False
            else:
                self.syntax_error("Fehler in verschachteltem Ausdruck")
                return False
        elif self.match(num_set, st):
            return True
        elif self.match(ident_set, st):
            return True
        else:
            self.syntax_error("Öffnende Klammer erwartet")
            return False  # TODO: SyntaxError

    def look_ahead(self, look_ahead_set: list['TOKEN']) -> bool:
        for el in look_ahead_set:
            if self.tokens[self.current_token_pointer + 1].token == el:
                return True
        return False

    def match(self, match_set: list[TOKEN], st: SyntaxTree) -> bool:
        for el in match_set:
            if self.tokens[self.current_token_pointer].token == el:
                st.insert_subtree(
                    self.tokens[self.current_token_pointer].token,
                    get_semantic_function(
                        self.tokens[self.current_token_pointer].token),
                    self.tokens[self.current_token_pointer])
                self.current_token_pointer += 1
                return True
        return False

    def syntax_error(self, s: str) -> None:
        if self.tokens[self.current_token_pointer].token == TOKEN.EOF:
            print("Syntaxfehler: EOF")
        else:
            print("Syntaxfehler: " +
                  self.tokens[self.current_token_pointer].token.name)
        print("" if s is None else s)


def get_semantic_function(t: TOKEN) -> Semantic | None:
    match t:
        case TOKEN.EXPRESSION:
            return Expression()
        case TOKEN.IDENT:
            return Ident()
        case TOKEN.NUMBER:
            return Num()
#        case TOKEN.TRUE:
#            return Boolean()
#        case TOKEN.FALSE:
#            return Boolean()
        case TOKEN.OPERATOR:
            return Operator()
        case TOKEN.PROGRAM:
            return Program()
        case TOKEN.RIGHT_EXPRESSION:
            return RightExpression()
        case TOKEN.RIGHT_TERM:
            return RightTerm()
        case TOKEN.STATEMENT:
            return Statement()
        case TOKEN.TERM:
            return Term()
        case TOKEN.EOL:
            return EOL()
        case TOKEN.EOF:
            return EOF()
        case TOKEN.EPSILON:
            return Epsilon()
        case _:
            return None
