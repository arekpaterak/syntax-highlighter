import keyword
from enum import Enum


class Tag(Enum):
    WHITESPACE = 'Whitespace'
    NEWLINE = 'Newline'
    CLASS = 'Class'
    CALLABLE = 'Callable'
    KEYWORD = 'Keyword'
    IDENTIFIER = 'Identifier'
    NUMBER = 'Number'
    STRING = 'String'
    OPERATOR = 'Operator'
    COMMENT = 'Comment'
    DECORATOR = 'Decorator'
    OTHER = 'Other'


class Token:
    keywords: list[str] = keyword.kwlist
    operators: set[str] = {'+', '-', '*', '/', '%', '//', '**',
                           '==', '!=', '>', '<', '>=', '<=',
                           '&', '|', '^', '~', '<<', '>>',
                           '=', '+=', '-=', '*=', '/=', '%=',
                           '//=', '**=', '&=', '|=', '^=', '>>=', '<<='}

    def __init__(self, name: Tag, value: str) -> None:
        self.tag: Tag = name
        self.value: str = value

    def __str__(self) -> str:
        return f'({self.tag}, {self.value})'
