import os
import subprocess

KALDI_RU_DIR = '../../kaldi-ru-0.6/'
FILES_TO_RECGN_DIR = '../data/'

class Recognize():
    def __init__(self, ):
        pass

    def file(self, file_to_recgn, logging=False):

        recgn_proc = subprocess.Popen(f"cd {KALDI_RU_DIR};"
                                    f"sh ./decode.sh {file_to_recgn} "
                                    f"{FILES_TO_RECGN_DIR}",
                                    shell=True,
                                    universal_newlines=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,

                                    )

        data, error = recgn_proc.communicate()
        if logging:
            return data
        else:
            data = [i.replace(file_to_recgn + ' ', '') for i in data.split('\n') if i.startswith(file_to_recgn)]
            data_obj = {}
            data_obj['raw_text'] = data[0]
            data_obj['words'] = data[1:]
            return data_obj

    def folder(self):
        data_obj = {}

        for file_name in [i.replace('.wav', '') for i in os.listdir(KALDI_RU_DIR+FILES_TO_RECGN_DIR) if i.endswith('.wav')]:
            data_obj[file_name] = self.file(file_name)

        return data_obj

#print(Recognize().file('1564615186602'))
#print(Recognize().folder())