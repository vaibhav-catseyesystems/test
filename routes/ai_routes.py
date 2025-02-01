from flask import Blueprint, request, jsonify
from services.ai_services import get_event_details_with_ai,get_events_list_with_ai
import logging

event_scrape_ai_bp=Blueprint('event_scrape_ai',__name__)

@event_scrape_ai_bp.route('/get-event-data-with-ai',methods=['POST'])
def get_event_data_with_ai():
    try:
        data=request.json
        if not data:
            return jsonify({"data":None,"error": "Invalid JSON format"}), 400
        url=str(data['url']).strip()
        markdown=str(data['markdown']).strip()
        logging.info(f"request received for /get-event-data-with-ai {url}")
        res=get_event_details_with_ai(markdown=markdown,url=url)
        if res["error"]:
            return jsonify({"data": None, "error": res["error"]}), 400
        return jsonify({"data": res['data'], "error": None}), 200
    except Exception as e:
        logging.info(f"Error at /get-event-data-with-ai {e}")
        return jsonify({"data": None, "error": str(e)}), 500

@event_scrape_ai_bp.route('/get-event-list-with-ai',methods=['POST'])
def get_event_list_with_ai():
    try:
        data=request.json
        if not data:
            return jsonify({"data":None,"error": "Invalid JSON format"}), 400
        markdown=str(data['markdown']).strip()
        logging.info(f"request received for /get-event-list-with-ai")
        res=get_events_list_with_ai(markdown=markdown)
        if res["error"]:
            return jsonify({"data": None, "error": res["error"]}), 400
        return jsonify({"data": res['data'], "error": None}), 200
    except Exception as e:
        logging.info(f"Error at /get-event-list-with-ai {e}")
        return jsonify({"data": None, "error": str(e)}), 500
