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
