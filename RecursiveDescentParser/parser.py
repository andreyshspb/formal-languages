
from lexer import to_lex

import sys


class Parser:

    def __init__(self, string: str):
        self.lexer = to_lex(string)
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
            block = self.Disjunction()
            if block and self.expect(')'):
                return True
            return False

        if str(self.current_token.type) != 'ID':
            print(f'Expected literal at line: {self.current_token.lineno}, '
                  f'pos: {self.current_token.lexpos}')
            return False

        self.current_token = next(self.lexer)
        return True

    def Disjunction(self) -> bool:
        left = self.Conjunction()
        if not left:
            return False

        if self.accept(';'):
            right = self.Disjunction()
            if not right:
                return False
            return True

        return True

    def Conjunction(self) -> bool:
        left = self.Literal()
        if not left:
            return False

        if self.accept(','):
            right = self.Conjunction()
            if not right:
                return False
            return True

        return True

    def Definition(self) -> bool:
        head = self.Literal()
        if not head:
            return False

        if self.accept(':-'):
            body = self.Disjunction()
            if body and self.expect('.'):
                return True
            return False

        if not self.expect('.'):
            return False

        return True


def main(filename: str):
    with open(filename, 'r') as file:
        data = file.read()

    Parser(data)


if __name__ == "__main__":
    main(sys.argv[1])

