
import ply.yacc as yacc
import re
import sys

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
        p[0] = f'{p[2]}'


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
    return None


def to_parse(text: str) -> str:
    parser = yacc.yacc()

    expressions = []
    lines = text.splitlines()
    for line in lines:
        buffer = line.split('.')
        for i in range(len(buffer) - 1):
            expressions.append(buffer[i] + '.')
        expressions.append(buffer[len(buffer) - 1].strip())

    output_data = ''
    for expression in expressions:
        if expression == '':
            continue
        result = parser.parse(expression)
        if result is None:
            return f'There is a problem in "{expression.strip()}"'
        output_data += result + '\n'

    return output_data


def main(filename: str):
    with open(filename, 'r') as file:
        text = file.read()

    output_filename = re.search(r'[^.]+', filename).group(0) + '.out'
    with open(output_filename, 'w') as file:
        file.write(to_parse(text))


if __name__ == '__main__':
    main(sys.argv[1])

