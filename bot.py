from preprocess import START, END, preprocess
from random import random
import os
import numpy as np
from telebot import TeleBot


# from telebot import apihelper


def conditional_prob(bigram_c, term_c, t1, t2):
    bigram = t1 + ' ' + t2
    if bigram_c[bigram] * term_c[t1] == 0:
        return 0
    return bigram_c[bigram] / term_c[t1]


def generate_sentence(bigram_c, term_c, next_words, sent_size):
    sent = []
    prev_word = START
    for j in range(round(sent_size)):
        if prev_word == END:
            break
        possible = next_words[prev_word]
        pdf = np.array([conditional_prob(bigram_c, term_c, prev_word, word) for word in possible])
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


def generate(bigram_c, term_c, next_words, sent_size, sent_num):
    text = [
        generate_sentence(bigram_c, term_c, next_words, sent_size)
        for _ in range(round(sent_num))
    ]
    return '. '.join(text)


def query(bigram_c, term_c, next_words, avg_sent_len, avg_sent_num):
    t = generate(bigram_c, term_c, next_words, round(avg_sent_len), round(avg_sent_num))
    return t


if 'tgtoken' in os.listdir():
    token = open('tgtoken', 'r').readline().strip()
    from telebot import apihelper

    PROXY = 'orbtl.s5.opennetwork.cc'
    PORT = 999
    USERNAME = 46321253
    PASSWORD = 'ThMSBJiT'
    apihelper.proxy = {'https': f'socks5://{USERNAME}:{PASSWORD}@{PROXY}:{PORT}'}
else:
    token = os.environ['tgtoken']

bot = TeleBot(token)

PATHS = {'si': 'ChatExport_SuperInno/',
         'zoo': 'ChatExport_Zoo/'}
si_bigram_c, si_term_c, si_next_words, si_avg_sent_len, si_avg_sent_num = preprocess(PATHS['si'])
zoo_bigram_c, zoo_term_c, zoo_next_words, zoo_avg_sent_len, zoo_avg_sent_num = preprocess(PATHS['zoo'])


@bot.message_handler(commands=['start'])
def help_command(message):
    bot.send_message(message.chat.id, "Для генерации случайного сообщения отправьте /new")


@bot.message_handler(commands=['new'])
def help_command(message):
    print(message)
    bot.send_message(message.chat.id,
                     query(si_bigram_c, si_term_c, si_next_words, si_avg_sent_len + 3, si_avg_sent_num))


@bot.message_handler(commands=['new_zoo'])
def help_command(message):
    print(message)
    bot.send_message(message.chat.id,
                     query(zoo_bigram_c, zoo_term_c, zoo_next_words, zoo_avg_sent_len + 2, zoo_avg_sent_num + 3))


bot.polling(none_stop=True, interval=0)
