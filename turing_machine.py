from sys import argv
class State():
    """
    A singal state in the turing machine.
    :param index: Index of the state.
    :type index: Integer.

    :param cases: Describes instructions for every element of the alphabet.
    :type cases: Dictionary.
    """
    def __init__(self, state_info, alphabet):
        """
        Constructs the state.
        """
        state_info = state_info.split(", ")
        for i in range(1, len(state_info)):
            state_info[i] = state_info[i].split()
        self.index = state_info[0]
        self.cases = dict()
        i = 1
        for symbol in alphabet:
            self.cases[symbol] =\
                 [state_info[i][0], state_info[i][1], state_info[i][2]]
            i += 1


class Tape:
    """
    The tape in the Turing's machine.

    :param head: Indicates current cell. Starts from 0.
    :type head: Integer.

    :param p_cells: Cells on the tape with non-negative indexes.
    :type p_cells: List of strings.

    :param n_cells: Cells on the tape with negative indexes.
    :type n_cells: List of strings.
    """
    def __init__(self, tape):
        """
        Constructs the tape.
        """
        self.head = 0
        self.p_cells = []
        for i in range(len(tape)):
            self.p_cells.append(tape[i])
        self.n_cells = []

    def read(self):
        """
        Returns content of the current cell.
        """
        return self.p_cells[self.head] if self.head >= 0\
            else self.n_cells[abs(self.head+1)]

    def is_the_edge(self, way):
        """
        Checks if the current cell is on the edge of given side of the tape.
        Returns True, if cell is on the edge.
        Returns False, if cell is not on the edge.
        """
        if way:
            if self.head == len(self.p_cells) - 1:
                return True
            return False
        else:
            if abs(self.head) == len(self.n_cells):
                return True
            return False

    def move_left(self):
        """
        Moves the head one cell left.
        If the current cell is on the left edge of the tape,
        creates new cell with character underline in it.
        """
        if self.is_the_edge(0):
            self.n_cells.append('_')
        self.head -= 1

    def move_right(self):
        """
        Moves the head one cell right.
        If the current cell is on the right edge of the tape,
        creates new cell with underline in it.
        """
        if self.is_the_edge(1):
            self.p_cells.append('_')
        self.head += 1

    def write(self, value):
        """
        Writes given value in the current cell.
        """
        if self.head >= 0:
            self.p_cells[self.head] = value
        else:
            self.n_cells[abs(self.head+1)] = value

    def show(self, radius=2):
        """
        Returns two lines.
        First:  Content of the current cell and given number (default - 2)
                of nearest cells from both sides in the ascending order.
        Second: Line, which indicates current cell with symbol "^".
        """
        line = ''
        head = ''
        for cell in range(self.head-radius, self.head+radius+1):
            if cell == self.head:
                head += '^'
            else:
                head += ' '
            if cell >= 0:
                if len(self.p_cells) > cell:
                    line += self.p_cells[cell]
                else:
                    line += '_'
            else:
                if len(self.n_cells) > abs(cell)-1:
                    line += self.n_cells[abs(cell)-1]
                else:
                    line += '_'
        line += '\n'
        display = line + head
        return display

    def show_all(self):
        """
        Returns contnet of every cell on the tape in the ascending order.
        """
        tape = ''
        for i in range(len(self.n_cells)-1, -1, -1):
            tape += self.n_cells[i]
        for i in range(len(self.p_cells)):
            tape += self.p_cells[i]
        return tape


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
