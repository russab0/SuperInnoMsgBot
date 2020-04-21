from nltk.tokenize import sent_tokenize, word_tokenize
from random import random, choice, seed
from collections import Counter
from itertools import chain
from count_dict import CountDict
from prepare_data import get_messages
import numpy as np
import string
import nltk
import re

START = 'START'
END = 'END'
PUNCT = string.punctuation + '“”'

seed(1)
np.random.seed(1)
nltk.download('punkt')


def normalize(text, allow_asterix=False):
    text = text.lower()
    text = re.sub('\'', '', text)  # remove apostrophes
    text = re.sub(f'[{PUNCT}]', ' ', text)  # replace all punctuation signs with spaces

    if not allow_asterix:
        text = re.sub('\*', ' ', text)  # replace all astrixes (*) with spaces
    text = re.sub('[0-9]', ' ', text)  # replace all digits with spaces
    result = " ".join([x.lower() for x in text.split()])  # lower all letters and delete all doubled spaces
    return result


def messages_to_sentences(messages):
    return list(chain(
        *[[word_tokenize(normalize(sent)) for sent in sent_tokenize(msg)] for msg in messages]))


def bigram_nextword(sentences):
    bigrams = CountDict()
    next_words = dict()
    for i in range(len(sentences)):
        sent = [START] + sentences[i] + [END]
        for cur_token_pos in range(len(sent) - 1):
            cur_token, next_token = sent[cur_token_pos:cur_token_pos + 2]
            bigram = cur_token + ' ' + next_token
            if not bigram in bigrams:
                bigrams[bigram] = 0
            bigrams[bigram] += 1

            if not cur_token in next_words:
                next_words[cur_token] = set()
            next_words[cur_token].add(next_token)
    for k in next_words:
        next_words[k] = list(next_words[k])
    return bigrams, next_words


messages = get_messages()
print('MSG')
sent_sizes = [len(word_tokenize(sent)) for msg in messages for sent in sent_tokenize(msg)]
avg_sent_len = sum(sent_sizes) / len(sent_sizes)
avg_sent_num = sum([len(sent_tokenize(msg)) for msg in messages]) / len(messages)

sentences = messages_to_sentences(messages)
print('SENT')
term_c = CountDict(Counter(list(chain(*sentences))))  # dict()
term_c[START] = term_c[END] = len(sentences)
N = sum(term_c.values())

bigram_c, next_words = bigram_nextword(sentences)
bi_N = sum(bigram_c.values())

bigram_pop = sorted(list(bigram_c.items()),
                    key=lambda x: x[1],
                    reverse=True
                    )[:10]

print('bigram pop', bigram_pop)

bigram_start_pop = sorted(
    [x for x in bigram_c.items() if x[0].startswith(START)],
    key=lambda x: x[1],
    reverse=True
)[:10]
print('bigram pop', bigram_pop)

print('bigram start pop', bigram_start_pop)
