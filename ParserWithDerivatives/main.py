class Regexp:

    def match(self, word: str) -> bool:
        state = self
        for symbol in word:
            state = derivative(symbol, state)
        return nullable(state)


class Empty(Regexp):
    pass


class Epsilon(Regexp):
    pass


class Symbol(Regexp):

    def __init__(self, symbol: str):
        self.symbol = symbol


class Sequence(Regexp):

    def __init__(self, left_re: Regexp, right_re: Regexp):
        self.left_re = left_re
        self.right_re = right_re


class Alternative(Regexp):

    def __init__(self, left_re: Regexp, right_re: Regexp):
        self.left_re = left_re
        self.right_re = right_re


class Star(Regexp):

    def __init__(self, re: Regexp):
        self.re = re


def nullable(re: Regexp) -> bool:
    if isinstance(re, Empty):
        return False
    if isinstance(re, Epsilon):
        return True
    if isinstance(re, Symbol):
        return False
    if isinstance(re, Sequence):
        return nullable(re.left_re) and nullable(re.right_re)
    if isinstance(re, Alternative):
        return nullable(re.left_re) or nullable(re.right_re)
    if isinstance(re, Star):
        return True


def make_sequence(left_re: Regexp, right_re: Regexp) -> Regexp:
    if isinstance(left_re, Empty) or isinstance(right_re, Empty):
        return Empty()
    if isinstance(left_re, Epsilon):
        return right_re
    if isinstance(right_re, Epsilon):
        return left_re
    return Sequence(left_re, right_re)


def make_alternative(left_re: Regexp, right_re: Regexp) -> Regexp:
    if isinstance(left_re, Empty):
        return right_re
    if isinstance(right_re, Empty):
        return left_re
    if isinstance(left_re, Epsilon):
        if nullable(right_re):
            return right_re
        return Alternative(Epsilon(), right_re)
    if isinstance(right_re, Epsilon):
        if nullable(left_re):
            return left_re
        return Alternative(Epsilon(), left_re)
    if type(left_re) == type(right_re):
        return left_re
    return Alternative(left_re, right_re)


def make_star(re: Regexp) -> Regexp:
    if isinstance(re, Empty):
        return Epsilon()
    if isinstance(re, Epsilon):
        return Epsilon()
    if isinstance(re, Star):
        return Star(re.re)
    return Star(re)


def derivative(symbol: str, unit: Regexp) -> Regexp:
    if isinstance(unit, Empty):
        return Empty()
    if isinstance(unit, Epsilon):
        return Empty()
    if isinstance(unit, Symbol):
        if symbol == unit.symbol:
            return Epsilon()
        return Empty()
    if isinstance(unit, Sequence):
        if nullable(unit.left_re):
            return make_alternative(make_sequence(derivative(symbol, unit.left_re),
                                                  unit.right_re),
                                    derivative(symbol, unit.right_re))
        else:
            return make_sequence(derivative(symbol, unit.left_re),
                                 unit.right_re)
    if isinstance(unit, Alternative):
        return make_alternative(derivative(symbol, unit.left_re),
                                derivative(symbol, unit.right_re))
    if isinstance(unit, Star):
        return make_sequence(derivative(symbol, unit.re),
                             make_star(unit.re))


def simple_tests():
    first = Empty()
    second = Epsilon()
    third = Symbol('a')

    assert (not first.match(''))
    assert (not first.match('aaa'))
    assert (second.match(''))
    assert (not second.match('aaa'))
    assert (third.match('a'))
    assert (not third.match('aaa'))


def middle_tests():
    first = Sequence(
        Symbol('a'),
        Symbol('b')
    )
    second = Alternative(
        Symbol('a'),
        Symbol('b')
    )
    third = Star(Symbol('a'))

    assert (first.match('ab'))
    assert (not first.match('a'))
    assert (not first.match('aa'))
    assert (not first.match(''))
    assert (second.match('a'))
    assert (second.match('b'))
    assert (not second.match('ab'))
    assert (not second.match(''))
    assert (third.match(''))
    assert (third.match('a'))
    assert (third.match('aaa'))
    assert (not third.match('aab'))


def hard_tests():
    first = Sequence(
        Star(Symbol('a')),
        Alternative(
            Symbol('b'),
            Symbol('c')
        )
    )
    second = Star(Alternative(
        Symbol('a'),
        Symbol('b')
    ))
    third = Star(Star(Symbol('a')))

    assert (first.match('b'))
    assert (first.match('ac'))
    assert (first.match('aaac'))
    assert (not first.match('aabc'))
    assert (second.match(''))
    assert (second.match('a'))
    assert (second.match('b'))
    assert (second.match('aaabbbaaa'))
    assert (not second.match('c'))
    assert (not second.match('aacaa'))
    assert (third.match(''))
    assert (third.match('a'))
    assert (third.match('aaa'))
    assert (not third.match('aba'))
    assert (not third.match('bbb'))


if __name__ == '__main__':
    simple_tests()
    middle_tests()
    hard_tests()
