import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.fftpack import fft
from scipy.signal import butter, lfilter
from hampel import hampel
from sklearn.decomposition import PCA
from scipy.fft import fft, fftfreq
#from interfaceHeartRate import InterfaceHeartRate
from time import time
from datetime import datetime;
from pytz import timezone

def iq_samples_abs(series):
	abs_series = {}
	for key in series.keys():
		for i in range(len(series[key])):
			valor = np.abs(series[key][i])
			if valor == 0:
				valor = -1 * 100
			else:
				valor = 20 * np.log10(valor)
			if key in abs_series:
				abs_series[key] = np.append(abs_series[key], valor)
			else:
				abs_series[key] = np.array(valor)

	abs_series = pd.DataFrame(abs_series)

	return abs_series
 
  
def hampel_filter(series):
	filtered = {}
	for key in series.keys():
		filtered[key] = hampel(series[key], window_size=31, n=3, imputation=True)
	filtered = pd.DataFrame(filtered)
	return filtered

def moving_avg_filter(series):
	moving_avg = {}

	for key in series.keys():                 #window=10 ###############################################################
		moving_avg[key] = series[key].rolling(window=10, min_periods=1, center=True).mean()

	moving_avg = pd.DataFrame(moving_avg)
	return moving_avg

def band_pass_filter(series):
	fs = 43.47
	t = 1.0 / fs
	#lowcut = 0.6
	#highcut = 3.67
	lowcut = 1
	highcut = 2.5
	n = len(series)
	b, a = butter(5, [lowcut / (fs / 2), highcut / (fs / 2)], 'band', analog=False, output='ba')

	bandpass_samples_filter = {}
	for key in series.keys():
		bandpass_samples_filter[key] = lfilter(b, a, series[key])

	bandpass_samples_filter = pd.DataFrame(bandpass_samples_filter)

	return bandpass_samples_filter

def csi_pca(series):
	series = series.reset_index()
	for subcarrier in series.keys():
		for sample in range(len(series[subcarrier])):
			if np.isnan(series[subcarrier][sample]) or np.isinf(series[subcarrier][sample]):
				series[subcarrier][sample] = 0

	pca = PCA(n_components=1)
	principal_components = pca.fit_transform(series)

	principal_components = pd.DataFrame(data=principal_components, columns=['PCA'])


	return principal_components
	
def heart_beat(n, xf, yf):
	frequencias = []
	amplitudes = []
	i = 0 
	sizeXf = len(xf)	

	for i in range(sizeXf):
		if xf[i] > 1 and xf[i] < 2.5:
		#if xf[i] > 0.6 and xf[i] < 3.67:
			frequencias.append(xf[i])
			amplitudes.append(np.abs(yf[i]))	
	amplitudes, frequencias = zip(*sorted(zip(amplitudes, frequencias)))

	j = len(frequencias) - 1
	frequenciasMax = []
	amplitudesMax = []

	for i in range(n):
		frequenciasMax.append(frequencias[j])
		amplitudesMax.append(amplitudes[j])	
		j-=1
	frequenciasMax, amplitudesMax = zip(*sorted(zip(frequenciasMax, amplitudesMax)))
	
	mediaFrequencia = sum(frequenciasMax) / n
	bpm = round(mediaFrequencia * 60) 
	#InterfaceHeartRate.show_heart_rate(bpm)
	timestamp = time()
	dt = datetime.fromtimestamp(timestamp, tz = timezone("America/Sao_Paulo"))
	timestamp_bpm = dt.strftime("%d/%m/%Y %H:%M:%S")

	arqSaida = open("batimentos.txt","a+") 
	arqSaida.write(str(bpm) + ' ' + str(timestamp_bpm) + '\n')
	arqSaida.close()
	return bpm
		  

def csi_fft(series):
	yf = fft(series)
	xf = fftfreq(yf.size, 0.023)
	#fig, ax = plt.subplots()
	#plt.plot(xf, np.abs(yf))
	#ax.set(xlabel='Frequencies (Hz)', ylabel='dB', title='FFT')
	#plt.xlim(0, 4)
	#plt.show()
                  #anteriormente 4
	return heart_beat(4, xf, yf)
	
	
def plot(series, title):
	f, ax = plt.subplots()
	plt.plot(series)
	ax.set(xlabel='Samples', ylabel='dB', title=title)
	plt.show()


def analyze(csi):
	series_abs = iq_samples_abs(csi)

	#series = hampel_filter(csi)  -----> Tirei esse filtro porque estava fazendo ficar lento
	
	series = moving_avg_filter(csi)

	series = moving_avg_filter(series)

	series = band_pass_filter(series)
	

	series = csi_pca(series)

	x = series['PCA'].to_numpy()
	bpm = csi_fft(x)
	return bpm
