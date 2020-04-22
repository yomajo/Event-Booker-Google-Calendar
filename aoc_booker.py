# pylint: disable=maybe-no-member 
import datetime
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
JSON_FILE = 'meeting_data.json'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
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
    # get_upcoming_events(service)

    # Create event
    # create_event(service, JSON_FILE)

    # Check settings
    check_settings(service)

def check_settings(service):
    setting = service.settings().get(setting='autoAddHangouts').execute()
    print(f'about to request for user setting: \n')
    print(setting)

def parse_json(json_file):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    return json_data

def prepare_title(template:str, pro_name, client_name):
    return template.replace('<PRO_NAME>', pro_name).replace('<CLIENT_NAME>',client_name)

def create_event(service, json_file:str):
    json_data = parse_json(json_file)
    title = prepare_title(json_data['summary'], json_data['attendees']['pro_name'], json_data['attendees']['client_name'])

    event_details = {
    'summary': title,
    'description': json_data['description'],
    'start': {
        'dateTime': json_data['start']['dateTime'],
        'timeZone': 'Europe/Vilnius',
    },
    'end': {
        'dateTime': json_data['end']['dateTime'],
        'timeZone': 'Europe/Vilnius',
    },
    'attendees': [
        {'email': json_data['attendees']['pro_email']},
        {'email': json_data['attendees']['client_email']},
    ],
    'guestsCanInviteOthers' : False,
    'guestsCanSeeOtherGuests' : False
    }

    event = service.events().insert(calendarId='primary', body=event_details).execute()
    print(f'\nPrinting out event stuff: \nevent:{event}\n\ndir_event{dir(event)}')
    print (f'Event created: {event.get("htmlLink")}')

def get_upcoming_events(service):
    now = datetime.datetime.now().isoformat() + 'Z'
    print('Getting the upcoming 10 events\n')
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()