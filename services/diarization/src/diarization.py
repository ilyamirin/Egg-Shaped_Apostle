from pyannote.audio.features import Pretrained
from pyannote.audio.pipeline import SpeakerDiarization

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
    return diarization({'audio': filename}).for_json()

