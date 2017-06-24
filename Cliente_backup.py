#!/usr/bin/env python

import os, time
from socket import *
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()
socket = socket(AF_INET, SOCK_STREAM) #cria um socket

host = '10.42.0.1'
port = 8421
vel_linear = 0.25
vel_angular = 1.5


speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    lm=False,
    hmm= os.path.join(model_path,'en-us'),
    #lm= '/home/paulo/PycharmProjects/VoiceRecognition/Data/TAR4858/4858.lm',
    dict = #'/home/vitor/Documentos/Univ/3_Ano/2_Semestre/Projeto/Projeto/VoiceRecognition/Data/Robot/Robot.dic',
	'/home/paulo/PycharmProjects/VoiceRecognition/Data/Robot/Robot.dic',
    kws = #'/home/vitor/Documentos/Univ/3_Ano/2_Semestre/Projeto/Projeto/VoiceRecognition/Data/Robot/Robot_Keyphrase.list'
          '/home/paulo/PycharmProjects/VoiceRecognition/Data/Robot/Robot_Keyphrase.list'
)

def parseVoice(frase):

    if frase == 'MOVE FORWARD ':
        valores = ' '.join([str(vel_linear),str(0)])
        socket.sendall(''.join([valores,'\n']).encode())
    elif frase == 'ROTATE LEFT ':
        valores = ' '.join([str(0),str(-vel_angular)])
        socket.sendall(''.join([valores, '\n']).encode())
    elif frase == 'ROTATE RIGHT ':
        valores = ' '.join([str(0),str(vel_angular)])
        socket.sendall(''.join([valores, '\n']).encode())
    elif frase == 'STOP MOVING ':
        socket.sendall('0 0\n'.encode())
    elif frase == 'STOP LISTENING ':
        return -1
    return 1

socket.connect(('localhost',port))

print 'A enviar talker ...'
time.sleep(1)
socket.send('talker\n'.decode())
print 'Enviou talker'

print 'Listening...'
for phrase in speech:
    frase = str(phrase)
    if parseVoice(frase) == -1:
        socket.close()
        break
    data = socket.recv(1024).decode()
    print data,
    print 'Listening...'


