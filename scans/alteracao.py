# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 00:12:19 2023

@author: Brenda
"""

import os

path = '.'


def transformar(caminho):
   for filename in os.listdir(caminho):
        if (filename[1]== '_' ):
            x= 'arq'+ filename[0] + '.pcap'
        else : 
            x = 'arq'+ filename[0] + filename[1] + '.pcap'
    
        os.rename(os.path.join(caminho, filename), os.path.join(caminho, x))
        
       


for filename in os.listdir(path):
    
    if filename == 'alteracao.py':
        continue
    caminho = os.path.join(path,filename)
    transformar(caminho)
