import os
import datetime
import csv
from shorthand import countingWords, split_and_edit

def save_team_as_csv(dataframe):
    fileName = str(datetime.datetime.now().ctime()) + 'team_stats'
    dataframe.to_csv(fileName, index=False)

def save_indiv_as_csv(dataframe):
    fileName = str(datetime.datetime.now().ctime()) + 'indiv_stats'
    dataframe.to_csv(fileName, index=False)