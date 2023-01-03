from lex_token import TOKEN


class SyntaxTree:
    """
    Klasse des Syntaxbaums
    Enthält die Eigenschaften:
    - childNodes: Kind-Knoten in Form von Syntaxbäumen
    - token: Token, das diesem Knoten zugeordnet ist
        * Dabei kann es ein Terminal- oder Nichtterminalsymbol sein
    """
    def __init__(self, t: TOKEN):
        self.childNodes: list[SyntaxTree] = []
        self.token = t
        # TODO: Set semantic function

    def print_syntax_tree(self, t: int) -> None:
        """
        Gibt den aktuellen Knoten in der Konsole aus
        :param t: Anzahl der "Tabs" (Indents)
        :return: Nichts
        """
        for i in range(0, t):
            print("  ", end="")
        print(self.token.name)

        for i in range(0, len(self.childNodes)):
            self.childNodes[i].print_syntax_tree(t+1)

    def insert_subtree(self, token: TOKEN) -> 'SyntaxTree':
        """
        Fügt diesem Syntaxbaum einen Kindknoten hinzu
        :param token: Token des neuen Kindelements
        :return: Den neuen Kindknoten
        """
        node = SyntaxTree(token)
        self.childNodes.append(node)
        return node

    def get_child(self, i: int) -> 'SyntaxTree':
        """
        Gibt ein Kindelement dieses Syntaxbaums zurück
        :param i: Index des gewünschten Kindelements
        :return: Das gewünschte Kindelement
        """
        if i > len(self.childNodes):
            return None
        else:
            return self.childNodes[i]

