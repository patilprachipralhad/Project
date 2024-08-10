import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from nltk.tokenize import word_tokenize
from collections import Counter
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a simple model (example)
class SimpleSummarizer(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super(SimpleSummarizer, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.LSTM(embed_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)
    
    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.rnn(x)
        x = self.fc(x)
        return x

# Define TextDataset with padding
class TextDataset(Dataset):
    def __init__(self, file_path, vocab, max_length=512):
        self.data = []
        self.vocab = vocab
        self.pad_idx = len(vocab)  # Padding index
        self.max_length = max_length
        self.load_data(file_path)
    
    def load_data(self, file_path):
        logging.info(f"Loading data from {file_path}")
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    tokens = word_tokenize(line.strip())
                    indices = [self.vocab.get(token, self.pad_idx) for token in tokens]
                    # Apply padding
                    if len(indices) < self.max_length:
                        indices += [self.pad_idx] * (self.max_length - len(indices))
                    else:
                        indices = indices[:self.max_length]
                    self.data.append(indices)
        except FileNotFoundError:
            logging.error(f"File {file_path} not found.")
            raise
        except Exception as e:
            logging.error(f"An error occurred while loading data: {e}")
            raise
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return torch.tensor(self.data[idx])

# Define collate function for padding
def collate_fn(batch):
    return torch.stack(batch, dim=0)

# Load vocabulary
def load_vocab(vocab_file):
    vocab = {}
    logging.info(f"Loading vocabulary from {vocab_file}")
    try:
        with open(vocab_file, 'r') as file:
            for line in file:
                word, idx = line.strip().split('\t')
                vocab[word] = int(idx)
    except FileNotFoundError:
        logging.error(f"File {vocab_file} not found.")
        raise
    except Exception as e:
        logging.error(f"An error occurred while loading vocabulary: {e}")
        raise
    return vocab

# Validation function
def validate_model(model, dataloader, criterion, vocab_size):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch in dataloader:
            output = model(batch)
            loss = criterion(output.view(-1, vocab_size), batch.view(-1))
            total_loss += loss.item()
    avg_loss = total_loss / len(dataloader)
    logging.info(f'Validation Loss: {avg_loss}')
    return avg_loss

def train_model():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, '..', 'data', 'preprocessed_data.txt')
    vocab_file = os.path.join(script_dir, '..', 'data', 'vocabulary.txt')
    model_path = os.path.join(script_dir, '..', 'data', 'model.pth')

    vocab = load_vocab(vocab_file)
    vocab_size = len(vocab) + 1  # +1 for padding index

    dataset = TextDataset(input_file, vocab)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True, collate_fn=collate_fn)
    
    model = SimpleSummarizer(vocab_size=vocab_size, embed_size=128, hidden_size=256)
    criterion = nn.CrossEntropyLoss(ignore_index=len(vocab))
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    num_epochs = 10  # Increased to 10 for better fitting
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        logging.info(f"Epoch {epoch+1}/{num_epochs}")
        for batch in dataloader:
            optimizer.zero_grad()
            output = model(batch)
            loss = criterion(output.view(-1, vocab_size), batch.view(-1))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        avg_loss = total_loss / len(dataloader)
        logging.info(f'Epoch {epoch+1}/{num_epochs}, Training Loss: {avg_loss}')

        # Validation step (assuming you have a validation dataset)
        val_loss = validate_model(model, dataloader, criterion, vocab_size)
        logging.info(f'Epoch {epoch+1}/{num_epochs}, Validation Loss: {val_loss}')

    torch.save(model.state_dict(), model_path)
    logging.info(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
