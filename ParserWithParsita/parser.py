
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
    elif len(data) == 2:
        data = delete_lists(data)
        return [f'{data[0]} {data[1]}']


def tree_definition(data):
    if len(data) == 2:
        data = delete_lists(data)
        return [data[0]]
    elif len(data) == 4:
        data = delete_lists(data)
        return [f'DEFINITION ({data[0]}) ({data[2]})']


def tree_definitions(data):
    data = delete_lists(data)
    result = ""
    for line in data:
        result += line + '\n'
    return [result]


def tree_module(data):
    if len(data) == 0:
        return None
    elif len(data) == 1:
        return [f'{data[0][0]} {data[0][1][0]}']


def tree_program(data):
    if data[0] is None:
        return [f'{data[1][0]}']
    else:
        return [f'{data[0][0]}\n\n{data[1][0]}']


class PrologParsers(TextParsers, whitespace='[ \t\n]*'):

    name = reg('[a-zA-Z_][a-zA-Z_0-9]*') > (lambda x: [x])
    identifier = pred(name, lambda x: x != ['module'], 'identifier')
    variable = pred(identifier, lambda x: 'A' <= x[0][0] <= 'Z', 'variable')
    not_variable = pred(identifier, lambda x: x[0][0] < 'A' or 'Z' < x[0][0], 'not variable')

    atom = fwd()
    brackets_atom = fwd()
    other_atom = fwd()
    expression = fwd()
    conjunction = fwd()
    disjunction = fwd()

    atom.define(not_variable & other_atom |
                not_variable > tree_atom)

    brackets_atom.define('(' & brackets_atom & ')' |
                         atom > tree_brackets_atom)

    other_atom.define(variable & other_atom |
                      variable |
                      brackets_atom & other_atom |
                      brackets_atom > tree_other_atom)

    expression.define(atom |
                      '(' & disjunction & ')' > tree_expression)

    conjunction.define(expression & ',' & conjunction |
                       expression > tree_conjunction)

    disjunction.define(conjunction & ';' & disjunction |
                       conjunction > tree_disjunction)

    definition = (atom & '.' | atom & ':-' & disjunction & '.') > tree_definition

    module = opt('module' & not_variable & '.') > tree_module

    definitions = rep(definition) > tree_definitions

    program = (module & definitions) > tree_program


def to_parse(text: str, flag: str) -> (bool, str):
    result = None
    if flag == '--prog':
        result = PrologParsers.program.parse(text)
    elif flag == '--module':
        result = PrologParsers.module.parse(text)
    elif flag == '--relation':
        result = PrologParsers.definition.parse(text)
    elif flag == '--atom':
        result = PrologParsers.atom.parse(text)
    if isinstance(result, Failure):
        return False, result.message
    assert result is not None
    return True, result.value[0]


def main(filename: str, flag='--prog') -> bool:
    with open(filename, 'r') as file:
        text = file.read()

    output_filename = re.search(r'[^.]+', filename).group(0) + '.out'
    with open(output_filename, 'w') as file:
        verdict, message = to_parse(text, flag)
        file.write(message)
        return verdict


if __name__ == '__main__':

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main(sys.argv[1], sys.argv[2])
