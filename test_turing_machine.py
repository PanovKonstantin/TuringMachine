from turing_machine import TuringMachine, convert_text_for_init
import pytest


def test_convert_text_for_init():
    with open("test.txt", 'r') as f:
        assert convert_text_for_init(f.read()) == ("00100", 
                            ['0', '1', '_'],[['2',['1','R','2'],
                            ['0','R','2'], ['_', 'S', 'stop']],
                            ['1', ['1', 'R', '1'], ['0', 'R', '2'],
                            ['_', 'S', 'stop']]] )

def test_init():
    with open("test.txt", 'r') as f:
        machine = TuringMachine(*convert_text_for_init(f.read()))
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
    with open("test.txt", 'r') as f:
        machine = TuringMachine(*convert_text_for_init(f.read()))
    assert machine.read() == '0'


def test_move():
    with open("test.txt", 'r') as f:
        machine = TuringMachine(*convert_text_for_init(f.read()))
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
    with open("test.txt", 'r') as f:
        machine = TuringMachine(*convert_text_for_init(f.read()))
    machine.write('1')
    assert machine.read() == '1'


def test_current_instruction():
    with open("test.txt", 'r') as f:
        machine = TuringMachine(*convert_text_for_init(f.read()))
    assert machine.current_instruction() == ['1', 'R', '1']


def test_is_stop():
    with open("test_is_stop.txt", 'r') as f:
        machine = TuringMachine(*convert_text_for_init(f.read()))
    machine.step()
    machine.step()
    assert machine.is_stop() is True


def test_show():
    with open("test.txt", 'r') as f:
        machine = TuringMachine(*convert_text_for_init(f.read()))
    assert machine.show() == '__001\n  ^  \nState: 1\n'


def test_show_tape():
    with open("test.txt", 'r') as f:
        machine = TuringMachine(*convert_text_for_init(f.read()))
    machine.move('L')
    for _ in range(7):
        machine.move('R')
    assert machine.show_tape() == "00100"


def test_step():
    with open("test.txt", 'r') as f:
        machine = TuringMachine(*convert_text_for_init(f.read()))
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
    with open("test_start.txt", 'r') as f:
        machine = TuringMachine(*convert_text_for_init(f.read()))
    machine.start()
    assert machine.show_tape() == "110010"


def test_wrong_type_data():
    with pytest.raises(TypeError):
        TuringMachine("0101010", ['00', '0', '1', '_'],
                            [['1', ['1', 'R', '1'],
                            ['0', 'R', '1'],['_', 'S', 'stop']]])
