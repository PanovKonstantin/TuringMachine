import turing_machine

def test_button_load_input_from_file():
    root = turing_machine.GUI()
    root.button_load_input_from_file()
    assert root.machine.tape.head == 0
    assert root.machine.tape.p_cells == ['0', '0', '1', '0', '0']
    assert root.machine.tape.n_cells == []
    assert root.machine.alphabet == ['0', '1', '_']
    assert root.machine.states[0].index == '1'
    assert root.machine.states[0].cases == {'0': ['1', 'R', '1'],
                                       '1': ['0', 'R', '2'],
                                       '_': ['_', 'S', 'stop']
                                       }
    assert root.machine.states[1].index == '2'
    assert root.machine.states[1].cases == {'0': ['1', 'R', '2'],
                                       '1': ['0', 'R', '2'],
                                       '_': ['_', 'S', 'stop']
                                       }
