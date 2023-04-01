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

    return csi_data
    
    

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

