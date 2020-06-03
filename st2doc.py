from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
from googleapiclient import discovery
import speedtest
import datetime
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Class for creating an object of JSON-files
class JsonData(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)

def testSpeed():
    """
    Returns a list with values to append to sheet.
    index 0: A date-time string
    index 1: Download speed
    index 2: Upload speed
    """
    st = speedtest.Speedtest()
    toReturn = list()

    toReturn.append(datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S"))
    toReturn.append(round(st.download()/10**6, 2))
    toReturn.append(round(st.upload()/10**6, 2))
    return toReturn

def main():
    # Read data-file and get sheet id
    with open('data.json', "r") as fh:
        jsonData = fh.read()
    parsedJson = JsonData(jsonData)

    spreadsheet_id = parsedJson.spreadsheetID
        
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    range_ = 'A1:C1' 

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'

    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'

    data = testSpeed()

    value_range_body = {
        "majorDimension": "COLUMNS",
        "values":[[data[0]], [str(data[1]).replace(".", ",")], [str(data[2]).replace(".", ",")]]
    }

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()

    pprint("Updated: {} cells".format(response["updates"]["updatedCells"]))

if __name__ == '__main__':
    main()