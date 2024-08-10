import requests
from bs4 import BeautifulSoup
import json
import os
import logging
from datetime import datetime
from requests.adapters import HTTPAdapter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory to save articles
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Initialize storage
articles = {
    'BBC': [],
    'The Guardian': [],
    'CNN': [],
    'India Today': [],
    'News18': []
}

# Set up HTTP adapter without retries
adapter = HTTPAdapter()
http = requests.Session()
http.mount("http://", adapter)
http.mount("https://", adapter)

# Fetch articles from a URL
def fetch_articles(url, source_name, article_limit=100):
    logger.info(f"Fetching articles from {source_name}...")
    try:
        response = http.get(url)
        response.raise_for_status()
        logger.info(f"Successfully fetched page from {source_name}.")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        
        count = 0
        for link in links:
            if count >= article_limit:
                break
            article_url = link['href']
            if article_url.startswith('/'):
                article_url = f"https://{url.split('/')[2]}{article_url}"
            if article_url.startswith(('http', 'https')):
                try:
                    article_response = http.get(article_url)
                    if article_response.status_code == 200:
                        article_soup = BeautifulSoup(article_response.content, 'html.parser')
                        title = article_soup.find('title').text if article_soup.find('title') else 'No title'
                        content = article_soup.get_text()
                        articles[source_name].append({'url': article_url, 'title': title, 'content': content})
                        count += 1
                        logger.info(f"Fetched article {count} from {source_name}: {article_url}")
                    else:
                        logger.warning(f"Skipping article {article_url} due to error {article_response.status_code}.")
                except requests.RequestException as e:
                    logger.error(f"Error fetching article from {source_name}: {e}")
    except requests.RequestException as e:
        logger.error(f"Error fetching articles from {source_name}: {e}")

# Define sources
sources = {
    'BBC': 'https://www.bbc.com/news',
    'The Guardian': 'https://www.theguardian.com/international',
    'CNN': 'https://edition.cnn.com/world',
    'India Today': 'https://www.indiatoday.in',
    'News18': 'https://www.news18.com'
}

# Fetch articles from each source
for source, url in sources.items():
    fetch_articles(url, source)

# Save articles to file
output_file = os.path.join(data_dir, 'articles.json')
with open(output_file, 'w') as f:
    json.dump(articles, f, indent=2)
    
# Log summary
logger.info("Summary of articles fetched:")
for source, article_list in articles.items():
    logger.info(f"{source}: {len(article_list)} articles")

logger.info(f"Data saved to {output_file}")
