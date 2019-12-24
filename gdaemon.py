
import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials
import sys


import dateutil.parser
from dateutil.parser import parse
import os

from time import sleep

import json
import requests

import re

import urllib3

urllib3.disable_warnings()


print "Loading things, please wait ~10 seconds\n"

#TICKER DATA
krakenXTZXBT = requests.get("https://api.kraken.com/0/public/Ticker?pair=XTZXBT")
krakenXBTUSD = requests.get("https://api.kraken.com/0/public/Ticker?pair=XBTUSD")
krakenXTZUSD = requests.get("https://api.kraken.com/0/public/Ticker?pair=XTZUSD")
pairXTZXBT = json.loads(krakenXTZXBT.text)
pairXBTUSD = json.loads(krakenXBTUSD.text)
pairXTZUSD = json.loads(krakenXTZUSD.text)

def remove_quotes(text):
    return re.sub(r"\"(-?\d+(?:[\.,]\d+)?)\"", r'\1', text)
XBTXBClastPriceWithQuotes= (json.dumps(pairXTZXBT.items()[0][1].items()[0][1].get(u"a"[0])[0]))
XBTXBClastPriceSansQuotes=remove_quotes(XBTXBClastPriceWithQuotes)
XBTXBClastPriceString = float(XBTXBClastPriceSansQuotes)
xtzxbtprice = format(XBTXBClastPriceString)

XTZUSDlastPriceWithQuotes= (json.dumps(pairXTZUSD.items()[0][1].items()[0][1].get(u"a"[0])[0]))
XTZUSDlastPriceSansQuotes=remove_quotes(XTZUSDlastPriceWithQuotes)
XTZUSDlastPriceString = float(XTZUSDlastPriceSansQuotes)
xtzusdprice = format(XTZUSDlastPriceString)

XBTUSDlastPriceWithQuotes= (json.dumps(pairXBTUSD.items()[0][1].items()[0][1].get(u"a"[0])[0]))
XBTUSDlastPriceSansQuotes=remove_quotes(XBTUSDlastPriceWithQuotes)
XBTUSDlastPriceString = float(XBTUSDlastPriceSansQuotes)
xbtusdprice = format(XBTUSDlastPriceString)


def get_row(self, row_number, worksheet_number=0):
    worksheet = self._get_worksheet(worksheet_number)
    return worksheet.row_values(row_number)
def append_row(self, row_values, worksheet_number=0):
    worksheet = self._get_worksheet(worksheet_number)
    return worksheet.append_row(row_values)
def insert_row(self, row_values, row_index, worksheet_number=0):
    worksheet = self._get_worksheet(worksheet_number)
    return worksheet.insert_row(row_values, row_index)

#setup google permissions
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key('Replace_Me')

#setup spreadsheets
CurrentCycleCSV = spreadsheet.worksheet("CurrentCycleCSV")
liveTickers = spreadsheet.worksheet("Live Tickers")
CurrentCycleCSVString = 'CurrentCycleCSV'  # Please set sheet name you want to put the CSV data.

#set up MAIN DATA and CurrentCycleValues sheets for automation
MAINDATAString = 'MAIN DATA'
CurrentCycleValueString = 'CurrentCycleValues'
MAINDATA = spreadsheet.worksheet(MAINDATAString)
CurrentCycleValue = spreadsheet.worksheet(CurrentCycleValueString)

print "Nearly there!\n"

#get the last row index
MAINDATAlastRow = len(MAINDATA.col_values(1))
MAINDATAcurrentRow = MAINDATAlastRow + 1
#get latest complete cycle
cycleResponse = requests.get("https://api.tzstats.com/explorer/cycle/head", timeout=60, verify=False)
cycleJSON = json.loads(cycleResponse.text)
for key, value in cycleJSON.items():
      if key == "cycle":
        latestCycle = value
        latestCompleteCycle = value-1



daemonInputIsValid = False
while daemonInputIsValid==False:
    askDaemon = raw_input("Run as daemon? (y/n)\n")
    if askDaemon == "y":
        isDaemon = True
        daemonInputIsValid = True
    if askDaemon == "n":
        isDaemon = False
        daemonInputIsValid = True
    else:
        if daemonInputIsValid == False:
            print "Error! Try again.\n"

