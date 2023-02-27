import langParser
from langParser import Parser
from lex_token import TOKEN
from lexer import Lexer
from syntax_tree import SyntaxTree
from semantic.semantic import Semantic

# Beispiel input, der verarbeitet wird
input_text = """10-2+5-6+1!"""
# Instanz eines lexers erstellen.
# Dem Konstruktur wird der Inputtext übergeben
lexer = Lexer(input_text)

# Den Input auslesen und jeden einzelnen
# Character als Instanz der InputCharacter Klasse speichern
lexer.read_input()
# Input Characters als Array ausgeben
print([str(x.character) for x in lexer.input_characters])
# Den Inputtext in die entsprechenden Token umwandeln
# und ggf. Fehler werfen
lexer.tokenize()

# Token in der Konsole ausgeben (alle Terminalsymbole inkl. Zeile und Position in Zeile)
print("!!!### ERKANNTE TOKEN ###!!!")
for token in lexer.tokens:
    print(token)

# Instanz eines Parsers erstellen.
# Dafür die Tokenliste des lexers übergeben
parser = Parser(lexer.tokens)

# Eine Instanz eines Syntaxbaumes erzeugen
# Als Top-Level Element das Nichtterminalsymbol "PROGRAM" übergeben
parseTree = SyntaxTree(TOKEN.PROGRAM, langParser.get_semantic_function(TOKEN.PROGRAM))

# Den Input in Form der Tokenliste parsen
# Den gerade erzeugten Syntaxbaum dem Konstruktor übergeben
parser.parse(parseTree)

# Den fertigen Syntaxbaum inkl. aller
# Kindelemente ausgeben
parseTree.print_syntax_tree(0)

# Semantische Funktionen ausführen
print("Input: " + input_text)
print("Output (semantische Funktionen): " + str(parseTree.value.f(parseTree, Semantic().UNDEFINED)))
# TODO: Codegen (Dafür werden noch die semantischen Funktionen in den (Nicht-)terminalsymbolen benötigt
