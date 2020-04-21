import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

PATH = 'ChatExport_SuperInno/'


def get_messages():
    messages = []
    if 'messages.csv' in os.listdir():
        return pd.read_csv('messages.csv')['data'].tolist()
    for file_name in tqdm(os.listdir(PATH), desc='Reading data'):
        if not file_name.startswith('messages'):
            continue
        file = open(PATH + file_name, 'r')
        soup = BeautifulSoup(file, 'html.parser')
        messages += [x.text.strip() for x in soup.findAll('div', class_='text')]

    df = pd.DataFrame(messages, columns=["data"])
    df.to_csv('messages.csv', index=False)
    return messages
