import torch
import spacy
import logging
from torch.nn.functional import softmax
from model.train_model import SimpleSummarizer  # Import your model

# Load your NLP model (ensure it's compatible with your summarizer) 
nlp = spacy.load("en_core_web_sm")

# Load your trained model
def load_model(model_path, vocab_size):
    model = SimpleSummarizer(vocab_size=vocab_size, embed_size=128, hidden_size=256)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

# Load vocabulary
def load_vocab(vocab_file):
    vocab = {}
    with open(vocab_file, 'r') as file:
        for line in file:
            word, idx = line.strip().split('\t')
            vocab[word] = int(idx)
    return vocab

# Initialize model and vocabulary
vocab_file = "data/vocabulary.txt"
model_path = "data/model.pth"
vocab = load_vocab(vocab_file)
vocab_size = len(vocab) + 1  # +1 for padding index
model = load_model(model_path, vocab_size)

def summarize_text(text):
    """
    Summarize the provided text using the custom-trained model.
    """
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    # For simplicity, let's just return the first few sentences
    summary = ' '.join(sentences[:min(5, len(sentences))])
    return summary

def fetch_text_from_url(url):
    """
    Fetch and extract text from the given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join(p.get_text() for p in paragraphs)
        
        # You might want to do additional cleaning or processing here
        return article_text
    
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching the URL: {str(e)}")
