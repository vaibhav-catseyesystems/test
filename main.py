from flask import Flask
from flask_cors import CORS
from routes.ai_routes import event_scrape_ai_bp
import logging


app = Flask(__name__)
CORS(app)
app.register_blueprint(event_scrape_ai_bp)

@app.route('/', methods=['GET'])
def getHome():
    return {"message": "model server is running..."}

if __name__ == '__main__':
    try:
        app.run(debug=True, port=7001,host="0.0.0.0")
    except Exception as e:
        logging.error(f"Error in server {e}")