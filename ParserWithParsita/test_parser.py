import parser


def test_integrate_empty_file(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'module f\n' \
                                        '\n'


def test_integrate_good_file(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'f.\n'
                                    'f :- g. x :- y.\n'
                                    'f :- g, (h; t).\n'
                                    '\n'
                                    'f a :- g, h (t C d).\n'
                                    'f (cons h t) :- g h, f T.\n'
                                    'f :- a, b, c.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'module f\n' \
                                        '\n' \
                                        'f\n' \
                                        'DEFINITION (f) (g)\n' \
                                        'DEFINITION (x) (y)\n' \
                                        'DEFINITION (f) (AND (g) (OR (h) (t)))\n' \
                                        'DEFINITION (f a) (AND (g) (h (t C d)))\n' \
                                        'DEFINITION (f (cons h t)) (AND (g h) (f T))\n' \
                                        'DEFINITION (f) (AND (a) (AND (b) (c)))\n'


def test_integrate_specific_good_file(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'f (g).\n'
                                    'f ((g)).\n'
                                    'f :- ((g)).\n'
                                    'f :- a (c) (c).\n'
                                    'f (a) (a) (a) (a b) (a) a.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'module f\n' \
                                        '\n' \
                                        'f (g)\n' \
                                        'f ((g))\n' \
                                        'DEFINITION (f) (g)\n' \
                                        'DEFINITION (f) (a (c) (c))\n' \
                                        'f (a) (a) (a) (a b) (a) a\n'


def test_integrate_no_dot1(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'f')
    monkeypatch.chdir(tmp_path)
    assert not parser.main('a.txt')


def test_integrate_no_dot2(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'f :- g')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_no_head(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    ':- f.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_no_body(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'f :- .\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_right_part(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'f :- g; h, .\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_unbalanced_paren(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'f :- (g; (f).\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_empty(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'f ().\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_head_in_brackets1(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    '(a) :- f.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_wrong_head(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'g, h :- g.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_head_in_brackets2(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'a ((b) c).')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_head_in_brackets3(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    'f :- a ((a b) (a b)).')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_syntax_error(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module f.\n'
                                    r'f :- x\ y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_error_in_module1(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module First.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_error_in_module2(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module first')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_variable_error1(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module first.\n'
                                    'First.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_variable_error2(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module first.\n'
                                    'first second (Third).')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')


def test_integrate_variable_error3(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('module first.\n'
                                    'first :- second (third (Fourth)).')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert not parser.main('a.txt')
