from lex_token import Token, DslToken, TokenDefinition, TOKEN, TokenMatch

# ACHTUNG: Die Klasse InputCharacter
# wird aktuell noch nicht weiterverwendet


class InputCharacter:
    """
    Klasse, die jedes Zeichen eines Inputs
    inkl. Zeile zwischenspeichert
    """
    def __init__(self, c: str, l: int, p: int):
        self.character = c
        self.line = l
        self.pos = p


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
        self.tokens: list['Token'] = []

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
        pos_in_line = 1

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
                self.input_characters.append(InputCharacter(c, line, pos_in_line))
                if c == self.EOF:
                    break
                elif c == '\n':
                    line += 1
                    pos_in_line = 0
                self.current_pos += 1
                pos_in_line += 1
        # Zurücksetzen der current_pos fürs tokenizing
        self.current_pos = 0

    def tokenize(self) -> None:
        """
        Sucht nach den passenden Token für jedes einzelne
        Element im Inputtext
        :return: Nichts
        """
        tokens: list['Token'] = list()
        # characters der Input_characters als zusammengeführter string
        remaining_text: str = ''.join(str(x.character) for x in self.input_characters)

        # Solange noch "remaining_text" vorhanden ist
        # wird weiterverarbeitet
        while remaining_text is not None and remaining_text.strip() != "":
            # lstrip entfernt alle new lines, tabs und Leerzeichen auf der linken
            # Seite eines strings
            remaining_text = remaining_text.lstrip()
            match = self.__find_match(remaining_text)
            if match.is_match:
                # neuen remaining_text einstellen
                remaining_text = match.remaining_text
                # position und line des gematchten lexemes ermitteln
                line, pos = self.get_line_pos(remaining_text, len(match.value))
                tokens.append(Token(match.token, match.value, line, pos))
            else:
                msg = f"{remaining_text.split(' ')[0]} kann keinem Token zugewiesen werden."
                raise Exception(msg)
                remaining_text = remaining_text[1:]
        self.tokens = tokens

    def get_line_pos(self, remaining_text: str, len_lexeme: int):
        diff: int = len(self.input_characters) - len(remaining_text) - len_lexeme
        return self.input_characters[diff].line, self.input_characters[diff].pos


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


