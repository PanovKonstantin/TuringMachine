from turing_machine import State


def test_init():
    alphabet = ['1', '0', '_']
    states = "1, 0 R 1, 1 R 1, _ S stop"
    state = State(states, alphabet)
    assert state.index == '1'
    assert state.cases == {'1': ['0', 'R', '1'],
                           '0': ['1', 'R', '1'],
                           '_': ['_', 'S', 'stop']
                           }
