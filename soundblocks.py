import librosa
import soundfile as sf
import numpy as np
#from librosa.feature import chroma_stft as chroma
from librosa.feature import tempogram as tempft

#create blocks of audio file via soundfile
#create tempogram
def getBlocksSF(audiosrc):
    sbl = sf.blocks(audiosrc, blocksize=22050)
    rate = sf.info(audiosrc).samplerate
    tgram = []
    for bl in sbl:
        y=np.mean(bl, axis=1)
        tgram.append(tempft(y,sr=rate))
    return(sbl,tgram,rate)

#create blocks of audio file via librosa and split/zip
#partly missing functionality
def getBlocksL(audiosrc):
    y,sr = librosa.load(audiosrc)
    bl = range(0,len(y),10*sr)
    spl = list(zip(bl[:-1],bl[1:]))


#create blocks of audio file via soundfile
#take norm value of each block
def getBlocksSFMed(audiosrc):
    bsize = 1024
    ol = 512
    blist = [block for block in
       sf.blocks(audiosrc, blocksize=bsize, overlap=ol)]
    return(blist)

#create blocks and detect beats via librosa
def getBeatsBl(audiosrc):
    y, sr = librosa.load(audiosrc)
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
#    import pdb;pdb.set_trace()
    return(ts)

    ablocks = sf.blocks(src, blocksize=1024)
    srate = sf.info(src).samplerate
    return(ablocks, srate)


#detect beats in audio track
#simple version
def getBeatsSmpl(audiosrc):
    y, sr = librosa.load(audiosrc)
    print(y)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr,trim=True)
    ts = librosa.frames_to_time(beats, sr=sr)
    return(ts)

#detect beats in audio track
#complex version w/ adjusted parameters
def getBeatsCmplx(audiosrc):
    bl, srt = simpleBlocks(audiosrc)
#    import pdb;pdb.set_trace()
    tempo = []
    beats = []
    for ii in bl:
        y, sr = librosa.load(audiosrc,sr=srt)
        y=ii
        sr=srt
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
        temp, beat = librosa.beat.beat_track(y=y, sr=sr, onset_envelope=onset_env)
        beats.append(beat)
        tempo.append(temp)
    ts = librosa.frames_to_time(beats, sr=srt)
    return(ts)

def getBeatsCombinedBPM(audiosrc):
    y, sr = librosa.load(audiosrc)
    temp_120, beats_120 = librosa.beat.beat_track(y=y, sr=sr, bpm=120)
    temp_90, beats_90 = librosa.beat.beat_track(y=y, sr=sr, bpm=90)
    temp_60, beats_60 = librosa.beat.beat_track(y=y, sr=sr, bpm=60)
    ts_120 = librosa.frames_to_time(beats_120, sr=sr)
    ts_90 = librosa.frames_to_time(beats_90, sr=sr)
    ts_60 = librosa.frames_to_time(beats_60, sr=sr)
    return np.concatenate([ts_60, ts_90, ts_120])
    
#detect beats in audio track
#input from soundfile blocks
def getBeatsSmplBlocks2(audiosrc):
    bl = getBlocksSFMed(audiosrc) #1d array
    sr = len(bl)
    
#    tempo, beats = librosa.beat.beat_track(y=bl, sr=sr)
    beats=[]
    tempo=[]
    for ii in bl:
        ii = librosa.to_mono(np.array(ii))
        temp, beat = librosa.beat.beat_track(y=ii, sr=sr)
        beats.append(beat)
        tempo.append(temp)
    ts = librosa.frames_to_time(beats, sr=sr)
    return(ts)


#detect beats in audio track
#input from soundfile
#conversion to mono channel
def getBeatsSmplBlocks(audiosrc):
    bl,tgr,sr = getBlocksSF(audiosrc)
#    sr=22050
    beats=[]
    tempo=[]
    for ii in bl:
        y = librosa.to_mono(ii)
        oe = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
        temp, beat = librosa.beat.beat_track(y=y, sr=sr,onset_envelope=oe, hop_length=len(ii)/40)
        beats.append(beat)
        tempo.append(temp)
    ts = librosa.frames_to_time(beats, sr=sr)
    return(ts)

#detect beats in audio track
#input from librosa blocks
def getBeatsMed(audiosrc):
    y, sr = librosa.load(audiosrc)
    msrc = librosa.core.to_mono(y=y)


    return(ts)

def getBeatsPS(audiosrc,tn):
    y, sr = librosa.load(audiosrc)
    aggfun = lambda x,**kw: np.max(x[(x > 8) &( x < 120)],**kw)
    oe = librosa.onset.onset_strength(y=y, sr=sr, aggregate=aggfun)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr,tightness=tn)
    #trim=True?
    ts = librosa.frames_to_time(beats, sr=sr)
    return(ts)

def getBeatsPrcssv(audiosrc):
    y, sr = librosa.load(audiosrc)
    D = librosa.stft(y)
    D_harm, D_perc = librosa.decompose.hpss(D)
    print(y)
    tempo, beats = librosa.beat.beat_track(y=D_perc, sr=sr,trim=True)
    ts = librosa.frames_to_time(beats, sr=sr)
    return(ts)

#main testing
if __name__ == '__main__':
    src = '/home/mina/projects/audiogame/src/inex_suender.ogg'
#    blt100 = getBeatsPS(src,100)
    blt = getBeatsPrcssv(src)
    print(blt[60:150])

