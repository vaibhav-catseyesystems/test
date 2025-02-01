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
    messages=[
            {
            'role': 'system',
            'content': """You are helpfull ai that etract event list from given html markdown
            Extract all event/conference related links links from the given HTML markdown, excluding non-event links like press, privacy policy, work-with-us, about-us, contact-us, etc. Do not return code snippet,other explanation only return links.
            give response in json format like [{{eventName:eventname,eventDate:event date,eventLink:eventLink}}] and nothing else
            if some details not found then simply keep them blank do not add inaccurate information
            """,
            },
            {
            'role': 'user',
            'content': markdown,
            },
        ]
    return messages


def create_listing_page_prompt(markdown):
    messages=[
            {
            'role': 'system',
            'content': """You are helpfull ai that etract event listing page from given html markdown without repeating them or modifying them
            give response in json format like [{{listingLink:Listing page URL,listingPageName:name of listing page}}] and nothing else
            if some details not found then simply keep them blank do not add inaccurate information
            """,
            },
            {
            'role': 'user',
            'content': markdown,
            },
        ]
    return messages

def create_event_speakers_prompt(markdown):
    messages=[
            {
            'role': 'system',
            'content': """You are helpfull ai that etract event speakers from given html markdown without repeating them or modifying them
                first check if this contains event speakers if it contains speakers information you to return it
                give response in json format like [{{speakerName:name of the speaker, speakerDesignation:designation of speaker, speakerCompany:company of the speaker,speakerImage:profile image of speaker}}]
                if some details not found then simply keep them blank do not add inaccurate information and if no speakers found then simply return [] and nothing else
                """,
            },
            {
            'role': 'user',
            'content': markdown,
            },
        ]
    return messages
