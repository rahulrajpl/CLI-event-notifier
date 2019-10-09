#!/usr/bin/env python
# Disclaimer:
# -----------
# Original code has been taken from the google developer website. 
# https: // developers.google.com/calendar/quickstart/python
# Modified the original code to give a desktop
# notification and a notification at the start of terminal window  
# of upcoming 'n' events logged in the Google Calendar

"""Google Calendar CLI Notifier

This program notifies you while you use it on linux operating system and also a reminder at
the start of the terminal window regarding upcoming 'n' google calendar events.

You should never miss a birthday/ anniversary 

Author(c) 2019
----------
Rahul Raj (github.com/rahulrajpl)
"""

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Number of upcoming events to read from calendar.
n = 10

def save_local_copy(upcoming_events):
    with open('events_local_copy', 'w') as f:
        for event in upcoming_events:
            e = ', '.join(event)
            f.write(e)
            f.write('\n')

def notify():
    if os.path.exists('events_local_copy'):
        with open('events_local_copy', 'r') as fileName:
            for line in fileName:
                line = line.split(',')
                # line[1] contains Date and line[2] contains Event Detail
                os.system('notify-send "Upcoming Events: ' + line[0] + ' ' + line[1] + '"')
                # print(line)
    else:
        main()


def main():
    """Shows basic usage of the Google Calendar API.
    
    Requests the user to grant permission to read the calendar. 
    Then displays n upcoming calendar events 
    """
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

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime. utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=n, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    upcoming_events = []

    if not events:
        # print('No upcoming events found.')
        save_local_copy(['Nil'])
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        
        year = int(start[0:4])
        month = int(start[5:7])
        day = int(start[8:10])
        x = datetime.datetime(year, month, day)
        # dtg = x.strftime("%b %d %Y %H:%M:%S")
        dtg = x.strftime("%b %d %Y")
        upcoming_events.append([dtg, event['summary']])
    print(upcoming_events)
    save_local_copy(upcoming_events)

    # os.system('notify-send "Upcoming events: ' + e + '"')
    # os.system('notify-send "Birthdays Today: ' + line[1]+ ' ' + line[2] + '"')
        # print(dtg, event['summary'])


if __name__ == '__main__':
    main()
    notify()
