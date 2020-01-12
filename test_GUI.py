import gui as g

def test_load_input_from_file():
    gui = g.GUI()
    gui.load_input_from_file()
    assert gui.machine.tape.head == 0
    assert gui.machine.tape.p_cells == ['0', '0', '1', '0', '0']
    assert gui.machine.tape.n_cells == []
    assert gui.machine.alphabet == ['0', '1', '_']
    assert gui.machine.states[0].index == '1'
    assert gui.machine.states[0].cases == {'0': ['1', 'R', '1'],
                                       '1': ['0', 'R', '2'],
                                       '_': ['_', 'S', 'stop']
                                       }
    assert gui.machine.states[1].index == '2'
    assert gui.machine.states[1].cases == {'0': ['1', 'R', '2'],
                                       '1': ['0', 'R', '2'],
                                       '_': ['_', 'S', 'stop']
                                       }
