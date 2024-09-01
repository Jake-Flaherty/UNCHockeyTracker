import csv
import pandas as pd
import os
import tkinter as tk
import re

#[X]put current stats on screen not the df
#[X]change all letters to uppercase always
#[X]save function
#[]period by period
#[]errorhandling
#[]change the stats on screen by period selected


# Initialize DataFrames for each tab
def create_team_stats():
    return pd.DataFrame([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]], columns=['FaceoffAttempts', 'FaceoffWins', 'Hits', 'Shots', 'ShotsFromHouse', 'TOO', 'TON', 'TOD', 'PEN', 'PIM', 'PK', 'PPG', 'ShotsFaced', 'HitsOpp', 'OppPEN'])

# Load individual stats from a file
def load_indiv_stats(file_path='24-25 Roster Empty.csv'):
    return pd.read_csv(file_path)

# Split and edit text
def split_and_edit(text):
    text = text.upper()
    events = text.split()
    return events

# Counting words with a specified DataFrame
def countingWords(word_array, teamdf, indivStats):
    # Iterate through the words
    for word in word_array:
        if word.startswith('FO'):
            teamdf.at[0, 'FaceoffAttempts'] += 1
            indivStats.loc[indivStats['Number'] == int(re.findall(r'\d+', word)[0]), 'FO'] += 1
            if 'W' in word:
                teamdf.at[0, 'FaceoffWins'] += 1
                indivStats.loc[indivStats['Number'] == int(re.findall(r'\d+', word)[0]), 'FOW'] += 1
        if word.startswith('H'):
            if word[1:].isnumeric():
                teamdf.at[0, 'Hits'] += 1
                indivStats.loc[indivStats['Number'] == int(word[1:]), 'Hits'] += 1
            else:
                teamdf.at[0, 'HitsOpp'] += 1
        if word.startswith('S'):
            if word[1] != 'V' and word[1] != 'F':
                teamdf.at[0, 'Shots'] += 1
                if 'HOUSE' in word:
                    teamdf.at[0, 'ShotsFromHouse'] += 1
        if word.startswith('TO'):
            indivStats.loc[indivStats['Number'] == int(re.findall(r'\d+', word)[0]), 'TO'] += 1
            if word.startswith('TOO'):
                teamdf.at[0, 'TOO'] += 1
            if word.startswith('TON'):
                teamdf.at[0, 'TON'] += 1
            if word.startswith('TOD'):
                teamdf.at[0, 'TOD'] += 1
        if word.startswith('PEN'):
            if word[3].isdigit():  # Check if the character after 'PEN' is a digit
                teamdf.at[0, 'PEN'] += 1
                teamdf.at[0, 'PIM'] += int(word[word.find(':') + 1:])
            elif not word[3].isdigit():
                teamdf.at[0, 'OppPEN'] += 1
        if word.startswith('PK'):
            teamdf.at[0, 'PK'] += 1
        if word == 'PPG':
            teamdf.at[0, 'PPG'] += 1
        if word.startswith('SF'):
            teamdf.at[0, 'ShotsFaced'] += 1
            indivStats.loc[indivStats['Number'] == int(re.findall(r'\d+', word)[0]), 'ShotsFaced'] += 1
        if word.startswith('SV'):
            teamdf.at[0, 'ShotsFaced'] += 1
            indivStats.loc[indivStats['Number'] == int(re.findall(r'\d+', word)[0]), 'Saves'] += 1
        if word.startswith('+'):
            indivStats.loc[indivStats['Number'] == int(re.findall(r'\d+', word)[0]), 'Plus/Minus'] += 1
        if word.startswith('-'):
            indivStats.loc[indivStats['Number'] == int(re.findall(r'\d+', word)[0]), 'Plus/Minus'] -= 1

    return teamdf

