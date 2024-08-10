import json
import os

def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data

# Example usage
if __name__ == "__main__":
    data_path = os.path.join('data', 'articles.json')
    articles = load_data(data_path)
    
    print(f"Loaded {len(articles)} articles.")
