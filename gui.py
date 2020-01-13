import tkinter as tk
import tkinter.font as font
from tkinter import filedialog

from turing_machine import TuringMachine, convert_text_for_init


class GUI():
    def __init__(self):
        self.create_root()
        self.create_first_set()
        self.font_for_label = font.Font(size=30)

    def create_root(self):
        self.root = tk.Tk()
        self.buttons = []

    def create_first_set(self):
        self.font_for_buttons = font.Font(size=15)
        self.openFile = tk.Button(self.root,
                                  text="Load instructions from file",
                                  font=self.font_for_buttons,
                                  command=self.load_input_from_file)
        self.createManualy = tk.Button(self.root,
                                       text="Create machine manualy",
                                       font=self.font_for_buttons,
                                       command=self.createManualy_command)
        self.openFile.grid(padx=5, pady=5)
        self.createManualy.grid(padx=5, pady=5)

    def load_input_from_file(self):
        filename = filedialog.askopenfile(initialdir="/",
                                          title="Select file",
                                          filetypes=(("text files", "*.txt"),
                                                     ("all files", "*.*")))
        self.machine = TuringMachine(*convert_text_for_init(filename.read()))
        self.clear_first_set()
        self.create_second_set()
        self.tape_peek()

    def createManualy_command(self):
        self.clear_first_set()
        self.create_third_set()

    def create_third_set(self):
        self.create_tape_interface()
        self.create_alphabet_interface()
        self.startStateEntryButton = tk.Button(self.root,
                                               text="Start states input.",
                                               command=self.state_input)
        self.startStateEntryButton.grid(row=5, sticky="E")

    def state_input(self):
        self.alphabetConfirm_command()
        self.tapeConfirm_command()
        self.clear_third_set()
        self.create_forth_set()

    def create_forth_set(self):
        self.state_count = 0
        self.forth_set = []
        hintState = tk.Label(text="Determine every instraction for every state")
        hintState.grid(row=0)
        self.forth_set.append(hintState)
        for i in range(len(self.alphabet_data)):
            alphabet_symbol = tk.Label(text=self.alphabet_data[i],
                                       font=0)
            alphabet_symbol.grid(row=1, column=i+1)
            self.forth_set.append(alphabet_symbol)
        addState = tk.Button(text="Add new State",
                                  command=self.create_state_line)
        deleteLine = tk.Button(text="Delete state",
                               command=self.delete_state)
        deleteLine.grid(row=0, column=2)
        addState.grid(row=0, column=1)
        createMachine = tk.Button(text="Create machine.",
                                  command=self.createMachine_command)
        createMachine.grid(row=0, column=3)
        back = tk.Button(text="Back",
                         command=self.back_command)
        back.grid(row=0, column=4)
        self.forth_set.append(addState)
        self.forth_set.append(back)
        self.forth_set.append(deleteLine)
        self.forth_set.append(createMachine)
        self.create_state_line()

    def back_command(self):
        self.clear_forth_set()
        self.create_third_set()

    def createMachine_command(self):
        print(self.forth_set)
        self.state_data = []
        for i in range(self.state_count):
            instraction = []
            self.state_data.append(str(i+1))
            for j in range(len(self.alphabet_data)):
                instraction.append(self.forth_set[8+i*len(self.alphabet_data)+j].get().split())
            self.state_data.append(instraction)
        self.clear_forth_set()
        self.machine = TuringMachine(self.tape_data, self.alphabet_data, self.state_data)
        self.create_first_set()

    def clear_forth_set(self):
        for widget in self.forth_set:
            widget.destroy()
        self.forth_set = []
    def delete_state(self):
        self.state_count -= 1
        for _ in range(len(self.alphabet_data)+1):
            self.forth_set[-1].destroy()
            del self.forth_set[-1]

    def create_state_line(self):
        self.state_count += 1
        stateNumber = tk.Label(text=f"State {self.state_count}")
        stateNumber.grid(row=self.state_count+1, column=0)
        self.forth_set.append(stateNumber)
        for i in range(len(self.alphabet_data)):
            stateInstraction = tk.Entry()
            stateInstraction.grid(row=self.state_count+1, column=i+1)
            self.forth_set.append(stateInstraction)

    def clear_third_set(self):
        for widget in (self.tapeInput, self.tapeInputLabel,
                       self.tapeResetButton, self.tapeConfirmButton,
                       self.tapeHint, self.alphabetConfirmButton,
                       self.alphabetHint, self.alphabetInput,
                       self.alphabetInputLabel, self.alphabetResetButton,
                       self.startStateEntryButton):
            widget.destroy()

    def create_tape_interface(self):
        self.tapeInput = tk.Entry(self.root)
        self.tapeInputLabel = tk.Label(self.root,
                                       text="Enter your tape here:",
                                       font=0)
        self.tapeHint = tk.Label(self.root,
                                 text="Hint: Line of characters without spaces. One character = One cell on a tape.")
        self.tapeConfirmButton = tk.Button(self.root,
                                           text="Confirm tape",
                                           width=15,
                                           command=self.tapeConfirm_command)
        self.tapeResetButton = tk.Button(self.root,
                                         text="Reset tape",
                                         width=15,
                                         command=self.tapeReset_command)
        self.tapeInput.grid(row=1, column=1, sticky="W")
        self.tapeInputLabel.grid(row=1, column=0, sticky="W")
        self.tapeConfirmButton.grid(row=1, column=2, sticky="W")
        self.tapeResetButton.grid(row=1, column=3, sticky="W")
        self.tapeResetButton.config(state="disabled")
        self.tapeHint.grid(row=2, columnspan=2, sticky="W")

    def create_alphabet_interface(self):
        self.alphabetInput = tk.Entry(self.root)
        self.alphabetInputLabel = tk.Label(self.root,
                                           text="Enter your alphabet here:",
                                           font=0)
        self.alphabetHint = tk.Label(self.root,
                                     text="Hint: Singal Charachters, separated by space")
        self.alphabetConfirmButton = tk.Button(self.root,
                                               text="Confirm alphabet",
                                               width=15,
                                               command=self.
                                               alphabetConfirm_command)
        self.alphabetResetButton = tk.Button(self.root,
                                             text="Reset alphabet",
                                             width=15,
                                             command=self.
                                             alphabetReset_command)
        self.alphabetInputLabel.grid(row=3, sticky="W")
        self.alphabetConfirmButton.grid(row=3, column=2, sticky="W")
        self.alphabetResetButton.config(state="disabled")
        self.alphabetResetButton.grid(row=3, column=3, sticky="W")
        self.alphabetInput.grid(row=3, column=1, sticky="W")
        self.alphabetHint.grid(row=4, columnspan=2, sticky="W")

    def tapeConfirm_command(self):
        self.tape_data = self.tapeInput.get().split()
        self.tapeConfirmButton.config(state="disabled")
        self.tapeResetButton.config(state="normal")

    def tapeReset_command(self):
        self.tape_data = ""
        self.tapeConfirmButton.config(state="normal")

    def alphabetConfirm_command(self):
        self.alphabet_data = self.alphabetInput.get().split()
        self.alphabetConfirmButton.config(state="disabled")
        self.alphabetResetButton.config(state="normal")

    def alphabetReset_command(self):
        self.alphabet_data = ""
        self.alphabetConfirmButton.config(state="normal")

    def create_second_set(self):
        self.step = tk.Button(self.root, text="Make a step",
                              font=self.font_for_buttons,
                              command=self.step_command)
        self.start = tk.Button(self.root, text="Complete the task",
                               font=self.font_for_buttons,
                               command=self.start_command)
        self.startNew = tk.Button(self.root, text="Open new machine",
                                  font=self.font_for_buttons,
                                  command=self.startNew_command)
        self.restart = tk.Button(self.root, text="Restart the machie",
                                 font=self.font_for_buttons,
                                 command=self.restart_command)
        self.start.grid(padx=100, pady=5, row=3)
        self.step.grid(padx=10, pady=5, row=4)
        self.restart.grid(padx=10, pady=5, row=5)
        self.startNew.grid(padx=10, pady=5, row=6)

    def restart_command(self):
        self.machine.restart()
        self.label.destroy()
        self.tape_peek()

    def start_command(self):
        self.machine.start()
        self.label.destroy()
        self.tape_peek()

    def step_command(self):
        self.machine.step()
        self.label.destroy()
        self.tape_peek()

    def startNew_command(self):
        self.clear_second_set()
        self.create_first_set()

    def clear_first_set(self):
        self.openFile.destroy()
        self.createManualy.destroy()

    def clear_second_set(self):
        self.start.destroy()
        self.restart.destroy()
        self.step.destroy()
        self.startNew.destroy()
        self.label.destroy()

    def tape_peek(self):
        tape = str(self.machine)
        self.label = tk.Label(self.root, text=tape,
                              font=self.font_for_label)
        self.label.grid(row=0)
