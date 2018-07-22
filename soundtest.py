import time, sys
import pygame

src = #add path to sound file

# pygame.init()
#pygame.mixer.init()
#pygame.mixer.music.load(src)
#pygame.mixer.music.set_volume(1.0)
#time.sleep(5)
#channel1 = pygame.mixer.music.play()
                
#sound = pygame.mixer.Sound(sys.argv[1])
#sound.play()

#running = True

#while running:
#        channel1

#from soundblocks import getBlocksSF as getbl
#blk = getbl(src)
#print(blk)
#print(sr)

from soundblocks import getBeatsSmplBlocks as getbeats
#bl,srt = getbeats(src)
blt = getbeats(src)
print(blt)
#import pandas as pd
#blout =pd.DataFrame.from_records(bl)
#blout.head()

#from soundblocks import getBeatsMed as gbmed
#bts = gbmed(src)
#print(bts)
