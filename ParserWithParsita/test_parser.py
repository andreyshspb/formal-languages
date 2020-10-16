import parser


def test_integrate_empty_file(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert open('a.out', 'r').read() == ''


def test_integrate_good_file(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('f.\n'
                                'f :- g. x :- y.\n'
                                'f :- g, (h; t).\n'
                                '\n'
                                'f a :- g, h (t C d).\n'
                                'f (cons h t) :- g h, f T.\n'
                                'f :- a, b, c.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert open('a.out', 'r').read() == 'f\n' \
                                        'DEFINITION (f) (g)\n' \
                                        'DEFINITION (x) (y)\n' \
                                        'DEFINITION (f) (AND (g) (OR (h) (t)))\n' \
                                        'DEFINITION (f a) (AND (g) (h (t C d)))\n' \
                                        'DEFINITION (f (cons h t)) (AND (g h) (f T))\n' \
                                        'DEFINITION (f) (AND (a) (AND (b) (c)))\n'


def test_integrate_specific_good_file(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                'f (g).\n'
                                'f ((g)).\n'
                                'f :- ((g)).\n'
                                'f :- a (c) (c).\n'
                                'f (a) (a) (a) (a b) (a) a.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert open('a.out', 'r').read() == 'module f\n' \
                                        '\n' \
                                        'f (g)\n' \
                                        'f ((g))\n' \
                                        'DEFINITION (f) (g)\n' \
                                        'DEFINITION (f) (a (c) (c))\n' \
                                        'f (a) (a) (a) (a b) (a) a\n'


def test_integrate_no_dot1(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                'f')
    monkeypatch.chdir(tmp_path)
    assert not parser.main('a')


def test_integrate_no_dot2(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                'f :- g')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_no_head(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                ':- f.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_no_body(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                'f :- .\n'
                                'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_right_part(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                'f :- g; h, .\n'
                                'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_unbalanced_paren(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                'f :- (g; (f).\n'
                                'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_empty(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                'f ().\n'
                                'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_head_in_brackets1(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                '(a) :- f.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_wrong_head(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                'g, h :- g.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_head_in_brackets2(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                'a ((b) c).')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_head_in_brackets3(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                'f :- a ((a b) (a b)).')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_syntax_error(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module f.\n'
                                r'f :- x\ y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_error_in_module1(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module First.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_error_in_module2(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module first')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_variable_error1(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module first.\n'
                                'First.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_variable_error2(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module first.\n'
                                'first second (Third).')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_variable_error3(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module first.\n'
                                'first :- second (third (Fourth)).')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_module_in_center(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('first :- second.\n'
                                'module prolog.\n'
                                'second :- first.')
    monkeypatch.chdir(tmp_path)
    parser.main('a')
    assert not parser.main('a')


def test_integrate_module(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('module prolog.')
    monkeypatch.chdir(tmp_path)
    parser.main('a', '--module')
    assert open('a.out', 'r').read() == 'module prolog'


def test_integrate_relation(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('first :- second Third.')
    monkeypatch.chdir(tmp_path)
    parser.main('a', '--relation')
    assert open('a.out', 'r').read() == 'DEFINITION (first) (second Third)'


def test_integrate_atom(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('second Third (lol KeK)')
    monkeypatch.chdir(tmp_path)
    parser.main('a', '--atom')
    assert open('a.out', 'r').read() == 'second Third (lol KeK)'


def test_integrate_bad_atom(tmp_path, monkeypatch):
    (tmp_path / 'a').write_text('second Third (Lol KeK)')
    monkeypatch.chdir(tmp_path)
    parser.main('a', '--atom')
    assert not parser.main('a', '--atom')
