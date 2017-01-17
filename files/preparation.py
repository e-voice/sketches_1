''' numpy - типов данных
    pandas - чтения csv 
    wave - чтение wave файла
    os - проверка существования пути файла
'''

print('Process has been started, please wait...')

import numpy as np
import pandas as pd
import wave
import os


# Типы данных амплитуд
types = {
    1: np.int8,
    2: np.int16,
    4: np.int32,
}


# Открытие файла на разбор
def wave_open(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        wavf =  wave.open(filepath, mode='r')
        return wavf

''' Путь к файлу '''
wav = wave_open("/Users/nikita/Documents/python_3_filies/ML/ML_sound_1/Eee_1.wav")

# Различные вкусности из wave-файла
''' Кол-во каналов '''
def nchannals():
    nchannals_var = wav.getnchannels()
    return nchannals_var

''' Длина семпла (int8, int16, int32) '''
def sampwidth():
    sampwidth_var = wav.getsampwidth()
    return  sampwidth_var

''' Частота окон '''
def framerate():
    framerate_var = wav.getframerate()
    return framerate_var

''' Кол-во окон '''
def nframes():
    nframes_var = wav.getnframes()
    return  nframes_var

''' Тип сжатия '''
def comptype():
    comptype_var = wav.getcomptype()
    return comptype_var

''' Название сжатия '''
def compname():
    compname_var = wav.getcompname()
    return compname_var

''' Длительность записи '''
def duration():
    duration_var = nframes()/framerate()
    return duration_var

# Значения амплитуд в 10-ричной системе счисления
def channel_data():
    byte_content = wav.readframes(nframes())
    samples = np.fromstring(byte_content, dtype=types[sampwidth()])
    #for n in range(nchannals()):
    channel = samples
    return channel

# ---------------- Перевод в биты и логарифмирование

''' Битовые данные'''
byte_content = wav.readframes(nframes())

''' Представление битов в int8(16,32) '''
samples = np.fromstring(byte_content, dtype=types[sampwidth()])

''' Образка первых 1000 семплов, т.к. там ненужный шум, позже можно будет убрать '''
samples = samples[1000:]
#samples = samples[131000:132000]

''' Логарифмирование семплов + минимальное значение int16 (т.к. запись была в int16), ибо логарифм не может иметь отрицательный аргумент '''
samples_log = np.log(samples+32768)
#len(samples)

# ---------------- Фурье

''' Преобразование Фурье из прологарифмированных семплов '''
samples_fourier = np.fft.fft(samples_log)

# ---------------- Получение фурье-семплов

''' Массив из Фурье-преобразований семплов(далее, фурье-семпл), один семпл - по 1000 бит значений '''
fourier_samples = []
begin = 0
step = 1000
end = step

''' Значение для хранения временного семпла '''
tmp_sample = samples[begin:end] 

''' Добавление первого фурье-семпла  '''
fourier_samples.append(np.fft.fft(np.log(tmp_sample+32768)).real) 

''' Проход по массиву семплов и получение фурье-семплов '''
while end < len(samples):
    abs_sample = [abs(i) for i in tmp_sample]
    ''' Проверка на тишину (будем считать тишиной абсолютную сумму семпла меньшую 50000) '''
    if sum(abs_sample) > 50000: 
        tmp_sample = np.log(tmp_sample+32768) # ''' Временный лог-семпл '''
        tmp_fourier = np.fft.fft(tmp_sample).real # ''' Временный фурье-семпл '''
        fourier_samples.append(tmp_fourier)
        begin += step
        end += step
        tmp_sample = samples[begin:end] 
        #print(end,sum(tmp_sample),sum(abs_sample))
    else:
        #print(end,sum(abs_sample),'-')
        begin += step
        end += step
        tmp_sample = samples[begin:end]

# ---------------- Data       
''' Формирование датасета '''
answer = pd.DataFrame(fourier_samples)

''' Запись датасета в csv файл '''
answer.to_csv('/Users/nikita/Documents/python_3_filies/ML/ML_sound_1/fourier_Eee_1_1.csv', index=False)
print('Process has been finished')