def waitForCycle():

    gc.login()
    for x in range(0,960):
        print format(960-x) + " seconds"
        sleep(1)
        if x >10:
            os.system('clear')
            print "waiting 15 minutes before checking for cycle update"
    os.system('clear')
    print "difference is "+format(difference)
    sleep(1)
    print "checking for cycle"
    gc.login()
    sleep(3)
    print"."
    checkForCycleDifference()


def checkForCycleDifference():
    #check last row cycle
    print "Checking for new cycle...\n"
    MAINDATAlastRow = len(MAINDATA.col_values(1))
    MAINDATAcurrentRow = MAINDATAlastRow + 1
    print "10 seconds until API request"
    sleep(5)
    print "."
    sleep(5)
    print "."
    #get latest complete cycle
    cycleResponse = requests.get("https://api.tzstats.com/explorer/cycle/head", timeout=60, verify=False)
    cycleJSON = json.loads(cycleResponse.text)
    for key, value in cycleJSON.items():
          if key == "cycle":
            latestCycle = value
            latestCompleteCycle = value-1
    lastRowCycle = MAINDATA.acell('A'+format(MAINDATAlastRow)).value
    print "Clearing screen in 10 seconds"
    print "."
    sleep(10)
    print "."
    os.system('clear')

    #get the difference
    difference = int(lastRowCycle)-latestCompleteCycle

askWhichCycle = raw_input("Which cycle? Or enter 'c' for the latest complete cycle\n")
if askWhichCycle == "c":
    for key, value in cycleJSON.items():
          if key == "cycle":

            latestCompleteCycle = value-1
    lastRowCycle = MAINDATA.acell('A'+format(MAINDATAlastRow)).value
    csvFile = format(lastRowCycle)+'.csv'

    #get the difference
    difference = int(lastRowCycle)-latestCompleteCycle
    if difference == 0:
        cycle = latestCompleteCycle
    else:
        lastRowCycle = MAINDATA.acell('A'+format(MAINDATAlastRow)).value
        csvFile = format(int(lastRowCycle)+1)+'.csv'
        cycle = int(lastRowCycle)+1
    print "The MAIN DATA last row cycle is " + format(lastRowCycle)
    if difference == 0:
        print "Last row cycle "+format(lastRowCycle)+" is up to date with recently completed cycle "+format(latestCompleteCycle)+"."
    else:
        cycle = int(lastRowCycle)+1
        print "Filling out for cycle " + format(cycle)
    print "Difference between last row cycle & latest complete cycle is "+format(difference)

else:
    try:
        cycleInput = int(askWhichCycle)
        print "filling out row for cycle "+format(cycleInput)
        csvFile = format(cycleInput)+'.csv'

    except ValueError:
        print "Sorry I didn't understand"
        sys.exit()





