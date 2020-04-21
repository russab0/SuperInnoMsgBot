from preprocess import START, END, bigram_c, term_c, next_words, avg_sent_len, avg_sent_num
from random import random
import os
import numpy as np
from telebot import TeleBot


# from telebot import apihelper


def conditional_prob(t1, t2):
    bigram = t1 + ' ' + t2
    if bigram_c[bigram] * term_c[t1] == 0:
        return 0
    return bigram_c[bigram] / term_c[t1]


def generate_sentence(bigrams, next_words, sent_size):
    sent = []
    prev_word = START
    for j in range(round(sent_size)):
        if prev_word == END:
            break
        possible = next_words[prev_word]
        pdf = np.array([conditional_prob(prev_word, word) for word in possible])
        cdf = np.cumsum(pdf)

        cur_word = possible[0]
        r = random()
        for i in range(len(cdf)):
            if cdf[i] > r:
                cur_word = possible[i]
                break
        sent.append(cur_word)
        prev_word = cur_word

    sent[0] = sent[0].capitalize()
    return ' '.join(sent[:-1])


def generate(bigrams, next_words, sent_size, sent_num):
    text = [
        generate_sentence(bigrams, next_words, sent_size)
        for _ in range(round(sent_num))
    ]
    return '. '.join(text)


def query():
    t = generate(bigram_c, next_words, round(avg_sent_len + 3), round(avg_sent_num))
    return t


if 'tgtoken' in os.listdir():
    token = open('tgtoken', 'r').readline().strip()
else:
    token = os.environ['tgtoken']
bot = TeleBot(token)

PROXY = 'orbtl.s5.opennetwork.cc'
PORT = 999
USERNAME = 46321253
PASSWORD = 'ThMSBJiT'


# apihelper.proxy = {'https': f'socks5://{USERNAME}:{PASSWORD}@{PROXY}:{PORT}'}


@bot.message_handler(commands=['start'])
def help_command(message):
    bot.send_message(message.chat.id, "Для генерации случайного сообщения отправьте /new")


@bot.message_handler(commands=['new'])
def help_command(message):
    bot.send_message(message.chat.id, query())


bot.polling(none_stop=True, interval=0)
