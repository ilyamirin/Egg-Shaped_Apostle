import os
from pydub import AudioSegment
import audiosegment

main_dir = '/home/user/Desktop/projects/Egg-Shaped_Apostle/data/RTKcalls/Calls/'
dirs = os.listdir(main_dir)
for dir in dirs:
    files = [i for i in os.listdir(main_dir+dir) if i.endswith('.mp3')]
    for file in files:
        try:
            sound = AudioSegment.from_mp3(main_dir+dir+'/'+file)
            sound.export(main_dir+dir+'/'+'converted/'+file, format="wav")
            #sound = audiosegment.from_file(main_dir+dir+'/'+'converted/'+file).resample(sample_rate_Hz=8000, sample_width=2, channels=1)
            #sound.export(main_dir+dir+'/'+'converted/'+file, format="wav")
        except:
            continue


