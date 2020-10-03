
import parser


def test_integrate_empty_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == ''


def test_integrate_good_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f :- g. x :- y.\n'
                                    'f :- g, (h; t).\n'
                                    '\n'
                                    'f a :- g, h (t c d).\n'
                                    'f (cons h t) :- g h, f t.\n'
                                    'f :- a, b, c.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'f\n' \
                                        'DEFINITION (f) (g)\n' \
                                        'DEFINITION (x) (y)\n' \
                                        'DEFINITION (f) (AND (g) (OR (h) (t)))\n' \
                                        'DEFINITION (f a) (AND (g) (h (t c d)))\n' \
                                        'DEFINITION (f (cons h t)) (AND (g h) (f t))\n' \
                                        'DEFINITION (f) (AND (a) (AND (b) (c)))\n'


def test_integrate_no_dot(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'There is a problem in "f"'


def test_integrate_no_head(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    ':- f\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'There is a problem in ":- f"'


def test_integrate_no_body(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f :- .\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'There is a problem in "f :- ."'


def test_integrate_right_part(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f :- g; h, .\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'There is a problem in "f :- g; h, ."'


def test_integrate_unbalanced_paren(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f :- (g; (f).\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'There is a problem in "f :- (g; (f)."'


def test_integrate_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n'
                                    'f ().\n'
                                    'x :- y.')
    monkeypatch.chdir(tmp_path)
    parser.main('a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'There is a problem in "f ()."'




