from typing import TextIO

from tokens import Token, Tag


class Scanner:
    def __init__(self, file: TextIO) -> None:
        self.file: TextIO = file
        self._read_character()

    def ended(self) -> bool:
        return not self.peek

    def scan(self) -> Token:
        # whitespaces
        if self.peek.isspace():
            # newlines
            if self.peek == '\n':
                self._read_character()
                return Token(Tag.NEWLINE, '\n')
            value = self.peek
            self._read_character()
            return Token(Tag.WHITESPACE, value)

        # numbers
        if self.peek.isdigit():
            value = ''
            while self.peek.isdigit():
                value += self.peek
                self._read_character()

            if self.peek != '.':
                return Token(Tag.NUMBER, value)

            value += self.peek

            self._read_character()
            while self.peek.isdigit():
                value += self.peek
                self._read_character()

            return Token(Tag.NUMBER, value)

        # identifiers
        if self.peek.isalpha() or self.peek == '_':
            value = ""
            while self.peek.isalnum() or self.peek == '_':
                value += self.peek
                self._read_character()

            if value in Token.keywords:
                return Token(Tag.KEYWORD, value)
            elif value[0].isupper():
                return Token(Tag.CLASS, value)
            elif self.peek == '(':
                return Token(Tag.CALLABLE, value)
            else:
                return Token(Tag.IDENTIFIER, value)

        # strings
        if self.peek == '\'' or self.peek == '"':
            quote = self.peek
            value = self.peek
            self._read_character()
            while self.peek != quote:
                value += self.peek
                self._read_character()
            value += self.peek
            self._read_character()
            return Token(Tag.STRING, value)

        # comments
        if self.peek == '#':
            value = ''
            while self.peek != '\n':
                value += self.peek
                self._read_character()
            return Token(Tag.COMMENT, value)

        # decorators
        if self.peek == '@':
            value = ''
            while self.peek != '\n':
                value += self.peek
                self._read_character()
            return Token(Tag.DECORATOR, value)

        # operators
        if self.peek in Token.operators:
            value = self.peek
            self._read_character()

            # typing arrow
            if value + self.peek == '->':
                value += self.peek
                self._read_character()
                return Token(Tag.OTHER, value)

            if value + self.peek in Token.operators:
                value += self.peek
                self._read_character()

                if value + self.peek in Token.operators:
                    value += self.peek
                    self._read_character()

            return Token(Tag.OPERATOR, value)

        # other
        value = self.peek
        self._read_character()
        return Token(Tag.OTHER, value)

    def _read_character(self) -> None:
        self.peek = self.file.read(1)


if __name__ == '__main__':
    filenames = ['examples/helloworld.py', 'examples/blank.py']

    for filename in filenames:
        with open(filename, 'r') as file:
            scanner = Scanner(file)
            while not scanner.ended():
                try:
                    token = scanner.scan()
                    if token:
                        print(token)
                except Exception as e:
                    print(e)
            print()
