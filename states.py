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
