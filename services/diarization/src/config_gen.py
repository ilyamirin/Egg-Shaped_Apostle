# creates config.ini and sets default settings if not exists
import sys, os
import configparser

pathname = os.path.dirname(sys.argv[0])
path = os.path.abspath(pathname)
root_dir = os.path.abspath(os.path.join(path, '..'))


def get_config():
    config = configparser.ConfigParser()
    if 'config.ini' in os.listdir(root_dir):
        config.read(os.path.join(root_dir, 'config.ini'))
    else:
        config['ENV'] = {
            'ROOT_ABS_PATH': root_dir,
            'EXT_DATA_DIR': os.path.join(root_dir, 'data')
        }

        config['NETWORK'] = {
            'WEB_API_IP': '0.0.0.0',
            'WEB_API_PORT': 5732,
        }

        config['DIARIZATION_CORE'] = {
            'VALIDATE_DIR': os.path.join(root_dir, 'resources/vad_ami_sber/train/SBERBANK'
                                               '.SpeakerDiarization.SberCorpus.train'
                                               '/validate_detection_fscore/SBERBANK'
                                               '.SpeakerDiarization.SberCorpus.development'),
            'PARAMS': os.path.join(root_dir, 'resources/dia_sber/train/SBERBANK.SpeakerDiarization.'
                                             'SberCorpus.development/params.yml'),
        }

        config['SETTINGS'] = {
            'DEBUG': 1,
        }

        with open(os.path.join(root_dir, 'config.ini'), 'w') as config_file:
            config.write(config_file)
    return config


get_config()
