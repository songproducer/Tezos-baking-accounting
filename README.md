# Tezos-baking-accounting

Requirements
Python2.7
pip install python-dateutil
pip install oauth2client
pip install gspread

Make a copy of this spreadsheet:
https://docs.google.com/spreadsheets/d/1NzfP5eLVGtNUol72dgo_bWE5qz8teVvHbkGUYMr335U/edit?usp=sharing

Go to share your copy and note the document's ID, copy/paste it between the quotes on line 61:
spreadsheet = gc.open_by_key('')

Use google to generate a credentials.json file:
https://console.cloud.google.com/apis/credentials/serviceaccountkey

Move everything into the TRD's calculations folder and export the path:
export GOOGLE_APPLICATION_CREDENTIALS="/home/leo/pymnt/reports/tz1ChangeThisToYourBakingAddress/calculations/credentials.json"

Run:
python gdaemon.py

Enter 'c' then 'y'
