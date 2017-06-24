#!/usr/bin/python

import sys, os, time
from socket import *
from pocketsphinx import get_model_path
from pocketsphinx.pocketsphinx import *
import pyaudio, Parser as p

modeldir = get_model_path()
socket = socket(AF_INET, SOCK_STREAM) #cria um socket

host = 'localhost'
port = 8421
vel_linear = 0.1
vel_angular = 0.7
broke = False

files = p.ConfigSectionMap('Files') #dicionario com nome do ficheiro e path. Ex: {dictionary: path,kws:path}
commands = p.ConfigSectionMap('Commands') #dicionario com comandos para mover o objeto e a mensagem a enviar ao servidor. Ex: {move forward: 0.1 0}

def parseVoice(frase):
    print frase
    if frase == 'STOP LISTENING':
        return -1
    elif frase in commands.keys():
        socket.sendall(''.join([commands[frase],'\n']).encode())
    return 1


# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', os.path.join(modeldir, 'en-us'))
config.set_string('-dict', files['Dictionary'])
config.set_string('-kws', files['Kws'])
config.set_string('-logfn',files['Logfn'])
#config.set_float('-kws_threshold', 1e+20)


#ligar microfone
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

socket.connect((host,port))

print 'A enviar talker ...'
time.sleep(1)
socket.send('talker\n'.decode())
print 'Enviou talker'

# Process audio chunk by chunk. On keyphrase detected perform action and restart search
decoder = Decoder(config)
decoder.start_utt()
print 'Listening...'
while True:
    buf = stream.read(1024)
    if buf:
         decoder.process_raw(buf, False, False)
    else:
         break
    if decoder.hyp() != None:
        for seg in decoder.seg():
            if parseVoice(seg.word) == -1:
                socket.close()
                broke = True
                break
            data = socket.recv(1024).decode()
            print data,
        if broke:
            break
        decoder.end_utt()
        decoder.start_utt()