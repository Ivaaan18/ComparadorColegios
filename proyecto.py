import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pandas as pd

from bs4 import BeautifulSoup

import os
from os import remove

import shutil

from csv import reader

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

print('Bienvenido al comparador de centros de la Comunidad de Madrid\n')

elif bandera == 1 or bandera == 0:
# funcion 4
# if respuesta == 'N':
respuesta1 = ''
Codigos = []

while respuesta1 != 'S' and respuesta1 != 'N':
    respuesta1 = input('¿Te gustaria comparar solo unos pocos centros? S o N ')
    respuesta1 = respuesta1.upper()
    if respuesta1 != 'S' and respuesta1 != 'N':
        print('¡¡ERROR!!: Escriba S o N')
if respuesta1 == 'S':

    Control1 = 0
    while Control1 != 1:
        numColes = int(input("¿Cuantos colegios vamos a comparar? (2-10) "))
        if numColes > 1 and numColes <= 10:
            Control1 = 1
        else:
            print("Porfavor introduzca un número de colegios dentro del intervalo del 2 al 10")
            # cambiar .csv
    df = pd.read_csv('datos_colegios.csv', sep=';', engine='python')

    for key, value in df.iteritems():
        if key == "COD Centro":
            for new in value:
                new = [new]
                Codigos.append(new)
    i = 0

    for key, value in df.iteritems():
        if key == "Nombre Centro":
            for centro in value:
                Codigos[i].append(centro)
                i += 1
    Coles = []

    for i in range(numColes):
        Control2 = 0
        Control3 = 0
        while Control2 != 1 or Control3 != 1:
            Control2 = 0  # que exista el codigo
            Control3 = 0  # de que no se repita
            # Posicion 0
            pedirCole = input("\nIntroduzca el codigo de colegio " + str((i + 1)) + str(": ")) + '.0'
            if i == 0:
                for x in Codigos:
                    for z in x:
                        if pedirCole == str(z):
                            Control2 = 1
                            Control3 = 1
                if Control2 != 1 or Control3 != 1:
                    print("Codigo de colegio inexistente")
                else:
                    Coles.append(pedirCole)

            # resto de posiciones en la lista
            else:
                # iterar lista si existe
                for x in Codigos:
                    for z in x:
                        if pedirCole == str(z):
                            Control2 = 1

                # iterar lista no se repita
                for x in Coles:
                    if pedirCole != x:
                        Control3 = 1
                    else:
                        Control3 = 0
                        break
                if Control2 != 1 or Control3 != 1:
                    print("Codigo de colegio inexistente o repetido")
                else:
                    Coles.append(pedirCole)

    df.set_index('COD Centro', inplace=True)

    for i in range(len(Coles)):
        Coles[i] = round(float(Coles[i]), 1)
    df3 = df.loc[Coles[:numColes]]
    df3.to_csv('colegios.csv', sep=';')

    lista1 = []
    lista2 = []
    lista3 = []

    for i in range(numColes):
        lista1.append([])
        lista2.append([])
        lista3.append([])

    c1 = 0
    c = 0

    for i, x in df3.iteritems():
        c = 0
        if i == 'Nombre Centro':
            for o in x:
                lista1[c].append(o)
                c += 1
        if 'Titulacion' in i:
            for r in x:
                lista2[c].append(r)
                c += 1
        if 'Evau' in i:
            for r in x:
                lista3[c].append(r)
                c += 1
        lista1 = []
        lista2 = []
        lista3 = []

        for i in range(numColes):
            lista1.append([])
            lista2.append([])
            lista3.append([])

        c1 = 0
        c = 0

        for i, x in df3.iteritems():
            c = 0
            if i == 'Nombre Centro':
                for o in x:
                    lista1[c].append(o)
                    c += 1
            if 'Titulacion' in i:
                for r in x:
                    lista2[c].append(r)
                    c += 1
            if 'Evau' in i:
                for r in x:
                    lista3[c].append(r)
                    c += 1
        index = ['Ev 13/14', 'Ev 14/15', 'Ev 15/16', 'Ev 16/17', 'Ev 17/18']
        index2 = ['Ti 13/14', 'Ti 14/15', 'Ti 15/16', 'Ti 16/17', 'Ti 17/18']
        diccionario = {}
        diccionario2 = {}

        for i in range(numColes):
            diccionario[lista1[i][0]] = lista3[i]
            diccionario2[lista1[i][0]] = lista2[i]

    df8 = pd.DataFrame(diccionario, index=index)
    df9 = pd.DataFrame(diccionario2, index=index2)

    ax = df8.plot.bar(rot=0)
    plt.yticks(np.arange(0, 11, 1))
    ax.set_title('Evau')
    ay = df9.plot.bar(rot=0)
    ay.set_title('Titulación')
    ay.set_ylim([0, 100])
    plt.show()