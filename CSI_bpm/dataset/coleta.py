import config
from analysis.dataAnalysis import analyze
import decoders.interleaved as decoder
from plotters.AmpPhaPlotter import Plotter
import os
import time
from CSIKit.reader import get_reader
from CSIKit.util import csitools
import datetime
import pandas as pd

def tempo_segundos(pcap):

    time = csikit(pcap)
    data = []
    for x in time:
        hm = datetime.fromtimestamp(x)
        obj = pd.to_datetime(hm)
        data.append(obj)
        
    return data


def csikit(pcap):
    my_reader = get_reader(pcap)
    csi_data = my_reader.read_file(pcap, scaled=True)

    return csi_data.timestamps


def add_time(pcap, dados_csi):
    
    dados_csi.insert(loc=0, column='tempo', value = tempo_segundos(pcap))

    return dados_csi






def process_pcap_file(pcap_filename, caminho):

   
    if '.pcap' not in pcap_filename:
        pcap_filename += '.pcap'
    pcap_filepath = '/'.join([caminho, pcap_filename])    
    try:
        samples = decoder.read_pcap(pcap_filepath)
    except FileNotFoundError:
        print(f'File {pcap_filepath} not found.')
        exit(-1)

    csi_data = samples.get_pd_csi()

    csi_data = add_time(pcap_filepath, csi_data)

    return analyze(csi_data)
    
    

    #function to check if next file exists. Wait until 15 seconds
def check_next_file(file_name):
    limit = 0
    while(limit <= 150):
        try:
            with open('./pcapfiles/' + file_name + '.pcap', 'r') as f:
                limit = 0
                return True
        except IOError:
            print("Waiting 0.25 seconds to receive next file")
            time.sleep(0.25)
            limit += 1
    print(limit)
    print("Timeout")
    return False

