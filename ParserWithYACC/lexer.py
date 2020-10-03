

import ply.lex as lex


tokens = [
    'IDENTIFIER',
    'DEFINITION',
    'END',
    'AND',
    'OR',
    'LPAREN',
    'RPAREN'
]

t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'

t_DEFINITION = r':-'
t_END = r'\.'
t_AND = r','
t_OR = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t\n'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
