import os
import pandas as pd
import pickle

def verificar(objeto):
    if str(type(objeto)).find("Series") != -1:
        return False
    else:
        return True
    

def batimentos(scan, bpm):
    
    global relogio

    bpm = pd.Series(bpm)

    if verificar(relogio.get(scan)): # caso não tenha o scan
        relogio[scan] = bpm
    else:
        x = relogio.get(scan)
        relogio[scan] = pd.concat([x,bpm], ignore_index = True)


def batidas(file, caminho): # retorna o bpm no relogio

    file = caminho + "\\"+ file + ".json"
    print()

    try:
        samples = pd.read_json(file)
    except FileNotFoundError:
        print(f'File {file} not found.')
        exit(-1)
    

    return samples["heart_rate"].mean()

def transformar(caminho):
   for file in os.listdir(caminho):
        final = file[-5:]

        if final.find(".png") != -1:
            os.remove(os.path.join(caminho, file))
            continue
        else:
            if (file[1]== '_' ) and final.find(".json")!=-1:
                x= 'arq'+ file[0] + '.json'
            else : 
                x = 'arq'+ file[0] + file[1] + '.json'
            
            print(x)
        
        if x.find("arq20")!=-1:
            continue
    
        os.rename(os.path.join(caminho, file), os.path.join(caminho, x))




path = "heartRateData" # caminho dos scans

scans = os.listdir(path)

relogio = {}


quantidade = 0

for filename in scans: # roda os scans
    caminho = os.path.join(path,filename)
    sequence = 1
    quantidade+=1

    #transformar(caminho)

    while sequence <18:
        file = 'arq' + str(sequence)
        
        if sequence<18:
            bpm = batidas(file, caminho)
            print("##########  BPM   "+ file + "  " + filename + "  "+str(bpm)+ "###################")
            batimentos(filename, bpm)
        else:
            sequence += 1
            continue
        sequence += 1
        print('Processados :', quantidade)

tab = pd.DataFrame(relogio)
print(tab)
tab.to_csv("relogio.csv")
tab.to_excel("tabela_relogio.xlsx")

with open ("tabela_1_1config.pkl", mode ='wb') as f:
        pickle.dump([tab], f)       


print("########## CSI EXPLORER Ends ##########")
comando = input('Type anything to close: ')
os._exit(1)