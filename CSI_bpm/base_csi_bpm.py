import config
from analysis.dataAnalysis import analyze
import decoders.interleaved as decoder
import os
import dataset.coleta as dataset
import pandas as pd
import pickle

def verificar(objeto):
    if str(type(objeto)).find("Series") != -1:
        return False
    else:
        return True
    
def batimentos(scan, bpm):
    
    global tabela

    bpm = pd.Series(bpm)

    if verificar(tabela.get(scan)): # caso não tenha o scan
        tabela[scan] = bpm
    else:
        x = tabela.get(scan)
        tabela[scan] = pd.concat([x,bpm], ignore_index = True)


if __name__ == "__main__":

    tabela = {}

    print("########## CSI EXPLORER Begins ##########")

    path = "..\scans" # caminho dos scans

    scans = os.listdir(path)

    quantidade = 0

    for filename in scans: 
        caminho = os.path.join(path,filename)
        sequence = 1
        quantidade +=1

        while sequence <18 and quantidade <118 :
            file = 'arq' + str(sequence)
            file_exists = dataset.check_next_file(file)

            print('Processados :', quantidade)
            
            if file_exists:
                bpm = dataset.process_pcap_file(file, caminho)
                print("##########  BPM   "+ file + "  " + filename + "  "+str(bpm)+ "###################")
                batimentos(filename, bpm)
            else:
                break
            sequence += 1
    
    tab = pd.DataFrame(tabela)
    print(tab)

    tab.to_excel("tab.xlsx")


    with open ("tabela_config.pkl", mode ='wb') as f:
        pickle.dump([tab], f)       


    print("########## CSI EXPLORER Ends ##########")
    comando = input('Type anything to close: ')
    os._exit(1)