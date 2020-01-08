from sys import argv

from states import State

from tape import Tape


class TuringMachine:
    """
    Turing machine. Reads and chages content of a tape accordingly to states.

    :param tape: The tape in the Turing's machine.
    :type tape: Tape.

    :param alphabet: All the accessable values.
    :type alphabet: List of strings.

    :param states: All the existing states in the ascending order by index.
    :type states: List of States.

    :param state: Current state.
    :type state: Integer.
    """
    def __init__(self, path_to_file):
        """
        Constructs the turing machine.
        """
        with open(path_to_file, 'r') as f:
            lines = f.read().split('\n')
            tape = lines[0]
            alphabet = lines[1]
            states = lines[2:]
        self.tape = Tape(tape)
        self.alphabet = alphabet.split(', ')
        self.alphabet.append('_')
        self.states = []
        for state in states:
            self.states.append(State(state, self.alphabet))
        self.states = sorted(self.states, key=lambda state: state.index)
        self.state = 1

    def write(self, value):
        """
        Writes given value in the current cell of the tape.
        """
        self.tape.write(value)

    def move(self, way):
        """
        Moves current cell in the given direction.
        """
        moves = {'R': self.tape.move_right,
                 'L': self.tape.move_left}
        moves.get(way, lambda: None)()

    def read(self):
        """
        Returns content of the current cell.
        """
        return self.tape.read()

    def is_stop(self):
        """
        Checks if current state instructs to stop the machine.
        """
        return self.current_instruction()[-1] == 'stop'

    def current_instruction(self):
        """
        Returns tuple of current instructions.
        Value to write, direction to move, next state.
        """
        return self.states[int(self.state)-1].cases[self.tape.read()]

    def show(self):
        """
        Returns two lines.
        First:  Content of the current cell and given number (default - 2)
                of nearest cells from both sides in the ascending order.
        Second: Line, which indicates current cell with symbol "^".
        """
        info = self.tape.show()
        info += f"\nState: {self.state}\n"
        return info

    def show_all(self):
        """
        Returns contnet of every cell on the tape in the ascending order.
        """
        return self.tape.show_all().strip('_')

    def step(self):
        """
        Execute all current instructions.
        """
        write, move, self.state = self.current_instruction()
        self.write(write)
        self.move(move)

    def start(self):
        while not self.is_stop():
            print(self.show())
            self.step()
        self.result()

    def result(self):
        with open("result.txt", 'w') as f:
            f.write(self.show_all())


if __name__ == "__main__":
    machine = TuringMachine(argv[1])
    machine.start()
