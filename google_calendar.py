import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

class GoogleCalendar:
    def __init__(self, credentials, calendar_id):
        self.credentials = credentials
        self.calendar_id = calendar_id
        self.service = build('calendar','v3',credentials = service_account.Credentials.from_service_account_info(self.credentials, scopes = ["https://www.googleapis.com/auth/calendar"]))
        
    def create_event(self, event_name, start_time, end_time, timezone, attendes = None):
        event={
            'summary': event_name,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone
            }
        }
        
        if attendes:
            event['attendes'] = [{"email": email} for email in attendes]
            
        try:
            created_event = self.service.events().insert(calendarId = self.calendar_id, body = event).execute()
        except HttpError as error:
            raise Exception(f"Ocurrió un error: {error}")
        
        return created_event
    
    def get_events(self, date = None):
        if not date:
            events = self.service.events().list(calendarId = self.calendar_id).execute()
        else:
            start_date = f"{date}T00:00:00Z"
            end_date = f"{date}T23:59:00Z"
            events = self.service.events().list(calendarId = self.calendar_id, timeMin = start_date, timeMax = end_date).execute()
            
        return events.get('items',[])
            
    
    def get_event_start_time(self,date):
        events = self.get_events(date)
        start_times = []
        
        for event in events:
            start_time = event['start']['dateTime']
            parsed_start_time = datetime.fromisoformat(start_time[:-6])
            hours_minutes = parsed_start_time.strftime("%H:%M")
            start_times.append(hours_minutes)
            
        return start_times
