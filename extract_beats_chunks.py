import audioread
import librosa
import numpy as np

def getBeats(audiosrc):
    y, sr = librosa.load(audiosrc)
#    import pdb;pdb.set_trace()
    bl = range(0,len(y),10*sr)
    spl = list(zip(bl[:-1],bl[1:]))
    tempo = []
    beats=[]
    ts = []
    for start, end in spl:
        onset_env = librosa.onset.onset_strength(y=y[start:end], sr=sr, aggregate=np.median)
        temp, beat = librosa.beat.beat_track(y=y[start:end], sr=sr, onset_envelope=onset_env)
 #       tst = librosa.frames_to_time(beat, sr=sr)
        beats.append(beat)
        tempo.append(temp)
        #import pdb;pdb.set_trace()
        tst = librosa.frames_to_time(beats, sr=sr)
        ts.append(tst)
    import pdb;pdb.set_trace()
    return(ts)

