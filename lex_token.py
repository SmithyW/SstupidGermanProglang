from enum import Enum
import re


class TOKEN(Enum):
    """
    Enum für alle Terminal und Nichtterminalsymbole
    (Die Nummerierung ist relativ willkürlich, soll aber einigermaßen kategorisiert sein)
    """
    # basic types
    NONE = 0            # Kein bekanntes Token
    IDENT = 1           # Ident
    NUMBER = 2          # Zahl
    BOOLEAN = 3            # Bool

    # reserved symbols
    ASSIGN = 10             # :=
    ADD = 11                # +
    SUB = 12                # -
    MUL = 13                # *
    DIV = 14                # /
    OPEN_PAR = 15           # (
    CLOSE_PAR = 16          # )
    OPEN_RECT_PAR = 17      # [
    CLOSE_RECT_PAR = 18     # ]
    COMPARE_EQ = 19         # ?=
    COMPARE_GT = 20         # ?>
    COMPARE_LT = 21         # ?<
    COMPARE_GTE = 22        # ?>?=
    COMPARE_LTE = 23        # ?<?=
    COMPARE_NOT = 24        # ?-=

    # keywords
    PRINT = 40          # DRUCKE keyword
    INT = 41            # ZAHL Keyword
    STR = 42            # ZEICHENKETTE keyword
    WHEN = 43           # FALLS keyword
    THEN = 44           # DANN keyword
    ELSE = 45           # ANSONSTEN keyword
    TRUE = 46           # WAHR keyword
    FALSE = 47          # FALSCH keyword
    AND = 48            # UND keyword
    OR = 49             # ODER keyword
    NOT = 50            # NICHT keyword

    # non-terminal symbols
    PROGRAM = 100
    STATEMENT = 101
    ASSIGNMENT = 102
    PRINTN = 103
    # PRINTN vs PRINT: PRINTN ist Nichtterminal,
    # PRINT Terminalsymbol
    EXPRESSION = 104
    RIGHT_EXPRESSION = 105
    TERM = 106
    RIGHT_TERM = 107
    OPERATOR = 108
    EPSILON = 109
    BOOL_EXPRESSION = 110
    BOOL_TERM = 111
    RIGHT_BOOL = 112
    COMPARISON = 113

    # others
    EOL = 900           # EndOfLine (!)
    EOF = 999           # EndOfFile


class Token:
    """
    Klasse, die Informationen zu jedem Token im Input enthält
    """
    def __init__(self, token: TOKEN, lexeme: str, line: int, pos: int):
        self.token = token  # Token
        self.lexeme = lexeme  # Dem Token zugehöriger Teilstring
        self.line = line  # Zeile, in der das Token vorkommt
        self.pos = pos  # Position, in der das Token vorkommt

    def __str__(self):
        # String, der beim Aufruf von str("Instanz von Token") ausgegeben werden soll
        return f"Token: {self.token.name}; lexeme: {self.lexeme}; Line: {self.line}; Starts at: {self.pos}"


class TokenDefinition:
    """
    Definiert ein Token: Welcher reguläre Ausruck weist auf welches Token hin
    """
    def __init__(self, token_type: TOKEN, regex_pattern: str) -> None:
        self.__regex_pattern = regex_pattern
        self.__returnsToken = token_type

    def match(self, input_string: str):
        match = re.search(self.__regex_pattern, input_string)
        if match is not None:
            if match.span()[1] <= len(input_string):
                remaining_text = input_string[match.span()[1]:]

                return TokenMatch(
                    is_match=True,
                    remaining_text=remaining_text,
                    token=self.__returnsToken,
                    value=input_string[match.span()[0]:match.span()[1]])
        else:
            return TokenMatch(
                is_match=False,
            )


class TokenMatch:
    """
    Hilfsobjekt zur Weiterverarbeitung im lexer
    """
    def __init__(
        self, 
        is_match: bool, 
        token: TOKEN = None, 
        value: str = None, 
        remaining_text: str = None
    ) -> None:
        self.is_match: bool = is_match
        self.token: TOKEN = token
        self.value: str = value
        self.remaining_text: str = remaining_text
    

class DslToken:

    def __init__(self, token_type: TOKEN, value: str = "") -> None:
        self.token_type = token_type
        self.value = value
    
    def clone(self):
        return DslToken(self.token_type, self.value)
