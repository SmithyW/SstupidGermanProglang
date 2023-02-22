from langParser import Parser
from lex_token import TOKEN
from lexer import Lexer
from syntax_tree import SyntaxTree

# Beispiel input, der verarbeitet wird
input_text = """
1-1*2!
ZAHL xyz := 50 * (60+2) - 7!
"""
# Instanz eines lexers erstellen.
# Dem Konstruktur wird der Inputtext übergeben
lexer = Lexer(input_text)

# Den Input auslesen und jeden einzelnen
# Character als Instanz der InputCharacter Klasse speichern
lexer.read_input()

# Den Inputtext in die entsprechenden Token umwandeln
# und ggf. Fehler werfen
lexer.tokenize()

# Token in der Konsole ausgeben (alle Terminalsymbole)
print("!!!### ERKANNTE TOKEN ###!!!")
for token in lexer.tokens:
    print(f"TOKEN: {token.token_type.name}, WERT: {token.value}")

# Instanz eines Parsers erstellen.
# Dafür die Tokenliste des lexers übergeben
parser = Parser(lexer.tokens)

# Eine Instanz eines Syntaxbaumes erzeugen
# Als Top-Level Element das Nichtterminalsymbol "PROGRAM" übergeben
parseTree = SyntaxTree(TOKEN.PROGRAM)

# Den Input in Form der Tokenliste parsen
# Den gerade erzeugten Syntaxbaum dem Konstruktor übergeben
parser.parse(parseTree)

# Den fertigen Syntaxbaum inkl. aller
# Kindelemente ausgeben
parseTree.print_syntax_tree(0)

# TODO: Codegen (Dafür werden noch die semantischen Funktionen in den (Nicht-)terminalsymbolen benötigt
