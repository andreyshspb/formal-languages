
import parser


def test_integrate_empty_file(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == ''


def test_integrate_good_file(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f :- g. x :- y.\n'
                                    'f :- g, (h; t).\n'
                                    '\n'
                                    'f a :- g, h (t c d).\n'
                                    'f (cons h t) :- g h, f t.\n'
                                    'f :- a, b, c.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'f\n' \
                                        'DEFINITION (f) (g)\n' \
                                        'DEFINITION (x) (y)\n' \
                                        'DEFINITION (f) (AND (g) (OR (h) (t)))\n' \
                                        'DEFINITION (f a) (AND (g) (h (t c d)))\n' \
                                        'DEFINITION (f (cons h t)) (AND (g h) (f t))\n' \
                                        'DEFINITION (f) (AND (a) (AND (b) (c)))\n'


def test_integrate_specific_good_file(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f (g).\n'
                                    'f ((g)).\n'
                                    'f :- ((g)).\n'
                                    'f :- a (c) (c).\n'
                                    'f (a) (a) (a) (a b) (a) a.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'f (g)\n' \
                                        'f ((g))\n' \
                                        'DEFINITION (f) (g)\n' \
                                        'DEFINITION (f) (a (c) (c))\n' \
                                        'f (a) (a) (a) (a b) (a) a\n'


def test_integrate_no_dot1(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in "f"\n'


def test_integrate_no_dot2(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f :- g')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in "f :- g"\n'


def test_integrate_no_head(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    ':- f.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in ":- f."\n'


def test_integrate_no_body(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f :- .\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in "f :- ."\n'


def test_integrate_right_part(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f :- g; h, .\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in "f :- g; h, ."\n'


def test_integrate_unbalanced_paren(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f :- (g; (f).\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in "f :- (g; (f)."\n'


def test_integrate_empty(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f ().\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in "f ()."\n'


def test_integrate_head_in_brackets1(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    '(a) :- f.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in "(a) :- f."\n'


def test_integrate_wrong_head(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('g, h :- g.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in "g, h :- g."\n'


def test_integrate_head_in_brackets2(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('a ((b) c).')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in "a ((b) c)."\n'


def test_integrate_head_in_brackets3(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('f :- a ((a b) (a b)).')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == 'There is a problem in "f :- a ((a b) (a b))."\n'


def test_integrate_syntax_error(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text(r'f :- x\ y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    assert open('a.out', 'r').read() == r'There is a problem in "f :- x\ y."' + '\n'

