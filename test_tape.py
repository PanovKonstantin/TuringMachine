from tape import Tape


def test_init():
    test_tape = Tape("101011")
    assert test_tape.p_cells == ['1', '0', '1', '0', '1', '1']
    assert test_tape.n_cells == []


def test_init_head():
    test_tape = Tape("101011")
    assert test_tape.head == 0


def test_read():
    test_tape = Tape("101011")
    assert test_tape.read() == '1'
    test_tape.move_left()
    assert test_tape.read() == '_'


def test_is_the_edge():
    test_tape = Tape("101011")
    assert test_tape.is_the_edge(0) is True
    test_tape = Tape("1")
    assert test_tape.is_the_edge(1) is True


def test_move():
    test_tape = Tape("101011")
    test_tape.move_right()
    assert test_tape.head == 1
    assert test_tape.read() == '0'


def test_write():
    test_tape = Tape("101011")
    test_tape.write('0')
    assert test_tape.read() == '0'
    test_tape.move_right()
    test_tape.write('1')
    assert test_tape.read() == '1'


def test_read_after_write_on_negative_cell():
    test_tape = Tape("101011")
    for _ in range(3):
        test_tape.move_left()
        test_tape.write('1')
    test_tape.move_right()
    assert test_tape.read() == '1'


def test_show():
    test_tape = Tape("1010110")
    test_tape.move_right()
    test_tape.move_right()
    assert test_tape.show() == '10101\n  ^  '
    test_tape.move_right()
    assert test_tape.show(3) == '1010110\n   ^   '
    test_tape = Tape("101")
    test_tape.move_left()
    test_tape.write('1')
    test_tape.move_left()
    test_tape.write('0')
    test_tape.move_left()
    test_tape.write('0')
    test_tape.move_right()
    test_tape.move_right()
    test_tape.move_right()
    assert test_tape.show() == '01101\n  ^  '
    assert test_tape.show(4) == '_001101__\n    ^    '


def test_show_all():
    test_tape = Tape("1010110")
    assert test_tape.show_all() == "1010110"
    test_tape.p_cells[3] = '1'
    assert test_tape.show_all() == "1011110"