def updateSpreadsheets():
    #check last row cycle
    MAINDATAlastRow = len(MAINDATA.col_values(1))
    MAINDATAcurrentRow = MAINDATAlastRow + 1
    lastRowCycle = MAINDATA.acell('A'+format(MAINDATAlastRow)).value

    if difference == 0:
        cycle = latestCompleteCycle
        currentCycleCSVFile = int(cycle)
        csvFile = format(currentCycleCSVFile)+".csv"
    if difference <0:
        previousCycleCSVFile = int(lastRowCycle)+1
        csvFile = format(previousCycleCSVFile)+".csv"
    print "Updating row, please wait\n"
    #update report.csv to CurrentCycleCSV sheet
    try:
        spreadsheet.values_update(
            CurrentCycleCSVString,
            params={'valueInputOption': 'USER_ENTERED'},
            body={'values': list(csv.reader(open(csvFile)))}
            )
    except IOError:
        print "Sorry, I couldn't find "+format(cycleInput) + ".csv - check the directory and try again!"
        sys.exit()

    #delete last two rows from CurrentCycleCSV worksheet
    CurrentCycleCSVlastRow = len(CurrentCycleCSV.col_values(1))
    def delete_row(self, row_number, worksheet_number=0):
        worksheet = self._get_worksheet(worksheet_number)
        return worksheet.delete_row(row_number)
    CurrentCycleCSV.delete_row(CurrentCycleCSVlastRow)
    CurrentCycleCSV.delete_row(CurrentCycleCSVlastRow-1)

    #get variables for blue columns
    stakingBalance = float(CurrentCycleCSV.acell('C2').value)/1000000
    amount = CurrentCycleValue.acell('B2').value
    fee = CurrentCycleValue.acell('B3').value
    totalBakedCycle = float(CurrentCycleCSV.acell('F2').value)/1000000



    #get the cycle date
    cycle = int(lastRowCycle)+1
    if askWhichCycle == "c":
        cycleDateResponse = requests.get("https://api.tzstats.com/explorer/cycle/"+format(cycle), timeout=60, verify=False)
    else:
        cycleDateResponse = requests.get("https://api.tzstats.com/explorer/cycle/"+format(askWhichCycle), timeout=60, verify=False)
    cycleJSON = json.loads(cycleDateResponse.text)

    for key, value in cycleJSON.items():
        if key == "start_time":
            datetime = parse(value)
            cycleDate = datetime.date()
            cycleDate = datetime.strftime("%d %m %Y")


    new_row = (
        format(cycle),
        format(cycleDate),
        format(totalBakedCycle),
        format(fee),
        "=sum("+format(float(amount))+"+G"+format(MAINDATAcurrentRow)+")",
        "=sum(I"+format(MAINDATAcurrentRow)+"-D"+format(MAINDATAcurrentRow)+"-G"+format(MAINDATAcurrentRow)+")",
        "",
        format(stakingBalance),
        "=sum(C"+format(MAINDATAcurrentRow)+"-E"+format(MAINDATAcurrentRow)+")",
        "=sum(I"+format(MAINDATAcurrentRow)+"*O"+format(MAINDATAcurrentRow)+")",
        "=sum(J"+format(MAINDATAcurrentRow)+"*M"+format(MAINDATAcurrentRow)+")",
        "=sum(I"+format(MAINDATAcurrentRow)+"*N"+format(MAINDATAcurrentRow)+")",
        liveTickers.acell("A1").value,
        xtzxbtprice,
        xtzusdprice,
        xbtusdprice,
        "=sum(Q"+format(MAINDATAlastRow)+"+C"+format(MAINDATAcurrentRow)+")",
        "=sum(R"+format(MAINDATAlastRow)+"+D"+format(MAINDATAcurrentRow)+")",
        "=sum(S"+format(MAINDATAlastRow)+"+E"+format(MAINDATAcurrentRow)+")",
        "=sum(T"+format(MAINDATAlastRow)+"+F"+format(MAINDATAcurrentRow)+")",
        "=sum(U"+format(MAINDATAlastRow)+"+I"+format(MAINDATAcurrentRow)+")",
        "=sum(V"+format(MAINDATAlastRow)+"+J"+format(MAINDATAcurrentRow)+")",
        "=sum(W"+format(MAINDATAlastRow)+"+K"+format(MAINDATAcurrentRow)+")",
        "=sum(X"+format(MAINDATAlastRow)+"+L"+format(MAINDATAcurrentRow)+")",
        "=sum(O"+format(MAINDATAcurrentRow)+"*E"+format(MAINDATAcurrentRow)+")",
        )

    if askWhichCycle == "c":
        MAINDATA.update_acell("Z2",int(latestCompleteCycle))
    else:
        MAINDATA.update_acell("Z2",int(askWhichCycle))
    MAINDATA.append_row(new_row, 'USER_ENTERED')
    print "Row updated!"
    #check last row cycle again
    MAINDATAlastRow = len(MAINDATA.col_values(1))
    MAINDATAcurrentRow = MAINDATAlastRow + 1
    #get the new last row cycle
    lastRowCycle = MAINDATA.acell('A'+format(MAINDATAlastRow)).value
    sleep(1)
    print "."
    sleep(1)
    print "."
    sleep(1)
    print "."

if isDaemon == False:
    print "Filling out row for cycle "+format(askWhichCycle)
    updateSpreadsheets()
else:
    while True:
        if difference < 0:
            if (int(lastRowCycle)-latestCompleteCycle)<0:
                print "waiting 15 seconds before updating"
                sleep(10)
                print "updating in 5"
                sleep(1)
                print "4"
                sleep(1)
                print "3"
                sleep(1)
                print "2"
                sleep(1)
                print "1"
                sleep(1)
                updateSpreadsheets()
                difference += 1
                print "Updated difference to "+format(difference)
                checkForCycleDifference()
            if (int(lastRowCycle)-latestCompleteCycle)==0:
                cycle = latestCompleteCycle
                updateSpreadsheets()
                difference = 1
                print "stop updating"
                waitForCycle()
        else:
            print "stop updating"
            waitForCycle()
