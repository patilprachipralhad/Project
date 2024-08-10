import json
import os
import re
import logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def preprocess_article(article):
    # Extract content and title
    content = article.get('content', '')
    title = article.get('title', '')

    # Combine title and content
    text = title + " " + content

    # Remove unnecessary characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'\d+', '', text)   # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation

    # Convert to lowercase
    text = text.lower()

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Reconstruct text from tokens
    processed_text = ' '.join(tokens)
    
    return processed_text

def preprocess_data(input_file, output_file):
    if not os.path.exists(input_file):
        logger.error(f"The file {input_file} does not exist.")
        return

    try:
        with open(input_file, 'r') as file:
            articles = json.load(file)
        
        logger.info(f"Successfully loaded data from {input_file}.")
        
        preprocessed_texts = []
        for source, article_list in articles.items():
            for article in article_list:
                preprocessed_text = preprocess_article(article)
                preprocessed_texts.append(preprocessed_text)
        
        with open(output_file, 'w') as file:
            for text in preprocessed_texts:
                file.write(text + '\n')

        logger.info(f"Preprocessed data saved to {output_file}.")
    
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {input_file}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Determine the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct file paths relative to the script directory
    input_path = os.path.join(script_dir, '..', 'data', 'articles.json')
    output_path = os.path.join(script_dir, '..', 'data', 'preprocessed_data.txt')
    
    preprocess_data(input_path, output_path)
