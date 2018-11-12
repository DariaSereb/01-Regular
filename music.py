from numpy import fft
import numpy
import struct
import sys
import wave
from pathlib import Path
from math import log2, pow


def data_from_file(f):

    while True:
        data = f.readframes(1)
        if len(data) < 1:
            return

        if f.getnchannels() == 1:
            yield struct.unpack('<h', data)[0]

        elif f.getnchannels() == 2:
            l, r = struct.unpack('<hh', data)
            yield ((l + r) / 2)
        else:
            print("Error:invalid number of channels: {}".format(f.getnchannels()), file=sys.stderr)
            return


def windows_r(file_name):

    with wave.open(str(file_name)) as f:

        if f.getsampwidth() != 2:
            print("Error:Expected 2, but {} given.".format(f.getsampwidth()))
            exit(-1)

        window = []

        for data in data_from_file(f):
            window.append(data)

            if len(window) == f.getframerate():
                yield window
                del window[:int(f.getframerate()/10)]


def get_peaks(window):
    magnitudes = numpy.abs(fft.rfft(window))
    mag_avg = sum(magnitudes) / len(magnitudes)

    peaks = []
    for f, m in enumerate(magnitudes, start=0):
        if m >= 20 * mag_avg:
            peaks.append((f, m))
    return peaks


def cluster_of_peaks(peaks):

    if not peaks:
        return []

    cluster_peaks = []

    cluster = []
    prev_frequency = None
    for frequency, magnitude in sorted(peaks):
        if not prev_frequency:
            prev_frequency = frequency

        if (frequency - prev_frequency) > 1:
            cluster_peaks.append(max(cluster, key=lambda x_y: x_y[1]))
            cluster = []

        cluster.append((frequency, magnitude))
        prev_frequency = frequency
    cluster_peaks.append(max(cluster, key=lambda x_y: x_y[1]))

    return cluster_peaks

A4 = int(sys.argv[1])
input_file = Path(sys.argv[2])
t_prev = 0
max_3_prev = None
t = None

def hz_to_tone(freq, A4):
    name = ["c", "cis", "d", "es", "e", "f", "fis", "g", "gis", "a", "bes", "b"]

    C0 = A4 * pow(2, -(12*4 + 9)/12)
    steps = round(12 * log2(freq / C0))
    octave = steps // 12


    tone = name[steps % 12]
    if octave < 3:
        tone = tone.title()
        tone += (2 - octave) * ','
    else:
        tone += (octave - 3) * '\''

   
    cents = round(((12 * log2(freq / C0)) % 1) * 100)
    if cents > 50:
        tone += "-{}".format(100 - cents)
    else:
        tone += "+{}".format(cents)

    return tone



for t, window in enumerate(windows_r(input_file), start=0):

    peaks = get_peaks(window)
    peaks = cluster_of_peaks(peaks)
    peaks.sort(key=lambda x: x[1])
    max_3 = list(map(lambda x: x[0], peaks[-3:]))
    max_3.sort()

    if max_3 != max_3_prev:
        if max_3_prev:
            print("{}-{} {}".format(t_prev/10, t/10, " ".join(map(lambda x: hz_to_tone(x, A4), max_3_prev))))
        max_3_prev = max_3
        t_prev = t

if max_3_prev:
   print("{}-{} {}".format(t_prev/10, t/10, " ".join(map(lambda x: hz_to_tone(x, A4), max_3_prev))))
