import os
from collections import Counter
from nltk.tokenize import word_tokenize
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def build_vocab(input_file, vocab_file):
    try:
        with open(input_file, 'r') as file:
            texts = file.readlines()
        
        # Tokenize all texts
        tokens = [word_tokenize(text) for text in texts]
        flat_tokens = [item for sublist in tokens for item in sublist]
        
        # Build vocabulary
        vocab = Counter(flat_tokens)
        
        # Save vocabulary
        with open(vocab_file, 'w') as file:
            for word, freq in vocab.items():
                file.write(f"{word}\t{freq}\n")
        
        logger.info(f"Vocabulary saved to {vocab_file}.")
    except Exception as e:
        logger.error(f"Error building vocabulary: {e}")

# Main execution
if __name__ == "__main__":
    # Determine the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct file paths relative to the script directory
    input_path = os.path.join(script_dir, '..', 'data', 'preprocessed_data.txt')
    vocab_path = os.path.join(script_dir, '..', 'data', 'vocabulary.txt')
    
    build_vocab(input_path, vocab_path)
