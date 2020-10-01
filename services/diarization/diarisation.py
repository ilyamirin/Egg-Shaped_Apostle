from pyannote.audio.features import Pretrained
from pyannote.audio.pipeline import SpeakerDiarization

validate_dir='./vad_ami_sber/train/SBERBANK'\
             '.SpeakerDiarization.SberCorpus.train'\
             '/validate_detection_fscore/SBERBANK'\
             '.SpeakerDiarization.SberCorpus.development'
diarization = SpeakerDiarization(sad_scores=Pretrained(validate_dir=validate_dir),
                                  scd_scores='scd_ami',
                                  embedding='emb_voxceleb',
                                  metric='cosine',
                                  method='affinity_propagation')

diarization.load_params('./dia_sber/train/SBERBANK.SpeakerDiarization.SberCorpus.development/params.yml')

diarization.initialize()


def diarize(filename):
    return diarization({'audio': filename}).for_json()

