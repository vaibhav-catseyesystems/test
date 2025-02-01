
def create_event_details_prompt(markdown,url):
    messages=[
            {
            'role': 'system',
            'content': """You are helpfull ai that etract event related information such as event name, date, location, description
            give response in json format like {{eventName:suitable name for event,eventDate:date when event is taking place in dd/mm/yyyy format, eventLocation:Location of the given event,eventDescription:describe this event in 4-5 meaningful line,eventOrganizer:name of company institution which organised this event, spekaerLink:return speakers listing page link if speakers available,if }} 
            if some details not found then simply keep them blank do not add inaccurate information
            """,
            },
            {
            'role': 'user',
            'content': f'I need event information from {url} I have given its markdown below please extract event information from following in json format only',
            },
            {
            'role': 'user',
            'content': markdown,
            },
        ]
    return messages


