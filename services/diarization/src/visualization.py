import os
import plotly.express as px
import pandas as pd
import numpy as np
import json
from dateutil import parser
from datetime import datetime, timedelta

from diarization import diarize
import db

from logger import get_logger
from config_gen import get_config

config = get_config()
logger = get_logger("diarization_service", config['SETTINGS']['DEBUG'])


def extract_metadata(filename):
    raspberry, card, device, date = filename[:-4].split(
        '_')  # разбиваем название файла по "_", получаем метаданные расположения
    return raspberry, card, device, parser.isoparse(date)


def visualize(filename):
    filename = os.path.basename(filename)
    if filename in db.get_list_of_diarized():
        annotation = diarize(filename)
        rasp, card, mic, date = extract_metadata(filename)
        df = pd.DataFrame([{
            'label': i['label'],
            'start': date + timedelta(seconds=round(i['segment']['start'])),
            'end': date + timedelta(seconds=round(i['segment']['end']))}
            for i in annotation['content'] if not str(i['label']).isdigit()])

        fig = px.timeline(df, x_start="start", x_end="end", y="label", color="label")
        fig.update_layout({
            'plot_bgcolor': 'rgba(255, 255, 255, 1)',
            'paper_bgcolor': 'rgba(255, 255, 255, 1)',
        })
        # fig.write_html('viz_1.html')
        return fig.to_image(format="svg", engine="kaleido")