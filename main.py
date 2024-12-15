import sys
import langParser
from langParser import Parser
from lex_token import TOKEN
from lexer import Lexer
from syntax_tree import SyntaxTree
from symbol_table_codegen import SymbolTableCodegen

# Beispiel input, der verarbeitet wird
INPUT_TEXT = """ZAHL a := 2 * 4 + 3!
ZAHL b := 2 * 5!
ZAHL c := a * b!
ZAHL d := 5!
a := 2!
"""

# Instanz eines lexers erstellen.
# Dem Konstruktur wird der Inputtext übergeben
lexer = Lexer(INPUT_TEXT)

# Den Input auslesen und jeden einzelnen
# Character als Instanz der InputCharacter Klasse speichern
lexer.read_input()
# Input Characters als Array ausgeben
print([str(x.character) for x in lexer.input_characters])
# Den Inputtext in die entsprechenden Token umwandeln
# und ggf. Fehler werfen
lex_success = lexer.tokenize()

print("!!!### Symboltabelle nach dem Scannen ###!!!")
lexer.symbol_table.print()

# Programm beenden, wenn Fehler aufgetreten sind
if not lex_success:
    print("Kompilierung aufgrund von Fehlern im Scanner beendet.")
    sys.exit(1)

# Token in der Konsole ausgeben (alle Terminalsymbole inkl. Zeile und Position in Zeile)
print("!!!### ERKANNTE TOKEN ###!!!")
for token in lexer.tokens:
    print(token)

# Instanz eines Parsers erstellen.
# Dafür die Tokenliste des lexers übergeben
parser = Parser(lexer.tokens)

# Eine Instanz eines Syntaxbaumes erzeugen
# Als Top-Level Element das Nichtterminalsymbol "PROGRAM" übergeben
parseTree = SyntaxTree(
    TOKEN.PROGRAM, langParser.get_semantic_function(TOKEN.PROGRAM))

# Den Input in Form der Tokenliste parsen
# Den gerade erzeugten Syntaxbaum dem Konstruktor übergeben
parser.parse(parseTree)

# Den fertigen Syntaxbaum inkl. aller
# Kindelemente ausgeben
parseTree.print_syntax_tree(0)

# Semantische Funktionen ausführen
print("Input: " + INPUT_TEXT)

sym = SymbolTableCodegen(lexer.symbol_table)
parseTree.value.p(parseTree, sym, None)
sym.print()
