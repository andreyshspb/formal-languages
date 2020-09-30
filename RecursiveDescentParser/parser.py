
from lexer import to_lex

import sys


class Node:

    def __init__(self, left, right, name):
        self.left = left
        self.right = right
        self.name = name

    def __str__(self):
        result = '('
        if self.left is not None:
            result += str(self.left)
        result += " " + self.name + ' '
        if self.right is not None:
            result += str(self.right)
        result += ')'
        return result


class Parser:

    def __init__(self, string: str):
        self.lexer = to_lex(string)
        self.current_token = next(self.lexer)

        while self.current_token is not None:
            tree = self.Definition()
            if tree is None:
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

    def Literal(self) -> (Node, None):
        if self.current_token is None:
            print("Expected literal in the end")
            return None

        if self.accept('('):
            block = self.Disjunction()
            if block is not None and self.expect(')'):
                return block
            return None

        if str(self.current_token.type) != 'ID':
            print(f'Expected literal at line: {self.current_token.lineno}, '
                  f'pos: {self.current_token.lexpos}')
            return None

        name = self.current_token.value
        self.current_token = next(self.lexer)
        return Node(None, None, name)

    def Disjunction(self) -> (Node, None):
        left = self.Conjunction()
        if left is None:
            return None

        if self.accept(';'):
            right = self.Disjunction()
            if right is None:
                return None
            return Node(left, right, 'or')

        return left

    def Conjunction(self) -> (Node, None):
        left = self.Literal()
        if left is None:
            return None

        if self.accept(','):
            right = self.Conjunction()
            if right is None:
                return None
            return Node(left, right, 'and')

        return left

    def Definition(self) -> (Node, None):
        head = self.Literal()
        if head is None:
            return None

        if self.accept(':-'):
            body = self.Disjunction()
            if body is not None and self.expect('.'):
                return Node(head, body, "define")
            return None

        if not self.expect('.'):
            return None

        return head


def main(filename: str):
    with open(filename, 'r') as file:
        data = file.read()

    Parser(data)


if __name__ == "__main__":
    main(sys.argv[1])

