import tkinter as tk
from tkinter import ttk
import pandas as pd
import csv
import os 
import datetime

# Import functions from other files
from instructions import messageBox
from shorthand import split_and_edit, countingWords, load_indiv_stats, create_team_stats
from createFile import save_team_as_csv, save_indiv_as_csv, combine_csvs

class DarkTheme:
    def __init__(self, root):
        # Define dark theme colors
        self.bg_color = "#7BAFD4"
        self.fg_color = "#FFFFFF"
        self.highlight_color = "#13294B"
        self.accent_color = "#13294B"

        # Apply styles
        style = ttk.Style(root)
        style.theme_use('clam')

        style.configure("TNotebook", background=self.bg_color)
        style.configure("TNotebook.Tab", font=('Helvetica', 12), background=self.highlight_color, foreground=self.fg_color)
        style.map("TNotebook.Tab", background=[('selected', self.bg_color)], foreground=[('selected', self.accent_color)])

        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("Header.TLabel", font=('Helvetica', 30, 'bold'), background=self.bg_color, foreground=self.accent_color)
        style.configure("Entry.TEntry", font=('Helvetica', 25), fieldbackground=self.highlight_color, foreground=self.fg_color)
        style.configure("TButton", font=('Helvetica', 12), background=self.highlight_color, foreground=self.fg_color)
        style.map("TButton", background=[('active', self.accent_color)], foreground=[('active', self.fg_color)])
        style.configure("TMessage", font=('Helvetica', 12), background=self.bg_color, foreground=self.fg_color)

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Hockey GUI")

        # Set window dimensions and center it
        window_width = 1200
        window_height = 800
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        master.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Apply dark theme
        self.theme = DarkTheme(master)

        # Create the tab control
        self.tab_control = ttk.Notebook(master)
        self.tab_control.pack(fill='both', expand=1)

        # Create and add tabs
        self.tabs = {
            "Period 1": ttk.Frame(self.tab_control),
            "Period 2": ttk.Frame(self.tab_control),
            "Period 3": ttk.Frame(self.tab_control),
            "Overtime": ttk.Frame(self.tab_control),
            "Final": ttk.Frame(self.tab_control),
            "Roster": ttk.Frame(self.tab_control),
            "Instructions": ttk.Frame(self.tab_control),
            "Extra": ttk.Frame(self.tab_control),
        }
        for tab_name, tab_frame in self.tabs.items():
            self.tab_control.add(tab_frame, text=tab_name)

        # Initialize DataFrames for each tab
        self.team_data = {name: create_team_stats() for name in ["Period 1", "Period 2", "Period 3", "Overtime", "Final"]}
        self.indiv_data = load_indiv_stats()

        # Populate tabs
        self.populate_period_tabs()
        self.populate_roster_tab()
        self.populate_instructions_tab()
        self.populate_extra_tab()
        self.populate_final_tab()

    def populate_period_tabs(self):
        for tab_name in ["Period 1", "Period 2", "Period 3", "Overtime"]:
            self.populate_tab(self.tabs[tab_name], tab_name)

    def populate_tab(self, tab, tab_name):
        # Title label
        label = ttk.Label(tab, text="UNC Hockey", style="Header.TLabel")
        label.pack(side="top", pady=20)

        # Save Button
        save_button = ttk.Button(tab, text='Save', command=lambda: self.on_save_button(tab_name))
        save_button.pack(side='bottom', pady=5)

        # Entry Box
        entry = ttk.Entry(tab, style="Entry.TEntry", width=120)
        entry.pack(side="bottom", pady=60)
        entry.bind("<Return>", lambda event, e=entry, tn=tab_name: self.on_enter_pressed(event, e, tn))

        # Current events message
        current_events = tk.Message(tab, width=900, text='Once you have entered stats the overview will appear here...', background=self.theme.bg_color, foreground=self.theme.fg_color)
        current_events.pack(side='left', padx=100)

        # Store widgets for later use
        tab.widgets = {
            'entry': entry,
            'current_events': current_events,
            'save_button': save_button,
        }

    def populate_roster_tab(self):
        # Read the CSV file
        df = pd.read_csv('24-25 Roster Empty.csv')

        # Create a treeview to display the roster
        roster_tree = ttk.Treeview(self.tabs['Roster'])
        roster_tree['columns'] = ('Player', 'Number')
        roster_tree.heading('#0', text='', anchor='w')
        roster_tree.heading('Player', text='Player', anchor='w')
        roster_tree.heading('Number', text='Number', anchor='w')
        roster_tree.pack(fill='both', expand=1)

        # Add the data to the treeview
        for i, row in df.iterrows():
            roster_tree.insert('', 'end', text='', values=(row['Player'], row['Number']))

    def populate_instructions_tab(self):
        # Display the instructions
        instructions_text = tk.Message(self.tabs['Instructions'], width=900, text=messageBox, background=self.theme.bg_color, foreground=self.theme.fg_color)
        instructions_text.pack(side='top', padx=20, pady=20)

    def populate_extra_tab(self):
        # Display a filler message
        extra_text = tk.Message(self.tabs['Extra'], width=900, text="This is the extra tab.", background=self.theme.bg_color, foreground=self.theme.fg_color)
        extra_text.pack(side='top', padx=20, pady=20)

    def populate_final_tab(self):
        # Centered "Save All Data" button on the "Final" tab
        save_button = ttk.Button(self.tabs['Final'], text="Save All Data", command=self.on_save_button_final)
        save_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def on_enter_pressed(self, event, entry, tab_name):
        entered_text = entry.get()
        current_events = self.tabs[tab_name].widgets['current_events']
        team_data = self.team_data[tab_name]

        try:
            # Process data for the specific tab
            updated_team_data = countingWords(split_and_edit(entered_text), team_data, self.indiv_data)
            faceoffPerc = 0
            if int(team_data['FaceoffAttempts']) != 0:
                faceoffPerc = int(team_data['FaceoffWins']) / int(team_data['FaceoffAttempts']) * 100
            UNCshots = int(team_data['Shots'])
            OPPshots = int(team_data['ShotsFaced'])
            TOcount = int(team_data['TOO']) + int(team_data['TON']) + int(team_data['TOD'])
            UNChits = int(team_data['Hits'])
            OPPhits = int(team_data['HitsOpp'])
            textFinal = f'''
            UNC Faceoff Percentage: {faceoffPerc:.2f}%
            Faceoff Attempts: {int(team_data['FaceoffAttempts'])}
            UNC has: {UNCshots} shots
            OPPS has: {OPPshots} shots
            UNC has: {TOcount} turnovers
            UNC has: {UNChits} hits
            OPPS has: {OPPhits} hits
            '''
            current_events['text'] = textFinal
            # Clear the box
            entry.delete(0, tk.END)
        except Exception as e:
            current_events['text'] = f"There was an error: {e}"

    def on_save_button(self, tab_name):
        # Save data for the specific tab
        if tab_name in ["Period 1", "Period 2", "Period 3", "Overtime"]:
            save_team_as_csv(self.team_data[tab_name], tab_name)
            save_indiv_as_csv(self.indiv_data, tab_name)

    def on_save_button_final(self):
        # Combine CSVs from Period 1, 2, 3, and Overtime
        combine_csvs(["Period 1", "Period 2", "Period 3", "Overtime"], 
                     f'{datetime.datetime.now().strftime("%Y-%m-%d")}_combined_stats')

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()