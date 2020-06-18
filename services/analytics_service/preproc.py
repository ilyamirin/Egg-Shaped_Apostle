import requests
from get_records import get_records
import pandas as pd
import numpy as np
import sys
import re
from os import listdir, getcwd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
nltk.download('stopwords')
nltk.download('punkt')

stop_words = stopwords.words('russian')+['это', 'свой']
morph_analyzer = MorphAnalyzer()

storage_service_api = 'http://127.0.0.1:5730'
analytics_service_api = 'http://127.0.0.1:5731'


def lemmatize(word):  # приводим слова в нормальную форму
    parse = morph_analyzer.parse(word)[0]
    return (parse.normal_form + '_' + parse.tag.POS)


def tokenize(text):  # разбиваем текст на слова
    if type(text) == str:
        words = [i for i in word_tokenize(text) if i not in stop_words and not i.isdigit()]
        words = [lemmatize(i) for i in words if morph_analyzer.parse(i)[0].tag.POS != None]
        return words
    else:
        return ''

results = get_records(work_place=1, role=0, date_time_start='2020-02-16', date_time_end='2020-06-20')

data_all = pd.DataFrame(results, columns=['id', 'work_place', 'role', 'date', 'text'])

data_proc = data_all.copy() # создаем рабочий экзмепляр данных

data_proc['text'] = [tokenize(i) for i in data_all['text']] # токенизируем текст, замещаем в датафрейме
data_proc = data_proc[data_proc['text'].apply(len) != 0] # убираем пустые текста

all_words_with_meta = [] # создаем промежуточный список для последующего создания датафрейма
for sample in data_proc.iterrows(): # идем по датафрейму, выбираем слова, забираем их параметры
    for word in sample[1]['text']:
        all_words_with_meta.append([word, sample[1]['work_place'], sample[1]['role'], sample[1]['date']])

all_words_with_meta = np.array(all_words_with_meta) # переводим в массив numpy
df_words = pd.DataFrame({'word':all_words_with_meta[:, 0],
                         'work_place':all_words_with_meta[:, 1],
                         'role':all_words_with_meta[:, 2],
                         'date':all_words_with_meta[:, 3]})

df_words['word_clean'] = df_words['word'].apply(lambda x: re.sub(r'(_[^_]*$)', '', x)) #чистим слова от частей речи

#предварительно отсортируем рабочие места, роли и даты для правильной конкатенации
work_places = list(set(df_words['work_place']))
work_places.sort()
dates = list(set(df_words['date']))
dates.sort()
roles = list(set(df_words['role']))
roles.sort()


#функция расчета частоты
def get_freq(work_place='all', date='all'):
    word_freqs = []
    if work_place == 'all' and date == 'all':
        words = df_words['word']
    elif date== 'all':
        words = df_words['word'][df_words['work_place'] == work_place]
    elif work_place == 'all':
        words = df_words['word'][df_words['date'] == date]
    else:
        words = df_words['word'][df_words['work_place'] == work_place and df_words['date'] == date]
    freqs_dist = nltk.FreqDist(words)
    for word in words:
        word_freqs.append(freqs_dist[word])
    return word_freqs, list((np.array(word_freqs)/len(words)))

#общая частота
freq_common = get_freq()
df_words['freqs_common'], df_words['freqs_common_scaled'] = freq_common[0], freq_common[1]

df_words.sort_values('work_place', inplace = True)

#считаем частоты слов по группам и датам
work_place_id = []

i = 0
for work_place in work_places:
    for work_place_ in df_words['work_place']:
        if work_place_ == work_place:
            work_place_id.append(i)
    i += 1

df_words['work_place_id'] = work_place_id

freq_work_places = []
freq_work_places_scaled = []

for work_place in work_places:
    freq_work_places_all = get_freq(work_place=work_place)
    freq_work_places += freq_work_places_all[0]
    freq_work_places_scaled += freq_work_places_all[1]

df_words['freq_work_places'] = freq_work_places
df_words['freq_work_places_scaled'] = freq_work_places_scaled

freq_dates = []
freq_dates_scaled = []

df_words.sort_values('date', inplace = True)
for date in dates:
    freq_dates_all = get_freq(date=date)
    freq_dates += freq_dates_all[0]
    freq_dates_scaled += freq_dates_all[1]

df_words['freqs_date'] = freq_dates
df_words['freqs_date_scaled'] = freq_dates_scaled

df_words.to_csv('dataset.csv')