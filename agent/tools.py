# agent/tools.py

create_calendar_event_tool = {
    "type": "function",
    "function": {
        "name": "create_calendar_event",
        "description": "Create a Google Calendar event after user confirmation",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the user"
                },
                "date": {
                    "type": "string",
                    "description": "Event date in YYYY-MM-DD format"
                },
                "time": {
                    "type": "string",
                    "description": "Event start time in HH:MM (24-hour)"
                },
                "title": {
                    "type": "string",
                    "description": "Title of the calendar event"
                }
            },
            "required": ["name", "date", "time", "title"]
        }
    }
}