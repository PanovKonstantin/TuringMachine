from turing_machine import TuringMachine, convert_text_for_init
import tkinter as tk
import tkinter.font as font
from tkinter import filedialog, Text

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
                font = self.font_for_buttons,
                command=self.load_input_from_file)
        self.createManualy = tk.Button(self.root,
                text="Create machine manualy",
                font = self.font_for_buttons,
                command=self.createManualy_command)
        self.openFile.grid(padx=5, pady=5)
        self.createManualy.grid(padx=5, pady=5)

    def load_input_from_file(self):
        filename = filedialog.askopenfile(initialdir="/",
                                            title="Select file",
                                            filetypes=(("text files",
                                            "*.txt"),("all files","*.*"))) 
        self.machine = TuringMachine(*convert_text_for_init(filename.read()))
        self.clear_first_set()
        self.create_second_set()
        self.tape_peek()

    def createManualy_command(self):
        self.clear_first_set()
        self.create_third_set()

    def create_third_set(self):
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
        self.tapeInput.grid(row=0, column=1, sticky='W')
        self.tapeInputLabel.grid(row=0, column=0, sticky='W')
        self.tapeConfirmButton.grid(row=0, column=2)
        self.tapeResetButton.grid(row=0, column=3)
        self.tapeHint.grid(columnspan=2, sticky='W')
        self.alphabetInput = tk.Entry(self.root)
        self.alphabetInputLabel = tk.Label(self.root,
                                        text="Enter your alphabet here:",
                                        font=0)
        self.alphabetHint = tk.Label(self.root,
                                    text="Hint: Singal Charachters, separated by space")
        self.alphabetConfirmButton = tk.Button(self.root,
                                            text="Confirm alphabet",
                                            width=15,
                                            command=self.alphabetConfirm_command)
        self.alphabetResetButton = tk.Button(self.root,
                                            text="Reset alphabet",
                                            width=15,
                                            command=self.alphabetReset_command)
        self.alphabetInput.grid(row=2,column=1, sticky='W')
        self.alphabetInputLabel.grid(row=2, sticky='W')        
        self.alphabetConfirmButton.grid(row=2, column=2)
        self.alphabetResetButton.grid(row=2, column=3)
        self.alphabetInput.grid(row=0, column=1)
        self.alphabetHint.grid(columnspan=2, sticky='W')

    def tapeConfirm_command(self):
        pass
    def tapeReset_command(self):
        pass
    def alphabetConfirm_command(self):
        pass
    def alphabetReset_command(self):
        pass
    def create_second_set(self):
        self.step = tk.Button(self.root, text="Make a step",
                            font = self.font_for_buttons,
                            command=self.step_command)
        self.start = tk.Button(self.root, text="Complete the task",
                            font = self.font_for_buttons,
                            command=self.start_command)
        self.startNew = tk.Button(self.root, text="Open new machine",
                            font = self.font_for_buttons,
                            command=self.startNew_command)
        self.restart = tk.Button(self.root, text="Restart the machie",
                            font = self.font_for_buttons,
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


