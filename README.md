# Event Booker Google Calendar


## Description

Simple Python interface to talk to Google Calendar API. Able to:
- list upcomming events;
- create event from [json data](meeting_data.json);
- list user calendar settings. 

#### Backstory

Friend is working on ACT ON CRISIS startup, where php devs could not create google events WITH hangout video call, therefore process could not be automated.

Decided to expand python skills and first time interact with major API provider Google. 

### Hangouts Issue

As far as I explored it's impossible to change settings with API, only observe for changes, but video call could be easily added to every event created using calendar settings UI:

![hangouts](https://user-images.githubusercontent.com/45366313/79978216-3b26eb80-84a8-11ea-99c6-eb7a22457a96.JPG)

## Requirements and Installation

Install required packages:

`pip install -r requirements.txt`

Then overview code, and decide what you want to do. Uncomment any of these under Calendar class run method:

- `self.get_upcoming_events()`
- `self.create_event()`
- `self.list_user_settings()`

### First run

When running for first time, google should prompt for login in browser to ask to authorize permissions to script.

`token.pickle` file will be created and used in later runs.

## References

Based on google calendar API documentation pages:

- Google Calendar API Quickstart (Python) - [link](https://developers.google.com/calendar/quickstart/python)
- Create Event (Python) [link](https://developers.google.com/calendar/v3/reference/events/insert#python)