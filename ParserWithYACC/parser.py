
import ply.yacc as yacc

from lexer import tokens


def p_definition(p):
    '''definition : atom END
                  | atom DEFINITION or END'''
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = f'DEFINITION ({p[1]}) ({p[3]})'


def p_or(p):
    '''or : and
          | and OR or'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'OR ({p[1]}) ({p[3]})'


def p_and(p):
    '''and : expression
           | expression AND and'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'AND ({p[1]}) ({p[3]})'


def p_expression(p):
    '''expression : atom
                  | LPAREN or RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'({p[2]})'


def p_atom(p):
    '''atom : id
            | id atom
            | id LPAREN atom RPAREN
            | id LPAREN atom RPAREN atom'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = f'{p[1]} {p[2]}'
    elif len(p) == 5:
        p[0] = f'{p[1]} ({p[3]})'
    elif len(p) == 6:
        p[0] = f'{p[1]} ({p[3]}) {p[5]}'


def p_id(p):
    'id : IDENTIFIER'
    p[0] = p[1]


def p_error(p):
    print(p, 'Syntax error')


if __name__ == '__main__':

    parser = yacc.yacc()

    while True:
        try:
            s = input("calc> ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)

