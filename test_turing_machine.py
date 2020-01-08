from turing_machine import TuringMachine


def test_init():
    machine = TuringMachine("test.txt")
    assert machine.tape.head == 0
    assert machine.tape.p_cells == ['0', '0', '1', '0', '0']
    assert machine.tape.n_cells == []
    assert machine.alphabet == ['0', '1', '_']
    assert machine.states[0].index == '1'
    assert machine.states[0].cases == {'0': ['1', 'R', '1'],
                                       '1': ['0', 'R', '2'],
                                       '_': ['_', 'S', 'stop']
                                       }
    assert machine.states[1].index == '2'
    assert machine.states[1].cases == {'0': ['1', 'R', '2'],
                                       '1': ['0', 'R', '2'],
                                       '_': ['_', 'S', 'stop']
                                       }


def test_read():
    machine = TuringMachine("test.txt")
    assert machine.read() == '0'


def test_move():
    machine = TuringMachine("test.txt")
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
    machine = TuringMachine("test.txt")
    machine.write('1')
    assert machine.read() == '1'


def test_current_instruction():
    machine = TuringMachine("test.txt")
    assert machine.current_instruction() == ['1', 'R', '1']


def test_is_stop():
    machine = TuringMachine("test_is_stop.txt")
    machine.step()
    machine.step()
    assert machine.is_stop() is True


def test_show():
    machine = TuringMachine("test.txt")
    assert machine.show() == '__001\n  ^  \nState: 1\n'


def test_show_all():
    machine = TuringMachine("test.txt")
    machine.move('L')
    for _ in range(7):
        machine.move('R')
    assert machine.show_all() == "00100"


def test_step():
    machine = TuringMachine("test.txt")
    machine.step()
    assert machine.state == '1'
    assert machine.show() == '_1010\n  ^  \nState: 1\n'
    machine.step()
    assert machine.state == '1'
    assert machine.show() == '11100\n  ^  \nState: 1\n'
    machine.step()
    assert machine.state == '2'
    assert machine.show() == '1000_\n  ^  \nState: 2\n'


def test_start():
    machine = TuringMachine("test_start.txt")
    machine.start()
    assert machine.show_all() == "110010"
