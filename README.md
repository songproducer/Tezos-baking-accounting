# Tezos-baking-accounting

## Requirements
Python2.7

>pip install python-dateutil oauth2client gspread

## Setup
Make a copy of this spreadsheet:

https://docs.google.com/spreadsheets/d/1NzfP5eLVGtNUol72dgo_bWE5qz8teVvHbkGUYMr335U/edit?usp=sharing

Go to share your copy and note the document's ID, copy/paste it between the quotes on line 61:

spreadsheet = gc.open_by_key('')

Use Google to generate a credentials.json file:

https://console.cloud.google.com/apis/credentials/serviceaccountkey

Move gdaemon.py and credentials.json into [TRD](https://github.com/habanoz/tezos-reward-distributor) **calculations** folder and export the path:

export GOOGLE_APPLICATION_CREDENTIALS="/home/leo/pymnt/reports/**tz1ChangeThisToYourBakingAddress**/calculations/credentials.json"

## Running the daemon

python gdaemon.py

Enter 'y' then 'c'

If you want to know frozen amounts make changes to the addresses in the tzstats API worksheet.

Credit for original worksheet, charts and this idea goes to TezWhale.

## Donations

Donations gratefully accepted

tz1M9YZxNwGsqMXn9k6rNR8hMTA6JGAVgX6X
