from syntax_highligther.tokens import Token, Tag
from syntax_highligther.scanner import Scanner


class Highlighter:
    def __init__(self, coloring: dict[Tag, str] = None) -> None:
        self.coloring = coloring
        if not coloring:
            self.set_default_coloring()

    def set_coloring(self, coloring: dict[Tag, str]) -> None:
        self.coloring = coloring

    def set_default_coloring(self) -> None:
        self.coloring = {
            'Callable': 'Orchid',
            'Class': 'Gold',
            'Identifier': 'Orange',
            'Keyword': 'IndianRed',
            'Number': 'DeepSkyBlue',
            'String': 'SkyBlue',
            'Operator': 'LightSeaGreen',
            'Comment': '#83929a',
            'Other': '#83929a',
            'Decorator': 'IndianRed'
        }

    def highlight(self, filename: str) -> str:
        html = '<!DOCTYPE html> ' \
               '<html> <head> ' \
               '<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sofia">' \
               '</head> ' \
               '<body style="background-color:#22272e; font-family: "JetBrains Mono"; font-size: 16px;">\n'

        with open(filename, 'r') as file:
            scanner = Scanner(file)
            while not scanner.ended():
                token = scanner.scan()
                if token:
                    html += self.color(token)

        html += '</body> </html> '
        return html

    def color(self, token: Token) -> str:
        if token.tag.value == "Newline":
            html = '<br>\n'
        elif token.tag.value == "Whitespace":
            html = '&nbsp;'
        else:
            html = f'<code style="color: {self.coloring[token.tag.value]}">{token.value}</code>'
        return html


if __name__ == '__main__':
    filenames = ['examples/helloworld.py', 'examples/blank.py', 'highlighter.py']

    highlighter = Highlighter()
    for filename in filenames:
        html_filename = filename.replace('.py', '.html')
        with open(html_filename, 'w') as output:
            output.write(highlighter.highlight(filename))
