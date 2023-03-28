import pandas as pd
import pickle
import numpy as np

def media(obj): # calcula a média dos valores #

    aux = pd.Series()

    for i in obj.index:
        soma = 0
        for j in obj.columns:
            soma += obj.loc[[i]][j]
             
        
        avg = soma/len(obj.columns)

        aux = pd.concat([aux, avg])

    return aux


with open ("variaveis.pkl", mode ='rb') as f:
        relogio, par1 , par2, par3, par4, par5, par6, par7 = pickle.load(f)

par_1 = media(par1)