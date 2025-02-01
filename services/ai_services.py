import json
import re
from ai_model.ai_model import tokenizer,model
from utils.ai_utils import create_event_details_prompt,create_event_list_prompt, create_event_speakers_prompt, create_listing_page_prompt, split_content_with_overlap
import logging

def model_response(prompt):
    try:
        text = tokenizer.apply_chat_template( prompt, tokenize=False, add_generation_prompt=True )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        generated_ids = model.generate(**model_inputs, max_new_tokens=2048)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response,None
    except Exception as e:
        return None,str(e)

def get_event_details_with_ai(markdown,url):
    try:
        prompt=create_event_details_prompt(markdown=markdown,url=url)
        response,error=model_response(prompt=prompt)
        if error:
            return {"data":None,"error":f"error while getting response from model {error}"}
        json_object_pattern = re.compile(r"\{.*?\}", re.DOTALL)
        match = json_object_pattern.findall(response)[0]
        try:
            event_data = json.loads(match)
            event_name = event_data.get('eventName', "")
            event_date = event_data.get('eventDate', "")
            event_location = event_data.get('eventLocation', "")
            event_description = event_data.get('eventDescription',"")
            event_organizer = event_data.get('eventOrganizer', "")
            speaker_link = event_data.get('speakerLink', "")
            return {"data":{"eventName":event_name,"eventDate":event_date,"eventLocation":event_location,"eventDescription":event_description,"eventOrganizer":event_organizer,"speakerLink":speaker_link},"error":None}
        except Exception as e:
            logging.error(f"Error while extracting event data {e}")
            return {"data":None,"error":f"error parsing model response {e}"}
    except Exception as e:
        logging.error(f"Exception while getting event details from AI model {e}")
        return {"data":None,"error":f"Exception while getting event details from AI model {e}"}

def get_events_list_with_ai(markdown):
    try:
        chunks=split_content_with_overlap(markdown)
        qwenResults=[]
        for i, chunk in enumerate(chunks, start=1):
            prompt=create_event_list_prompt(markdown=chunk)
            response,error=model_response(prompt=prompt)
            if error:
                return {"data":None,"error":f"error while getting response from model {error}"}
            qwenResults.append(str(response))
        parsed_objects = []
        for obj in qwenResults:
            json_object_pattern = re.compile(r"\{.*?\}", re.DOTALL)
            matches = json_object_pattern.findall(obj)
            for match in matches:
                try:
                    event = json.loads(match)
                    event_link = event["eventLink"]
                    if not event_link.startswith("http"):
                        print(f"{event_link} needs to reformatted...")
                    parsed_objects.append(event)
                except Exception as e:
                    logging.error(f"Error processing event object {match} {e}")
        return {"data":parsed_objects,"error":None}
    except Exception as e:
        logging.error(f"Exception while getting events list with ai {e}")
        return {"data":None,"error":f"Exception while getting event link with AI {e}"}

def get_event_listing_page_with_ai(markdown):
    try:
        chunks=split_content_with_overlap(markdown)
        qwenResults=[]
        for i, chunk in enumerate(chunks, start=1):
            prompt=create_listing_page_prompt(markdown=chunk)
            response,error=model_response(prompt=prompt)
            if error:
                return {"data":None,"error":f"error while getting response from model {error}"}
            qwenResults.append(str(response))
        parsed_objects = []
        for obj in qwenResults:
            json_object_pattern = re.compile(r"\{.*?\}", re.DOTALL)
            matches = json_object_pattern.findall(obj)
            for match in matches:
                try:
                    event = json.loads(match)
                    event_link = event["listingLink"]
                    if not event_link.startswith("http"):
                        print(f"{event_link} needs to reformatted...")
                    event["listingLink"]=event["listingLink"].split('?')[0].split('#')[0]
                    if not any(entry['listingLink'] == event["listingLink"] for entry in parsed_objects):
                        parsed_objects.append(event)
                except Exception as e:
                    logging.error(f"Error processing listing object {match} {e}")
        return {"data":parsed_objects,"error":None}
    except Exception as e:
        logging.error(f"Exception while getting event listing page with AI {e}")
        return {"data":None,"error":f"Exception while getting event listing page with AI {e}"}

def get_event_speakers_with_ai(markdown):
    try:
        prompt=create_event_speakers_prompt(markdown=markdown)
        response,error=model_response(prompt=prompt)
        if error:
            return {"data":None,"error":f"error while getting response from model {error}"}
        json_object_pattern = re.compile(r"\{.*?\}", re.DOTALL)
        matches = json_object_pattern.findall(response)
        speakers=[]
        for match in matches:
            try:
                spk_data = json.loads(match)
                speaker_name = spk_data.get('speakerName', "")
                speaker_designation = spk_data.get('speakerDesignation', "")
                speaker_company = spk_data.get('speakerCompany', "")
                speaker_image = spk_data.get('speakerImage', "")
                speakers.append({"speaker_name":speaker_name,"speaker_designation":speaker_designation,"speaker_company":speaker_company,"speaker_image":speaker_image})
            except Exception as e:
                logging.error(f"Error processing speaker object {match} {e}")
        return {"data":speakers,"error":None}
    except Exception as e:
        logging.error(f"Exception while getting speakers list with ai {e}")
        return {"data":None,"error":f"Exception while getting speakers with AI {e}"}
