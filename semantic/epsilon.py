from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from syntax_tree import SyntaxTree

from semantic import Semantic


class Epsilon(Semantic):

    def __init__(self):
        super().__init__()

    def f(self, st: SyntaxTree, n: int):
        return n
