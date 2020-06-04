# Speedtest-to-Google-Sheets
 A python script that logs internet speed to a google sheet

## Config
1. Run the following command to install all libraries needed: ```pip install --upgrade speedtest-cli google-api-python-client google-auth-httplib2 google-auth-oauthlib```
1. Create a Google Sheets API with an OAuth 2.0 Client ID. Save credentials as "credentials.json" in project folder.
1. Create a Google Sheet and set following cells: A1 = Datetime, B1 = Download, C1 = Upload
1. Set up a diagram over the columns A:C
1. Copy the sheet id and paste into "data.json".
1. Run the script!
