from lex_token import Token, DslToken, TokenDefinition, TOKEN, TokenMatch

# ACHTUNG: Die Klasse InputCharacter
# wird aktuell noch nicht weiterverwendet


class InputCharacter:
    """
    Klasse, die jedes Zeichen eines Inputs
    inkl. Zeile zwischenspeichert
    """
    def __init__(self, c: str, l: int):
        self.character = c
        self.line = l


class Lexer:
    """
    Der Lexer extrahiert alle Token aus dem
    übergebenen Inputtext
    """
    # Definition des End-Of-File characters
    EOF = chr(255)

    def __init__(self, input_text: str):
        # Der Inputtext (Source code)
        self.input: str = input_text
        # Die aktuelle Position im Inputtext
        self.current_pos: int = 0

        # Liste aller Inputcharacters
        # Aktuell ohne Verwendung
        self.input_characters: list['InputCharacter'] = []
        # Liste aller erkannten Token
        # Diese wird im Laufe des "lexens"
        # gefüllt
        self.tokens: list['DslToken'] = []

        self.__token_definitions: list['TokenDefinition'] = list()
        # Jedes Terminalsymbol inkl. regulärem
        # Ausdruck registrieren
        self.__token_definitions.append(TokenDefinition(TOKEN.IDENT, r'^[a-z]+'))
        self.__token_definitions.append(TokenDefinition(TOKEN.NUMBER, r'^[0-9]+'))
        self.__token_definitions.append(TokenDefinition(TOKEN.ASSIGN, r'^:='))
        self.__token_definitions.append(TokenDefinition(TOKEN.ADD, r'^\+'))
        self.__token_definitions.append(TokenDefinition(TOKEN.SUB, r'^\-'))
        self.__token_definitions.append(TokenDefinition(TOKEN.MUL, r'^\*'))
        self.__token_definitions.append(TokenDefinition(TOKEN.DIV, r'^\/'))
        self.__token_definitions.append(TokenDefinition(TOKEN.OPEN_PAR, r'^\('))
        self.__token_definitions.append(TokenDefinition(TOKEN.CLOSE_PAR, r'^\)'))
        self.__token_definitions.append(TokenDefinition(TOKEN.PRINT, r'^DRUCKE'))
        self.__token_definitions.append(TokenDefinition(TOKEN.INT, r'^ZAHL'))
        self.__token_definitions.append(TokenDefinition(TOKEN.STR, r'^ZEICHENKETTE'))
        self.__token_definitions.append(TokenDefinition(TOKEN.EOL, r'^!'))
        self.__token_definitions.append(TokenDefinition(TOKEN.EOF, r'^' + self.EOF))

    def read_input(self) -> bool:
        """
        Liest den Inputtext aus und speichert
        die erkannten characters als Instanz
        der Klasse InputCharacter ab.
        Der letzte char wird automatisch als
        EOF character hinzugefügt.
        :return:
        """
        c = -1
        line = 1

        while True:
            if len(self.input) < self.current_pos:
                break
            try:
                c = self.input[self.current_pos]
            except IndexError:
                c = self.EOF
            # ord gibt den Dezimalwert eines chars zurück
            # 13 ist linefeed
            if ord(c) == 13:
                continue
            else:
                self.input_characters.append(InputCharacter(c, line))
                if c == self.EOF:
                    break
                elif c == '\n':
                    line += 1
                self.current_pos += 1
        # Zurücksetzen der current_pos fürs tokenizing
        self.current_pos = 0

    def tokenize(self) -> None:
        """
        Sucht nach den passenden Token für jedes einzelne
        Element im Inputtext
        :return: Nichts
        """
        tokens: list['DslToken'] = list()
        remaining_text: str = self.input

        # Solange noch "remaining_text" vorhanden ist
        # wird weiterverarbeitet
        while remaining_text is not None and remaining_text.strip() != "":
            # lstrip entfernt alle new lines, tabs und Leerzeichen auf der linken
            # Seite eines strings
            remaining_text = remaining_text.lstrip()
            match = self.__find_match(remaining_text)
            if match.is_match:
                tokens.append(DslToken(match.token, match.value))
                remaining_text = match.remaining_text
            else:
                msg = f"{remaining_text.split(' ')[0]} kann keinem Token zugewiesen werden."
                raise Exception(msg)
                remaining_text = remaining_text[1:]
        tokens.append(DslToken(TOKEN.EOF, self.EOF))  # Achtung Krücke
        self.tokens = tokens

    def __find_match(self, remaining_text: str):
        """
        Sucht in den token Definitionen nach einem
        passenden Token für den aktuellen verbliebenen Text
        :param remaining_text:
        :return:
        """
        for td in self.__token_definitions:
            match = td.match(remaining_text)
            if match.is_match:
                return match
        
        return TokenMatch(is_match=False)


