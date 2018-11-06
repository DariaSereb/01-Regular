from numpy import fft, abs
import struct
import sys
import wave



def data_from_file(parameter, current_frame):
	fr = struct.unpack(parameter*'h', current_frame)
	if parameter == 2:
		return float((fr[0] + fr[1]) / 2)
	else:
		return float(fr[0])


def data_read(filename, channels_num):
	current_frame = filename.readframes(1)
	data_unpacked = []
	while current_frame:
		unpacked = data_from_file(channels_num, current_frame)
		data_unpacked.append(unpacked)
		current_frame = filename.readframes(1)
	return data_unpacked

def peaks_get(peaks):
	if len(peaks) != 0:
		return min(peaks), max(peaks)
	return None, None


def fourier_get(data, window, position):
	pos_from = position * window
	pos_to = (position + 1) * window
	data_to_transform = data[pos_from:pos_to]

	return fft.rfft(data_to_transform)


def main():

	f = wave.open(sys.argv[1], "rb")

	channels = f.getnchannels()
	data = data_read(f, channels)
	frames_num = f.getnframes()
	window = f.getframerate()

	Min_peaks = None
	Max_peaks = None

	for i in range(frames_num // window):
		transform = fourier_get(data, window, i)

		amplitudes = []
		for item in transform:
			amplitudes.append(abs(item))

		avg_amplitude = sum(amplitudes) / len(amplitudes)

		peaks = []

		for j, amplitude in enumerate(amplitudes):
			if amplitude >= 20 * avg_amplitude:
				peaks.append(j)

		current_peaks = peaks_get(peaks)

		if Max_peaks is None or Max_peaks < current_peaks[1]:
			Max_peaks = current_peaks[1]

		if Min_peaks is None or Min_peaks > current_peaks[0]:
			Min_peaks = current_peaks[0]



	if Min_peaks is not None and Max_peaks is not None:
		print("low = " + str(Min_peaks) + ", high = " + str(Max_peaks))
	else:
		print("no peaks")


main()
