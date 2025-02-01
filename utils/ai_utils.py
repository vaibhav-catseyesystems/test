def split_content_with_overlap(dom_content, max_length=30000, overlap=500):
    chunks = []
    for i in range(0, len(dom_content), max_length - overlap):
        chunks.append(dom_content[i : i + max_length])
    return chunks

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


def create_event_list_prompt(markdown):
    prompt=f"""
    Below i have given markdown content of html webpage
    Extract all event/conference related links links from the given HTML, excluding non-event links like press, privacy policy, work-with-us, about-us, contact-us, etc. Do not return code snippet,other explanation only return links.
    give response in json format like [{{eventName:eventname,eventDate:event date,eventLink:eventLink}}] and nothing else
    {markdown}
    """
    return prompt