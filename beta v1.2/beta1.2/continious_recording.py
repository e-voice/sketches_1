import pyaudio
import wave

def Record(number):
    ''' Параметры wave файла '''
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 1

    ''' Путь к файлу '''

    rootpath = "/Users/nikita/Documents/python_3_filies/ML/ML_sound_1/audio/"
    filename = "output_looptest_" + str(number) + ".wav"
    WAVE_OUTPUT_FILENAME = rootpath + filename

    ''' Класс подключения к портам аудио '''
    p = pyaudio.PyAudio()

    ''' Инициализация открытия с параметрами '''
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording ",number)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording ", number)

    ''' Завершение записи '''
    stream.stop_stream()
    stream.close()
    p.terminate()

    ''' Запись в файл '''
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def ContiniousRecord():
    #times = 3
    #for time in range(times):
        #Record(time)
    number = 0
    while True:
        Record(number)
        number += 1


#ContiniousRecord()

def loop(keypressed):
    keypressed = keypressed
    number = 0
    if keypressed == 's':
        Record(number)
        number += 1


from tkinter import *

root = Tk()

def key(event):
    print ("pressed", repr(event.char))
    loop(event.char)

def callback(event):
    frame.focus_set()
    print ("clicked at", event.x, event.y)

frame = Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()
