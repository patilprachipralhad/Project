import sys
import os
import logging
from flask import Flask, render_template, request, jsonify
from .summarizer import summarize_text, fetch_text_from_url

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__, static_folder='../static', template_folder='../app/templates')

@app.route('/')
def index():
    logging.info("Rendering index page")
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json  # Use request.json to get JSON data
    logging.debug(f"Received form data: {data}")
    article_text = data.get('article_text', '').strip()
    article_url = data.get('article_url', '').strip()

    if not article_text and not article_url:
        logging.warning("No text or URL provided")
        return jsonify({'error': 'No text or URL provided'}), 400

    if article_url:
        logging.info(f"Fetching text from URL: {article_url}")
        try:
            article_text = fetch_text_from_url(article_url)
        except RuntimeError as e:
            logging.error(f"Error fetching text from URL: {e}")
            return jsonify({'error': str(e)}), 400

    if not article_text:
        logging.warning("No text provided")
        return jsonify({'error': 'No text provided'}), 400

    logging.info("Generating summary")
    summary = summarize_text(article_text)
    logging.debug(f"Generated summary: {summary}")
    return jsonify({'summary': summary})

if __name__ == '__main__':
    logging.info("Starting Flask app")
    app.run(host='0.0.0.0', port=5000,debug=True)
