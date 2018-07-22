import audioread
import librosa

def getBeats(audiosrc):
    y, sr = librosa.load(audiosrc)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    ts = librosa.frames_to_time(beats, sr=sr)
    return(ts)

