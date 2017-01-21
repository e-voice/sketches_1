import pyaudio
import wave

''' Параметры wave файла '''
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3

''' Путь к файлу '''

rootpath = "/Users/nikita/Documents/python_3_filies/ML/ML_sound_1/audio/"
filename = "Eee_test_1.wav"
WAVE_OUTPUT_FILENAME = rootpath + filename

''' Класс подключения к портам аудио '''
p = pyaudio.PyAudio()

''' Инициализация открытия с параметрами '''
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

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
