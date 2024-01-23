import tkinter as tk
from tkinter import ttk
#from PIL import ImageTK, Image
import csv
import pandas as pd
import os
from instructions import messageBox
from shorthand import split_and_edit, countingWords, teamStats, indivStats
from createFile import save_team_as_csv, save_indiv_as_csv

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Hockey GUI")

        #Style for the Labels
        label_style = ttk.Style()
        label_style.configure("Header.TLabel", font=('Helvetica', 30, 'bold'))

        #Style for the Entry_box
        entry_style = ttk.Style()
        entry_style.configure("Entry.TEntry", font=('Helvetica', 25))

        #Style for the Frame/Text
        message_style = ttk.Style()
        message_style.configure("Message.TMessage", font=('Helvetica', 12))

        #Increase size of main window
        master.geometry("1200x600")

        #Title label
        self.label = ttk.Label(master, text="UNC Hockey", style="Header.TLabel")
        self.label.pack(side="top", pady=20)

        #Save Button
        self.saveButton = ttk.Button(master, text='Save', command=self.on_save_button)
        self.saveButton.pack(side='bottom', pady=5)
        # [] bind to save csv

        #Entry Box Placement
        self.entry = ttk.Entry(master, style="Entry.TEntry", width=120)
        self.entry.pack(side="bottom", pady=60)

        self.entry.bind("<Return>", self.on_enter_pressed)

        #Create a frame that will eventually hold the intructions
        self.instructions = tk.Message(master, width=170, text=messageBox)
        self.instructions.pack(side="left", padx=20)     
        
        self.currentEvents = tk.Message(master,width=900, text='Once you have entered stats the overview will appear here...')
        self.currentEvents.pack(side='left', padx=100)

    def on_enter_pressed(self, event):
        #Get text and store it
        entered_text = self.entry.get()

        #Do something with it
        print("Text entered:", entered_text)
        countOfStuff = countingWords(split_and_edit(entered_text), teamStats)

        faceoffPerc = 0
        if int(teamStats['FaceoffAttempts']) != 0:
            faceoffPerc = int(teamStats['FaceoffWins'])/int(teamStats['FaceoffAttempts']) * 100
        UNCshots = int(teamStats['Shots'])
        OPPshots = int(teamStats['Saves'])
        TOcount = int(teamStats['TOO']) + int(teamStats['TON']) + int(teamStats['TOD'])
        UNChits = int(teamStats['Hits'])
        OPPhits = int(teamStats['HitsOpp'])

        textFinal = f'''
        UNC Faceoff Percentage: {faceoffPerc}
        Faceoff Attempts: {int(teamStats['FaceoffAttempts'])}
        UNC has: {UNCshots} shots
        OPPS has: {OPPshots} shots
        UNC has: {TOcount} turnovers
        UNC has: {UNChits} hits
        OPPS has: {OPPhits} hits
        '''

        self.currentEvents['text'] = textFinal
        #Clear the box
        self.entry.delete(0, tk.END)

    def on_save_button(self):
        save_team_as_csv(teamStats)
        save_indiv_as_csv(indivStats)

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()