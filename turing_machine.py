from sys import argv


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

    class TuringMachineError(Exception):
        pass

    @staticmethod
    def convert_text_for_init(text):
        """
        Convert the text from the file, given in a particular form
        Returns three values: Tape, Alphabet and list of every given state
        Returns tape as a list if string
        Ret
        """
        lines = text.split('\n')
        tape = lines[0]
        alphabet = lines[1]
        alphabet = alphabet.split(', ')
        TuringMachine.is_alphabet_correct(alphabet)
        states = lines[2:]
        converted_states = []
        for state in states:
            state = state.split(", ")
            for i in range(1, len(state)):
                state[i] = state[i].split()
            converted_states.append(state)
        if TuringMachine.is_tape_correct(tape, alphabet):
            raise TuringMachine.TuringMachineError("There are symbols in the tape, that don't appear in the alphabet")
        if not TuringMachine.is_alphabet_correct(alphabet):
            raise TuringMachine.TuringMachineError(f"Alphabet is incorrect")
        if TuringMachine.does_alphabet_repeats(alphabet):
            raise TuringMachine.TuringMachineError(f"Symbols in alphabet shoudln't apear twice")
        if not TuringMachine.can_machine_stop(converted_states):
            raise TuringMachine.TuringMachineError("Turing machine must have at least one final state")
        return tape, alphabet, converted_states

    @staticmethod
    def is_alphabet_correct(alphabet):
        """
        If alphabet contains underline and every element is a single
        symbol returns True
        """
        does_contain_underline = False
        for symbol in alphabet:
            if symbol == '_':
                does_contain_underline = True
            if len(symbol) != 1:
                return False
        return does_contain_underline

    @staticmethod
    def is_tape_correct(tape, alphabet):
        for cell in tape:
            cell_value_is_in_alphabet = False
            for symbol in alphabet:
                if cell == symbol:
                    cell_value_is_in_alphabet = True
                    break
                if not cell_value_is_in_alphabet:
                    return False
        return True

    @staticmethod
    def can_machine_stop(states):
        for state in states:
            for intsraction in state[1:]:
                for next_state in intsraction:
                    if next_state == "stop":
                        return True
        return False

    @staticmethod
    def does_alphabet_repeats(alphabet):
        for i in range(len(alphabet)-1):
            for j in range(1, len(alphabet)):
                if alphabet[i] == alphabet[j]:
                    return False
        return True

    def __init__(self, tape, alphabet, states):
        """
        Constructs the turing machine.
        """
        self.tape = Tape(tape)
        self.alphabet = alphabet
        self.states = []
        for state in states:
            self.states.append(State(state, self.alphabet))
        self.states = sorted(self.states, key=lambda state: state.index)
        self.state = 1
        self.step_counter = 0

    def __repr__(self):
        """
        Returns the tape, current state, and current step
        """
        return self.tape.__repr__(), self.state, self.step_counter

    def __str__(self):
        """
        Returns fragment of tape, which contains the current cell and 5 cells around
        them fom both sides, current state and current step.
        """
        info = self.show(5)
        info += f"\nStep: {self.step_counter}"
        return info

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

    def show(self, radius=2):
        """
        Returns two lines.
        First:  Content of the current cell and given number (default - 2)
                of nearest cells from both sides in the ascending order.
        Second: Line, which indicates current cell with symbol "^".
        """
        tape = self.tape.show(radius=radius)
        head = '^'
        for _ in range(radius):
            head += ' '
            head = ' ' + head
        tape += '\n'
        tape += head
        tape += f"\nState: {self.state}"
        return tape

    def show_tape(self):
        """
        Returns contnet of every cell on the tape in the ascending order.
        """
        return self.tape.show_tape().strip('_')

    def step(self):
        """
        Execute all current instructions.
        """
        write, move, self.state = self.current_instruction()
        self.write(write)
        self.move(move)
        self.step_counter += 1

    def start(self):
        """
        Stars the machine.
        Calls "step" methods until the next states is "stop"
        """
        while not self.is_stop():
            self.step()
            print(self.show())  # Printing cells near the head of the machine
        self.result()

    def result(self):
        with open("result.txt", 'w') as f:
            f.write(self.show_tape())

    def restart(self):
        """
        Resets the machine's parameters to the initial state.
        """
        self.state = 1
        self.step_counter = 0
        self.tape.restart()


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

        class StateError(Exception):
            pass

        if len(state_info) - 1 != len(alphabet):
            raise StateError("Machine is incomplete or nondeterministic")
        for intsraction, symbol in zip(state_info[1:], alphabet):
            if len(intsraction) != 3:
                raise StateError("Every instraction has exactly 3 values")
            if intsraction[1] != 'R' and intsraction != 'L':
                raise StateError(f"Machine can move only (R)igth or (L)eft: {intsraction[1]}")
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
        self.default_tape = tape
        self.p_cells = []
        for i in range(len(tape)):
            self.p_cells.append(tape[i])
        self.n_cells = []

    def __repr__(self):
        """
        Returs every cell on the tape
        """
        cells = self.n_cells + self.p_cells
        return cells

    def __str__(self):
        """
        Returs every cell on the tape
        """
        return self.show_tape()

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
        for cell in range(self.head-radius, self.head+radius+1):
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
        return line

    def show_tape(self):
        """
        Returns contnet of every cell on the tape in the ascending order.
        """
        tape = ''
        for i in range(len(self.n_cells)-1, -1, -1):
            tape += self.n_cells[i]
        for i in range(len(self.p_cells)):
            tape += self.p_cells[i]
        return tape

    def restart(self):
        """
        Resets every cell on the tape to the initial values
        and the head to the start cell (0).
        """
        self.p_cells = []
        for i in range(len(self.default_tape)):
            self.p_cells.append(self.default_tape[i])
        self.n_cells = []
        self.head = 0


if __name__ == "__main__":
    if argv[1] is None:  # if an argument wasnt given starts User interface
        import gui
        gui1 = gui.GUI()
        gui1.root.mainloop()
    else:                # if an argument was given opens the file from the path that was
        with open(argv[1], "r") as f:  # given in the argument
            machine = TuringMachine(*TuringMachine.convert_text_for_init(f.read()))
            machine.start()
