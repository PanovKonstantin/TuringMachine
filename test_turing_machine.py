from turing_machine import TuringMachine as TM


def test_convert_text_for_init():
    with open("tests/test.txt", 'r') as f:
        assert TM.convert_text_for_init(f.read()) == ("00100",
                                                      ['0', '1', '_'],
                                                      [['2', ['1', 'R', '2'],
                                                       ['0', 'R', '2'],
                                                       ['_', 'R', 'stop']],
                                                       ['1', ['1', 'R', '1'],
                                                       ['0', 'R', '2'],
                                                       ['_', 'R', 'stop']]])


def test_init():
    with open("tests/test.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
    assert machine.tape.head == 0
    assert machine.tape.p_cells == ['0', '0', '1', '0', '0']
    assert machine.tape.n_cells == []
    assert machine.alphabet == ['0', '1', '_']
    assert machine.states[0].index == '1'
    assert machine.states[0].cases == {'0': ['1', 'R', '1'],
                                       '1': ['0', 'R', '2'],
                                       '_': ['_', 'R', 'stop']
                                       }
    assert machine.states[1].index == '2'
    assert machine.states[1].cases == {'0': ['1', 'R', '2'],
                                       '1': ['0', 'R', '2'],
                                       '_': ['_', 'R', 'stop']
                                       }


def test_read():
    with open("tests/test.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
    assert machine.read() == '0'


def test_move():
    with open("tests/test.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
    assert machine.read() == '0'
    machine.move('R')
    assert machine.read() == '0'
    assert machine.tape.head == 1
    machine.move('R')
    assert machine.read() == '1'
    assert machine.tape.head == 2
    machine.move('L')
    assert machine.read() == '0'
    assert machine.tape.head == 1
    machine.move('S')
    assert machine.read() == '0'
    assert machine.tape.head == 1


def test_write():
    with open("tests/test.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
    machine.write('1')
    assert machine.read() == '1'


def test_current_instruction():
    with open("tests/test.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
    assert machine.current_instruction() == ['1', 'R', '1']


def test_is_stop():
    with open("tests/test_is_stop.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
    machine.step()
    machine.step()
    assert machine.is_stop() is True


def test_show():
    with open("tests/test.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
    assert machine.show() == '__001\n  ^  \nState: 1'


def test_show_tape():
    with open("tests/test.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
    machine.move('L')
    for _ in range(7):
        machine.move('R')
    assert machine.show_tape() == "00100"


def test_step():
    with open("tests/test.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
    machine.step()
    assert machine.state == '1'
    assert machine.show() == '_1010\n  ^  \nState: 1'
    machine.step()
    assert machine.state == '1'
    assert machine.show() == '11100\n  ^  \nState: 1'
    machine.step()
    assert machine.state == '2'
    assert machine.show() == '1000_\n  ^  \nState: 2'


def test_start():
    with open("tests/test_start.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
    machine.start()
    assert machine.show_tape() == "110010"


def test_repr():
    with open("tests/test.txt", 'r') as f:
        machine = TM(*TM.convert_text_for_init(f.read()))
        assert machine.__repr__() == (['0', '0', '1', '0', '0'],
                                      1, 0)
