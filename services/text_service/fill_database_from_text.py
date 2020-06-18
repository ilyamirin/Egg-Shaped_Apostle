from random import randint, choice
import pandas as pd
from interface import record_create


def mock_data():
    workplace = randint(1, 8)
    role = randint(0, 1)

    month = randint(3, 6)
    day = randint(1, 28)
    date = f'2020-{month}-{day}T23:48:35.354930'
    # 0_0_0_2020-06-16T23:48:35.354930.wav
    return workplace, role, date


def mock_text(text_list):
    n_templates = len(text_list)
    n_to_use = 10
    text = ''
    for i in range(n_templates):
        template = choice(text_list)
        text += ' '+template
    return text


def fill_table_mock_text(filename, n_templates):
    with open(filename) as scripts:
        text = scripts.read().split('\n')

    for i in range(n_templates):
        text_mock = mock_text(text)
        data = mock_data()
        record_create(*data, text_mock)
        print(*data, text_mock)
    return


def fill_table_real_text(filename, text_list):
    for text in text_list:
        data = mock_data()
        record_create(*data, text)
        print(*data, text)
    return

files = ['sber_questions_1453.xlsx',
         'sber_questions_2906.xlsx',
         'sber_questions_4359.xlsx',
         'sber_questions_5814.xlsx']

text_total = []
for file in files:
    text = list(pd.read_excel(file)['q'])
    text_total = text_total + text
    for text in text_total:
        data = mock_data()
        record_create(*data, text)






