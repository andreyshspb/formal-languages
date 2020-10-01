
from lexer import Lexer

import sys


class Parser:

    def __init__(self, string: str):
        self.lexer = Lexer(string)
        self.current_token = next(self.lexer)

        while self.current_token is not None:
            result = self.Definition()
            if not result:
                return

        print("OK")

    def accept(self, element: str) -> bool:
        if self.current_token is None:
            return False

        if self.current_token.value == element:
            self.current_token = next(self.lexer)
            return True

        return False

    def expect(self, element: str) -> bool:
        if self.current_token is None:
            print("Expected", element, "in the end")
            return False

        if self.current_token.value == element:
            self.current_token = next(self.lexer)
            return True

        print("Expected", element, f'at line: {self.current_token.lineno}, '
                                   f'pos: {self.current_token.lexpos}')
        return False

    def Literal(self) -> bool:
        if self.current_token is None:
            print("Expected literal in the end")
            return False

        if self.accept('('):
            return self.Disjunction() and self.expect(')')

        if str(self.current_token.type) != 'ID':
            print(f'Expected literal at line: {self.current_token.lineno}, '
                  f'pos: {self.current_token.lexpos}')
            return False

        self.current_token = next(self.lexer)
        return True

    def Disjunction(self) -> bool:
        if not self.Conjunction():
            return False
        if self.accept(';'):
            return self.Disjunction()
        return True

    def Conjunction(self) -> bool:
        if not self.Literal():
            return False
        if self.accept(','):
            return self.Conjunction()
        return True

    def Definition(self) -> bool:
        if not self.Literal():
            return False
        if self.accept(':-'):
            return self.Disjunction() and self.expect('.')
        return self.expect('.')


def main(filename: str):
    with open(filename, 'r') as file:
        data = file.read()

    Parser(data)


if __name__ == "__main__":
    main(sys.argv[1])

