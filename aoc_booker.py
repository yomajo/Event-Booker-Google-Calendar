# pylint: disable=maybe-no-member 
import datetime
import pickle
import os.path
import json
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
JSON_FILE = 'meeting_data.json'

class Calendar():
    '''Interacts with Google Calendar API. run() is main class method. Accepts event data in json (path to file)'''

    def __init__(self, json_file):
        self.json_file = json_file
        self.service = self.init_service()

    def init_service(self):
        '''establishes a connection to calendar API and returns service object to work with'''
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
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
        try:
            service = build('calendar', 'v3', credentials=creds)
            return service
        except Exception as e:
            print(f'Failed to establish connection to Calendar API. Error: {e}. Terminating...')
            sys.exit()

    def list_user_settings(self):
        '''lists user current calendar settings'''
        settings = self.service.settings().list().execute()
        for setting in settings['items']:
            print(f'Setting: {setting["id"]}, value: {setting["value"]}')
    
    @staticmethod
    def parse_json(json_file):
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        return json_data

    def get_upcoming_events(self):
        '''Shows basic usage of the Google Calendar API. Prints the start and name of the next 10 events on the user's calendar'''
        now = datetime.datetime.now().isoformat() + 'Z'
        print('Getting the upcoming 10 events\n')
        events_result = self.service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    @staticmethod            
    def prepare_title(template:str, pro_name, client_name):
        return template.replace('<PRO_NAME>', pro_name).replace('<CLIENT_NAME>',client_name)

    def create_event(self):
        '''creates event from hardcoded tempalte and cls accepted json values'''
        json_data = self.parse_json(self.json_file)
        title = self.prepare_title(json_data['summary'], json_data['attendees']['pro_name'], json_data['attendees']['client_name'])
        # Pluging in values from json:
        event_details = {
        'summary': title,
        'description': json_data['description'],
        'start': {'dateTime': json_data['start']['dateTime'], 'timeZone': json_data['timeZone']},
        'end': {'dateTime': json_data['end']['dateTime'], 'timeZone': json_data['timeZone']},
        'attendees': [{'email': json_data['attendees']['pro_email']},{'email': json_data['attendees']['client_email']}],
        'guestsCanInviteOthers' : False,
        'guestsCanSeeOtherGuests' : False
        }
        # Creating event:
        event = self.service.events().insert(calendarId='primary', body=event_details).execute()
        print(f'\nPrinting out event details: \nevent:{event}\n')
        print (f'Event created: {event.get("htmlLink")}')
    
    def run(self):
        '''comment/uncomment for certain actions'''
        # self.get_upcoming_events()
        self.create_event()
        # self.list_user_settings()


if __name__ == '__main__':
    Calendar(JSON_FILE).run()    