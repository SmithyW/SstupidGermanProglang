
"""
    Grammatik:
    program -> statement program | statement
    statement -> (assignment | print | expression) eol # TODO: Nochmal schauen, weil anders implementiert
    assignment -> var ident assign expression # TODO: Anders implementiert
    var -> int | str # TODO: Anders implementiert
    assign -> := # TODO: Anders implementiert
    print -> print ident # TODO: Anders implementiert
    expression -> term rightExpression
    rightExpression -> plus term rightExpression
    rightExpression -> minus term rightExpression
    rightExpression -> Epsilon
    term -> operator rightTerm
    rightTerm -> mult operator rightTerm
    rightTerm -> div operator rightTerm
    rightTerm -> Epsilon
    operator -> openPar expression closePar | num | ident
"""
from lexer import TOKEN, DslToken
from syntax_tree import SyntaxTree


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
        self.tokens: list['DslToken'] = tokens
        self.current_token_pointer: int = 0
        self.parse_tree: SyntaxTree = None

    def parse(self, parse_tree: SyntaxTree):
        # Parsen wird an dieser Stelle mit dem übergebenen initialen
        # Syntaxtbaums gestartet
        if self.program(parse_tree):
            return True
        else:
            self.syntax_error("Error in Program")
            return False

    # program -> statement program | statement
    def program(self, st: SyntaxTree) -> bool:
        eof_set = [TOKEN.EOF]
        while not self.match(eof_set, st):
            if not self.statement(st.insert_subtree(TOKEN.STATEMENT)):
                self.syntax_error("Error in statement")
                return False
        return True

    # statement -> (assignment | print | expression) eol
    # statement -> var ident assign expression eol
    # statement -> print ident eol
    # statement -> expression eol
    def statement(self, st: SyntaxTree) -> bool:
        var_set = [TOKEN.STR, TOKEN.INT]
        print_set = [TOKEN.PRINT]
        ident_set = [TOKEN.IDENT]
        eol_set = [TOKEN.EOL]
        assign_set = [TOKEN.ASSIGN]

        if self.match(var_set, st):
            if self.match(ident_set, st):
                if self.match(assign_set, st):
                    if self.expression(st.insert_subtree(TOKEN.EXPRESSION)):
                        if self.match(eol_set, st):
                            return True
                        else:
                            self.syntax_error("Expected EOL character")
                            return False
                    else:
                        self.syntax_error("Error in expression")
                        return False
                else:
                    self.syntax_error("Expected assign token")
                    return False
            else:
                self.syntax_error("Expected identifier")
                return False
        elif self.match(print_set, st):
            if self.match(ident_set, st):
                if self.match(eol_set, st):
                    return True
                else:
                    self.syntax_error("Expected EOL character")
                    return False
            else:
                self.syntax_error("Expected identifier")
                return False
        elif self.expression(st.insert_subtree(TOKEN.EXPRESSION)):
            if self.match(eol_set, st):
                return True
            else:
                self.syntax_error("Expected EOL character")
                return False
        else:
            self.syntax_error("Error in expression")
            return False

    # expression -> term rightExpression
    def expression(self, st: SyntaxTree) -> bool:
        return \
                self.term(st.insert_subtree(TOKEN.TERM)) \
                and self.right_expression(st.insert_subtree(TOKEN.RIGHT_EXPRESSION))

    # rightExpression -> plus term rightExpression
    # rightExpression -> minus term rightExpression
    # rightExpression -> Epsilon
    def right_expression(self, st: SyntaxTree) -> bool:
        add_set = [TOKEN.ADD]
        sub_set = [TOKEN.SUB]

        if self.match(add_set, st):
            return \
                    self.term(st.insert_subtree(TOKEN.TERM)) \
                    and self.right_expression(st.insert_subtree(TOKEN.RIGHT_EXPRESSION))
        elif self.match(sub_set, st):
            return \
                    self.term(st.insert_subtree(TOKEN.TERM)) \
                    and self.right_expression(st.insert_subtree(TOKEN.RIGHT_EXPRESSION))
        else:
            st.insert_subtree(TOKEN.EPSILON)
            return True

    # term -> operator rightTerm
    def term(self, st: SyntaxTree) -> bool:
        return \
                self.operator(st.insert_subtree(TOKEN.OPERATOR)) \
                and self.right_term(st.insert_subtree(TOKEN.RIGHT_TERM, "halloLOOL"))

    # rightTerm -> mult operator rightTerm
    # rightTerm -> div operator rightTerm
    # rightTerm -> Epsilon
    def right_term(self, st: SyntaxTree) -> bool:
        mul_set = [TOKEN.MUL]
        div_set = [TOKEN.DIV]

        if self.match(mul_set, st):
            return \
                    self.operator(st.insert_subtree(TOKEN.OPERATOR)) \
                    and self.right_term(st.insert_subtree(TOKEN.RIGHT_TERM))
        elif self.match(div_set, st):
            return \
                    self.operator(st.insert_subtree(TOKEN.OPERATOR)) \
                    and self.right_term(st.insert_subtree(TOKEN.RIGHT_TERM))
        else:
            st.insert_subtree(TOKEN.EPSILON)
            return True

    # operator -> openPar expression closePar | num | ident
    def operator(self, st: SyntaxTree) -> bool:
        open_par_set = [TOKEN.OPEN_PAR]
        close_par_set = [TOKEN.CLOSE_PAR]
        num_set = [TOKEN.NUMBER]
        ident_set = [TOKEN.IDENT]

        if self.match(open_par_set, st):
            if self.expression(st.insert_subtree(TOKEN.EXPRESSION)):
                if self.match(close_par_set, st):
                    return True
                else:
                    self.syntax_error("Expected closing parenthesis")
                    return False
            else:
                self.syntax_error("Error in nested expression")
                return False
        elif self.match(num_set, st):
            return True
        elif self.match(ident_set, st):
            return True
        else:
            self.syntax_error("Expected opening parenthesis")
            return False  # TODO: SyntaxError

    def look_ahead(self, look_ahead_set: list['TOKEN']) -> bool:
        for el in look_ahead_set:
            if self.tokens[self.current_token_pointer + 1].token_type == el:
                return True
        return False

    def match(self, match_set: list[TOKEN], st: SyntaxTree) -> bool:
        for el in match_set:
            if self.tokens[self.current_token_pointer].token_type == el:
                st.insert_subtree(self.tokens[self.current_token_pointer].token_type, self.tokens[self.current_token_pointer].value)
                self.current_token_pointer += 1
                return True
        return False

    def syntax_error(self, s: str) -> None:
        if self.tokens[self.current_token_pointer].token_type == TOKEN.EOF:
            print("Syntax error: EOF")
        else:
            print("Syntax error: " + self.tokens[self.current_token_pointer].token_type.name)
        print("" if s is None else s)
