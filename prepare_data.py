import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd


def get_messages(path):
    print('PATH', path)
    messages = []
    if 'messages.csv' in os.listdir(path):
        return pd.read_csv(path + 'messages.csv')['data'].tolist()
    for file_name in tqdm(os.listdir(path), desc='Reading data'):
        if not file_name.startswith('messages'):
            continue
        file = open(path + file_name, 'r')
        soup = BeautifulSoup(file, 'html.parser')
        messages += [x.text.strip() for x in soup.findAll('div', class_='text')]

    df = pd.DataFrame(messages, columns=["data"])
    df.to_csv(path + 'messages.csv', index=False)
    return messages
