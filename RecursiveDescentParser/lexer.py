

import ply.lex as lex


reserved = {
    'module': 'MODULE',
    'sig': 'SIG',
    'type': 'TYPE'
}


tokens = [
    'NUM',
    'LITERAL',
    'OPERATOR',
    'SEPARATOR',
    'ID'
] + list(reserved.values())


def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_LITERAL(t):
    r'"[^"]*"'
    return t


def t_OPERATOR(t):
    r'(->)|(:-)|(,)|(;)'
    return t


def t_SEPARATOR(t):
    r'(\.)|(\[)|(\])|(\|)|(\()|(\))'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# TODO: too slow
def token_column(string: str, token) -> int:
    line_start = string.rfind('\n', 0, token.lexpos)
    return token.lexpos - line_start


class Lexer:

    def __init__(self, text: str):
        self.lexer = lex.lex()
        self.lexer.input(text)
        self.text = text

    def __next__(self):
        token = self.lexer.token()
        if token is None:
            return None
        token.lexpos = token_column(self.text, token)
        return token
