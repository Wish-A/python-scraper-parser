import os
import csv
import pandas as pd
import datetime as date
import calendar
import numpy as np
from collections import Counter

csvFile = 'database_not_final.csv' # Name of the file in question
dataFrame = pd.read_csv(csvFile) # Import the choosen file
dataFrame['NEW_SCRAPE_DATE'] = dataFrame['scrape_datumtijd'] # Copy from scrape_datumtijd which will be used as new date notation
dataFrame['NEW_SCRAPE_TIME'] = dataFrame['scrape_datumtijd'] # Copy from scrape_datumtijd which will be used as new time notation

now = date.datetime.now()

def getNewDate(currentDateTime):
    currentDateTime = date.datetime.strptime('March 30, 2021, 10:49 AM', '%B %d, %Y, %I:%M %p') # View current date and time
    newDate = currentDateTime.strftime('%d-%m-%Y')
    return (newDate)

dataFrame['NEW_SCRAPE_DATE'] = dataFrame['NEW_SCRAPE_DATE'].apply(getNewDate) # New date format will be saved into the dataframe

def getNewTime(currentDateTime):
    currentDateTime = date.datetime.strptime('March 30, 2021, 10:49 AM', '%B %d, %Y, %I:%M %p') # View current date and time
    newTime = currentDateTime.strftime('%H:%M')
    return (newTime)

dataFrame['NEW_SCRAPE_TIME'] = dataFrame['NEW_SCRAPE_TIME'].apply(getNewTime) # New date format will be saved into the dataframe

dataFrame['NEW_SCRAPE_DATE'] = pd.to_datetime(dataFrame['NEW_SCRAPE_DATE'], format='%d-%m-%Y')
dataFrame['NEW_SCRAPE_TIME'] = dataFrame['NEW_SCRAPE_TIME'].replace(':', '', regex=True)

def nightTime(datum,tijd):
    if 1400 <= int(tijd) <= 1500:
        datum = datum - pd.Timedelta(1, unit='D')
    return datum.strftime('%d-%m-%Y')

dataFrame['NEW_SCRAPE_DATE'] = dataFrame.apply(lambda x: nightTime(x.NEW_SCRAPE_DATE, x.NEW_SCRAPE_TIME), axis=1)

dataFrame['EXACT_LAST_POST_DATES'] = dataFrame['LP_post_datumtijd']

def getExactLastPostDates(EXACT_LAST_POST_DATES, NEW_SCRAPE_DATE):
    if "Yesterday" in EXACT_LAST_POST_DATES:
        NEW_SCRAPE_DATE = date.datetime.strptime(NEW_SCRAPE_DATE, "%d-%m-%Y")
        yesterday = NEW_SCRAPE_DATE - pd.Timedelta(days = 1)
        yesterday = yesterday.strftime('%d-%m-%Y')
        return yesterday
    elif "ago" in EXACT_LAST_POST_DATES:
        return NEW_SCRAPE_DATE
    elif "at" in EXACT_LAST_POST_DATES:
        strippedDate = EXACT_LAST_POST_DATES.split("at")[0]
        strippedDate = strippedDate.strip()
        strippedDate = pd.to_datetime(strippedDate, format="%B %d, %Y")
        strippedDate = strippedDate.strftime('%d-%m-%Y')
        return strippedDate
    else:
        return EXACT_LAST_POST_DATES

dataFrame['EXACT_LAST_POST_DATES'] = dataFrame.apply(lambda x: getExactLastPostDates(x.EXACT_LAST_POST_DATES, x.NEW_SCRAPE_DATE), axis=1)

dataFrame['EXACT_OP_POST_DATES'] = dataFrame['OP_post_datumtijd']

def getOpDate(EXACT_OP_POST_DATES, NEW_SCRAPE_DATE):
    if "Yesterday" in EXACT_OP_POST_DATES:
        NEW_SCRAPE_DATE = date.datetime.strptime(NEW_SCRAPE_DATE, "%d-%m-%Y")
        yesterday = NEW_SCRAPE_DATE - pd.Timedelta(days = 1)
        yesterday = yesterday.strftime('%d-%m-%Y')
        return yesterday
    elif "ago" in EXACT_OP_POST_DATES:
        return NEW_SCRAPE_DATE
    elif "at" in EXACT_OP_POST_DATES:
        strippedDate = EXACT_OP_POST_DATES.split("at")[0]
        strippedDate = strippedDate.strip()
        strippedDate = pd.to_datetime(strippedDate, format="%B %d, %Y")
        strippedDate = strippedDate.strftime('%d-%m-%Y')
        return strippedDate
    else:
        return EXACT_OP_POST_DATES

dataFrame['EXACT_OP_POST_DATES'] = dataFrame.apply(lambda x: getOpDate(x.EXACT_OP_POST_DATES, x.NEW_SCRAPE_DATE), axis=1)

firstDate = pd.to_datetime("04-02-2021", format = "%d-%m-%Y")
dataFrame['EXACT_LAST_POST_DATES'] = pd.to_datetime(dataFrame['EXACT_LAST_POST_DATES'], format = "%d-%m-%Y")
newDataFrame = dataFrame.loc[(dataFrame['EXACT_LAST_POST_DATES'] >= firstDate)]

df = pd.DataFrame(np.random.randint(0,1000,size=(38, 1)), columns=list('I'))
print(df)

pd.set_option('display.max_columns', None)
print(newDataFrame)

print("\nTop 7 lijst van meest geposte dagen:")
dataFrame['weekday'] = pd.to_datetime(dataFrame['EXACT_OP_POST_DATES'])
dataFrame['newWeekDay'] = dataFrame['weekday'].dt.day_name()
mostPostedDay = dataFrame['newWeekDay'].tolist()
count = Counter(mostPostedDay)
topSeven = count.most_common(7)
print(topSeven)

print("\nTop 10 lijst OP's (Naam en hoevaak gepost):")
OPnicklijst = dataFrame['OP_nick'].tolist()
count = Counter(OPnicklijst)
topTienOP = count.most_common(10)
print(topTienOP)

print("\nTop 10 lijst LP's (Naam en hoevaak gepost):")
LPnicklijst = dataFrame['LP_nick'].tolist()
count = Counter(LPnicklijst)
topTienOP = count.most_common(10)
print(topTienOP)
