#!/usr/bin/env python

import os
from pocketsphinx import LiveSpeech, get_model_path

i = 0
j = 0
frase = ''
tab = [['x','o','o'],['o','o','o'],['o','o','o']]

def move():
    global i,j,frase

    if 'BACKWARD' in frase and i!= 2:
        i=i+1
    if 'FORWARD' in frase and i!= 0:
        i=i-1
    if 'LEFT' in frase and j != 0:
        j = j - 1
    if 'RIGHT' in frase and j != 2:
        j = j + 1

def draw():
    global i,j
    s = 0
    for l in range(3):
        for c in range(3):
            if tab[l][c] == 'x':
                tab[l][c] = 'o'
                s = 1
                break
        if s == 1:
            break
    tab[i][j] = 'x'
    for p in tab:
        print p


model_path = get_model_path()



speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    #lm=False,
    hmm= os.path.join(model_path,'en-us'),
    dic= os.path.join(model_path,'en-us.lm.bin'),
    lm= os.path.join(model_path,'cmudict-en-us.dict')
)



for p in tab:
    print p

for phrase in speech:
    print phrase.probability()
    frase = str(phrase)
    print frase
    move()
    draw()
