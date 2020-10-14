
from parsita import *
import re
import sys


def delete_lists(data):
    for i in range(len(data)):
        if isinstance(data[i], list):
            data[i] = data[i][0]
    return data


def tree_disjunction(data):
    if len(data) == 1:
        return data
    elif len(data) == 3:
        data = delete_lists(data)
        return [f'OR ({data[0]}) ({data[2]})']


def tree_conjunction(data):
    if len(data) == 1:
        return data
    elif len(data) == 3:
        data = delete_lists(data)
        return [f'AND ({data[0]}) ({data[2]})']


def tree_expression(data):
    if len(data) == 1:
        return data
    elif len(data) == 3:
        data = delete_lists(data)
        return [data[1]]


def tree_atom(data):
    if len(data) == 1:
        return data
    elif len(data) == 2:
        data = delete_lists(data)
        return [f'{data[0]} {data[1]}']


def tree_brackets_atom(data):
    if len(data) == 1:
        return data
    elif len(data) == 3:
        data = delete_lists(data)
        return [f'({data[1]})']


def tree_other_atom(data):
    if len(data) == 1:
        return data
    elif len(data) == 4:
        data = delete_lists(data)
        return [f'({data[1]}) {data[3]}']


def tree_definition(data):
    if len(data) == 2:
        data = delete_lists(data)
        return [data[0]]
    elif len(data) == 4:
        data = delete_lists(data)
        return [f'DEFINITION ({data[0]}) ({data[2]})']


class PrologParsers(TextParsers, whitespace='[ \t\n]*'):

    identifier = reg('[a-zA-Z_][a-zA-Z_0-9]*') > (lambda x: [x])

    atom = fwd()
    brackets_atom = fwd()
    other_atom = fwd()
    expression = fwd()
    conjunction = fwd()
    disjunction = fwd()
    definition = fwd()

    atom.define(identifier & other_atom |
                identifier > tree_atom)

    brackets_atom.define('(' & brackets_atom & ')' |
                         atom > tree_brackets_atom)

    other_atom.define('(' & brackets_atom & ')' & other_atom |
                      brackets_atom > tree_other_atom)

    expression.define(atom |
                      '(' & disjunction & ')' > tree_expression)

    conjunction.define(expression & ',' & conjunction |
                       expression > tree_conjunction)

    disjunction.define(conjunction & ';' & disjunction |
                       conjunction > tree_disjunction)

    definition.define(atom & '.' |
                      atom & ':-' & disjunction & '.' > tree_definition)


def to_parse(text: str) -> (bool, str):

    expressions = text.split('.')
    for i in range(len(expressions) - 1):
        expressions[i] += '.'

    output_data = ''
    for expression in expressions:
        if expression.strip() == '':
            continue

        result = PrologParsers.definition.parse(expression)
        if isinstance(result, Failure):
            return False, result.message

        output_data += result.value[0] + '\n'

    return True, output_data


def main(filename: str) -> bool:
    with open(filename, 'r') as file:
        text = file.read()

    output_filename = re.search(r'[^.]+', filename).group(0) + '.out'
    with open(output_filename, 'w') as file:
        verdict, message = to_parse(text)
        file.write(message)
        return verdict


if __name__ == '__main__':
    main(sys.argv[1])

