import pandas as pd
import numpy as np
import wordcloud
from get_records import get_records
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
    return (parse.normal_form)


def tokenize(text):  # разбиваем текст на слова
    if type(text) == str:
        words = [i for i in word_tokenize(text) if i not in stop_words and not i.isdigit()]
        words = [lemmatize(i) for i in words]
        return words
    else:
        return ''


def clear_text(text):
    result = tokenize(text)
    result = ' '.join(result)
    return(result)





def draw_total(df):
    text = df.clear_text.str.cat(sep=',')
    word_cloud = wordcloud.WordCloud(random_state=0,
                                     max_words=20,
                                     width=300 * 5,
                                     height=110 * 5,
                                     background_color="rgba(255, 255, 255, 0)",
                                     mode="RGBA",).generate(text)
    # word_cloud.recolor(grey_color_func)
    image = word_cloud.to_image()
    image.save(f'word_clouds_total.png')
    return 'word_clouds_total.png'


def draw_by_groups(data_text):
    for work_place in data_text['work_place'].unique():
        try:
            df_temp = data_text[data_text['work_place'] == work_place]
            for date in df_temp['date'].unique():
                df_temp_role = df_temp[df_temp['date'] == date]

                for role in df_temp_role['role'].unique():
                    df_to_wc = df_temp_role[df_temp_role['role'] == role]
                    text = ' '.join(df_to_wc['clear_text'])
                    word_cloud = wordcloud.WordCloud(random_state=0,
                                                     max_words=20,
                                                     width=300 * 5,
                                                     height=110 * 5,
                                                     background_color="rgba(255, 255, 255, 0)",
                                                     mode="RGBA",
                                                     ).generate(text)
                    # word_cloud.recolor(grey_color_func)
                    image = word_cloud.to_image()
                    image.save(f'word_clouds{work_place}_{date}_{role}.png')
        except:
            pass


# texts = get_records(work_place=1, role=0, date_time_start='2020-02-16', date_time_end='2020-06-20')


texts = get_records(work_place=1, role=0, date_time_start='2020-03-01', date_time_end='2020-03-27')
data_text = pd.DataFrame(texts, columns=['id', 'work_place', 'role', 'date', 'text'])
data_text['clear_text'] = data_text['text'].apply(clear_text)
draw_total(data_text)
texts = get_records(work_place=2, role=1, date_time_start='2020-04-5', date_time_end='2020-04-20')
data_text = pd.DataFrame(texts, columns=['id', 'work_place', 'role', 'date', 'text'])
data_text['clear_text'] = data_text['text'].apply(clear_text)
draw_total(data_text)
texts = get_records(work_place=3, role=0, date_time_start='2020-02-7', date_time_end='2020-02-20')
data_text = pd.DataFrame(texts, columns=['id', 'work_place', 'role', 'date', 'text'])
data_text['clear_text'] = data_text['text'].apply(clear_text)
draw_total(data_text)
texts = get_records(work_place=4, role=0, date_time_start='2020-04-28', date_time_end='2020-04-20')
data_text = pd.DataFrame(texts, columns=['id', 'work_place', 'role', 'date', 'text'])
data_text['clear_text'] = data_text['text'].apply(clear_text)
draw_total(data_text)
texts = get_records(work_place=5, role=1, date_time_start='2020-05-2', date_time_end='2020-05-20')
data_text = pd.DataFrame(texts, columns=['id', 'work_place', 'role', 'date', 'text'])
data_text['clear_text'] = data_text['text'].apply(clear_text)
draw_total(data_text)
texts = get_records(work_place=6, role=0, date_time_start='2020-04-14', date_time_end='2020-04-20')
data_text = pd.DataFrame(texts, columns=['id', 'work_place', 'role', 'date', 'text'])
data_text['clear_text'] = data_text['text'].apply(clear_text)
draw_total(data_text)
texts = get_records(work_place=7, role=1, date_time_start='2020-02-12', date_time_end='2020-02-20')
data_text = pd.DataFrame(texts, columns=['id', 'work_place', 'role', 'date', 'text'])
data_text['clear_text'] = data_text['text'].apply(clear_text)
draw_total(data_text)
texts = get_records(work_place=8, role=0, date_time_start='2020-03-16', date_time_end='2020-03-20')
data_text = pd.DataFrame(texts, columns=['id', 'work_place', 'role', 'date', 'text'])
data_text['clear_text'] = data_text['text'].apply(clear_text)
draw_total(data_text)