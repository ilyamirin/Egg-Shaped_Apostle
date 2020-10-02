import os
from pyannote.audio.features import Pretrained
from pyannote.audio.pipeline import SpeakerDiarization
import db

from config_gen import get_config
config = get_config()


validate_dir = config['DIARIZATION_CORE']['VALIDATE_DIR']
diarization = SpeakerDiarization(sad_scores=Pretrained(validate_dir=validate_dir),
                                  scd_scores='scd_ami',
                                  embedding='emb_voxceleb',
                                  metric='cosine',
                                  method='affinity_propagation')

diarization.load_params(config['DIARIZATION_CORE']['PARAMS'])

diarization.initialize()


def diarize(filename):
    abs_filename = filename
    filename = os.path.basename(filename)
    if filename in db.get_list_of_diarized():
        annotation = db.get_annotation_by_filename(filename)
    else:
        annotation = diarization({'audio': abs_filename}).for_json()
        db.create_record(filename, annotation)
    return annotation