#!/usr/bin/python3

## Title: Splits Happen
## Author: Bryan Arloff
## Date: 20181130
##
## Description: This is a Python script that displays a Tkinter GUI allowing users to enter a bowling line score and see the resulting final score.
##
## Running Requirements: Python 3 with Tkinter
## Built and tested on macOS 10.14.1 and Python 3.7.1

from tkinter import Tk, StringVar, IntVar, Label, Entry, Button, DISABLED, NORMAL, END, W, E

class SplitsHappen:
    def __init__(self, master):
        self.master = master
        master.title("Splits Happen")

        self.line_score = StringVar()
        self.score = IntVar()
        self.error = StringVar()

        self.entry_header = Label(master, text="Enter a line score", font="Roboto 14")
        self.score_header = Label(master, text="Score", font="Roboto 14 bold")
        self.score_text = Label(master, textvariable=self.score, font="Roboto 14")
        self.error_text = Label(master, textvariable=self.error, foreground="red", font="Roboto 12")

        self.entry = Entry(master) # Not doing any entry validation

        self.enter_button = Button(master, text="Enter", font="Roboto 12", command=self.calculate_score)
        self.reset_button = Button(master, text="Reset", font="Roboto 12", command=self.reset, state=DISABLED)

        # GUI layout
        self.entry_header.grid(row=0, column=0, columnspan=2, sticky=W+E)
        self.score_header.grid(row=0, column=4, ipadx=20)
        self.entry.grid(row=1, column=0, columnspan=2, sticky=W+E)
        self.enter_button.grid(row=1, column=2)
        self.reset_button.grid(row=1, column=3)
        self.score_text.grid(row=1, column=4, ipadx=20)
        self.error_text.grid(row=3, column=0, columnspan=4, sticky=W)
    
    # Method to calculate the total score, from a linescore entered on the GUI's entry box, and update the score section of the GUI
    def calculate_score(self):
        self.line_score.set(self.entry.get()) # Set the line score to what was entered
        self.error.set("") # Clear any error for the new run
        
        line = self.line_score.get()

        if line != "": # Only do something if the line score is not empty
            total_score = 0

            i = 0
            x = 0 # There neeeds to be a second iteration to not skip any rolls whil accounting for skipping frames after a strike
            while i < 20: # There is always only 20 rolls per line, minus any end bonus roll, which is accounted for in the "add_bonus" method
                roll = line[x] # Get the roll result

                if roll == None: # Either nothing was entered, or there is a problem with pulling the value
                    print("Value cannot be retrieved for roll" + str(i))
                elif roll == "X":
                    strike_bonus = line[x+1:x+3] # Get next 2 rolls
                    total_score += 10 + self.add_bonus(strike_bonus)
                    i += 1 # Skip the frame's next roll
                elif roll == "/":
                    previous_roll = line[x-1] # Need to get the previous roll score to know what "/" equals
                    spare_bonus = line[x+1] # Get next roll
                    total_score += 10 - int(previous_roll) + self.add_bonus(spare_bonus)
                elif roll == "-":
                    pass # Do not do anything, it was a miss
                else: # Everthing else should be a number, just add it in
                    try:
                        total_score += int(roll)
                    except ValueError: # A non number character was entered other than the standard bowling ones
                        self.error.set("Syntax error for bowling line score entry")
                        self.reset_button.configure(state=NORMAL)
                
                # DEBUG: Uncomment line below for CLI output to monitor rolls within the normal 2 rolls per frame
                #print("Roll " + str(x+1) + ": " + str(roll) + " -Total: " + str(total_score))
                
                i += 1 # Iterate loop through the 10 frame limit
                x += 1 # Go to the next roll

            self.score.set(str(total_score))

            self.reset_button.configure(state=NORMAL)

    # Method to add the strike and spare carryover bonus. I wonder if this could be recursive in the "calculate_score" method, but the operations are slightly different.
    # Passed in: Up to 2 roll results in the form of a string depending on if it strike (2) or spare (1)
    # Returned: The bonus to add into the strike or spare frame
    def add_bonus(self, bonus):
        bonus_score = 0

        # This will be a loop of 2 or 1 character depending on if it is a strike or spare, respectively
        for c in bonus:
            if c == None: # There is a problem pulling the value
                print("A value cannot be retrieved for a bonus")
            elif c == "X":
                bonus_score += 10
            elif c == "/": # This can never be following a strike or spare, so it can always just grab the first character in "bonus"
                previous = bonus[0]
                bonus_score += 10 - int(previous)
            elif c == "-":
                pass # Do not do anything, it was a miss
            else: # Everything else should be a number, just add it in
                try:
                    bonus_score += int(c)
                except ValueError: # A non number character was entered other than the standard bowling ones
                    self.error.set("Syntax error for bowling line score entry")
                    self.reset_button.configure(state=NORMAL)
            
            # DEBUG: Uncomment line below for CLI output to monitor bonus additions to the frame
            #print("vv Frame bonus: " + c + " (" + str(bonus_score) + ")")
        
        return bonus_score

    # Method to clear the GUI values, resetting them to their defaults
    def reset(self):
        self.entry.delete(0, END)
        self.line_score.set(None)
        self.score.set(0)
        self.error.set("")

        self.enter_button.configure(state=NORMAL)
        self.reset_button.configure(state=DISABLED)

root = Tk()
my_gui = SplitsHappen(root)
root.mainloop()