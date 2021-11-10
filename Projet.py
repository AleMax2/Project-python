# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 16:21:53 2021

@author: alepi
"""
import geopandas as gpd
import numpy as np
import pandas as pd
import os
os.chdir('D:\\Universita\\STatistica\\TIDE\\Python\\Projet')
pd.set_option("display.max_rows", 16)
dati=pd.read_excel("Data/base-cc-emploi-pop-active-2018.xlsx", sheet_name="ARM_2018",
                   index_col=None, header=5)
dati
dati.info()

Paris=dati.loc[dati['REG']==11]
# Le taux d'activité 
# 15-64
Paris['TACT1564']= 100*Paris['P18_ACT1564'] / Paris['P18_POP1564']
# Tous 15 ou plus
Paris['TACT15OP']= 100*Paris['P18_ACT15P'] / Paris['P18_POP15P']

# Le taux d'emploi 
# Tous 15-64
Paris['TEMPL1564']= 100*Paris['P18_ACTOCC1564'] / Paris['P18_POP1564']
# Femmes 55-64
Paris['TEMPL1564']= 100*Paris['P18_FACTOCC5564'] / Paris['P18_F5564']

# Le taux de chomage 
# Tous 15-64
Paris['TCHOM1564']= 100*Paris['P18_CHOM1564'] / Paris['P18_ACT1564']

# Concentration d'emploi
Paris['TCONC1564']= 100*Paris['P18_EMPLT'] / Paris['P18_ACTOCC']

# Part d'ouvriers dans l'emploi
Paris['POUVR']= 100*Paris['C18_EMPLT_CS6'] / Paris['C18_EMPLT']

# Taux de féminisation des emplois salariés de l'agriculture
Paris['TFSAGR']= 100*Paris['C18_AGRILT_FSAL'] / Paris['C18_AGRILT_SAL']

# Taux de féminisation des emplois non-salariés de l'agriculture
Paris['TFNONSAGR']= 100*Paris['C18_AGRILT_FNSAL'] / Paris['C18_AGRILT_NSAL']

fp = "D:/Universita/STatistica/TIDE/Python/Projet/arrondissements/arrondissements.shp"
map_df = gpd.read_file(fp)
map_df.head()
map_df.plot()

# CLeaning the dataset
Paris = Paris[['CODGEO','TACT1564', 'TEMPL1564','TCHOM1564']]
map_df= map_df.rename(index=str, columns={"c_arinsee":"CODGEO"})
merged = map_df.set_index('CODGEO').join(Paris.set_index('CODGEO'))
merged.head()

#Let's do the map
import matplotlib.pyplot as plt

variable = 'TCHOM1564'
plt.figure(figsize=(16,9))
merged.plot(column=variable, cmap='Reds', linewidth=0.8, edgecolor='0.8')

vmin, vmax = 8, 16
# Create colorbar as a legend
fig, ax = plt.subplots(1, figsize=(16, 9))
sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=vmin, vmax=vmax))
# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = fig.colorbar(sm)
plt.figure(figsize=(16,9))
merged.plot(column=variable, cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')
ax.axis('off')
plt.show()

 #os.getcwd()

#open('Data/base-cc-emploi-pop-active-2018.xlsx')