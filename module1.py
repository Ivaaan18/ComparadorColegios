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
def csv1():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.maximize_window()
    driver.get('https://gestiona3.madrid.org/wpad_pub/run/j/MostrarConsultaGeneral.icm')

    B_A = driver.find_element_by_xpath('//*[@id="irBuscador"]/img')
    click_B_A = B_A.click()
    time.sleep(1)

    BA = driver.find_element_by_xpath('//*[@id="comboTipoEnsenanza"]/option[6]')
    click_BA = BA.click()
    time.sleep(1)

    finalizar = driver.find_element_by_xpath('//*[@id="btnConsultarCritBusq"]/span')
    click_finalizar = finalizar.click()
    time.sleep(1)

    descargar = driver.find_element_by_xpath('//*[@id="btnDescargarListado"]/span')
    click_descargar = descargar.click()
    time.sleep(5)

    driver.quit()

def listado2():
    a = os.getcwd() + os.sep
    a = a.split('\\')

    draiz = a[0] + '\\'
    dusers = draiz + a[1] + '\\'
    duser = dusers + a[2] + '\\'
    ddesktop = duser + a[3] + '\\'

    ddescargas = duser + 'Downloads\\'
    dp = a[4] + '\\' + a[5] + '\\'
    dproyecto = ddesktop + dp

    os.chdir(ddescargas)#nos situamos en el directorio descargas
    contenidos = os.listdir(ddescargas) #listamos el directorio descargas
    csv = []

    for contenido in contenidos:
        if os.path.isfile(os.path.join(ddescargas, contenido)) and contenido.endswith('.csv'):
            csv.append(contenido)

    csv_py = csv[0] #elegimos el csv que hemos acabado de descargar

    datos = os.listdir(dproyecto) #listamos Dproyecto

    try:#copiamos el archivo de descargas a nuestro directorio de trabajo
        shutil.copy(csv_py, dproyecto)
    except:
        for i in datos:
            if i == csv_py:
                del i
                shutil.copy(csv_py, dproyecto)

    os.chdir(dproyecto)

    with open(csv_py,'r') as f:
        with open("listado2.csv",'w') as f1:
            next(f) # skip header line
            for line in f:
                f1.write(line)
    try:
        remove(csv_py)
    except:
        pass