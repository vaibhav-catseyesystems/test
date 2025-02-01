import json
import re
from ai_model.ai_model import tokenizer,model
from utils.ai_utils import create_event_details_prompt
import logging

def get_event_details_with_ai(markdown,url):
    try:
        messages=create_event_details_prompt(markdown=markdown,url=url)
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=2048
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
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
