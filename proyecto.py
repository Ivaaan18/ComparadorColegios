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

if respuesta == 'S':
    # funcion 1
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
    # funcion 2
    a = os.getcwd() + os.sep
    a = a.split('\\')

    draiz = a[0] + '\\'
    dusers = draiz + a[1] + '\\'
    duser = dusers + a[2] + '\\'
    ddesktop = duser + a[3] + '\\'

    ddescargas = duser + 'Downloads\\'
    dp = a[4] + '\\' + a[5] + '\\'
    dproyecto = ddesktop + dp
    print(dproyecto)

    os.chdir(ddescargas)  # nos situamos en el directorio descargas
    contenidos = os.listdir(ddescargas)  # listamos el directorio descargas
    csv = []

    for contenido in contenidos:
        if os.path.isfile(os.path.join(ddescargas, contenido)) and contenido.endswith('.csv'):
            csv.append(contenido)

    csv_py = csv[0]  # elegimos el csv que hemos acabado de descargar

    datos = os.listdir(dproyecto)  # listamos Dproyecto

    try:  # copiamos el archivo de descargas a nuestro directorio de trabajo
        shutil.copy(csv_py, dproyecto)
    except:
        for i in datos:
            if i == csv_py:
                del i
                shutil.copy(csv_py, dproyecto)

    os.chdir(dproyecto)

    with open(csv_py, 'r') as f:
        with open("listado2.csv", 'w') as f1:
            next(f)  # skip header line
            for line in f:
                f1.write(line)
    try:
        remove(csv_py)
    except:
        pass
    # funcion 3
    # Recopilación de los datos de los centros especialidad bachillerato
    driver = webdriver.Chrome("chromedriver.exe")
    driver.maximize_window()
    driver.get('https://gestiona3.madrid.org/wpad_pub/run/j/MostrarConsultaGeneral.icm')

    data = []

    df = pd.read_csv('listado2.csv', sep=';', engine='python')

    for key, value in df.iteritems():
        if key == "TIPO DE CENTRO":
            for centro in value:
                centro = [centro]
                data.append(centro)
    z = 0
    for key, value in df.iteritems():
        if key == "COD. POSTAL":
            for telf in value:
                data[z].append(telf)
                z += 1

    z = j = 0

    for key, value in df.iteritems():
        if key == "AREA TERRITORIAL":
            for new in value:
                new = str(new)
                #####            Seleccionamos buscador de colegios
                try:
                    Buscador_colegios = driver.find_element_by_xpath(
                        '//*[@id="cabecera_superior_logo3"]/table/tbody/tr/td/a/img')
                    click_Buscador_colegios = Buscador_colegios.click()
                    time.sleep(1)
                except:
                    Buscador_colegios = driver.find_element_by_xpath(
                        '//*[@id="cabecera_superior_logo3"]/table/tbody/tr/td/a/img')
                    click_Buscador_colegios = Buscador_colegios.click()
                    time.sleep(3)
                    #####            Boton de escribir
                try:
                    Boton_escribir = driver.find_element_by_id("basica.strCodNomMuni")
                    click_Boton_escribir = Boton_escribir.click()
                    time.sleep(1)
                except:
                    Boton_escribir = driver.find_element_by_id("basica.strCodNomMuni")
                    click_Boton_escribir = Boton_escribir.click()
                    time.sleep(3)

                #####            Escribir codigo centro
                try:
                    element = Boton_escribir
                    element.send_keys(new + Keys.ENTER)
                    time.sleep(0.5)
                except:
                    element = Boton_escribir
                    element.send_keys(new + Keys.ENTER)
                    time.sleep(2)

                #####            centro
                try:
                    centro = driver.find_element_by_xpath('//*[@id="formResultadoLista"]/table/tbody/tr[4]/td[2]/a')
                    click_centro = centro.click()
                    time.sleep(1)
                except:
                    centro = driver.find_element_by_xpath('//*[@id="formResultadoLista"]/table/tbody/tr[4]/td[2]/a')
                    click_centro = centro.click()
                    time.sleep(3)

                #####            resultados academicos
                try:
                    try:
                        resultados_academicos = driver.find_element_by_xpath('//*[@id="solapastab2"]/span')
                        click_resultados_academicos = resultados_academicos.click()
                        time.sleep(1)
                    except:
                        resultados_academicos = driver.find_element_by_xpath('//*[@id="solapastab2"]/span')
                        click_resultados_academicos = resultados_academicos.click()
                        time.sleep(3)

                    #####            Transformacion html bs4

                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    Tabla_titulacion = soup.find(id="tablaDatos.grafica5")
                    Tabla_selectividad = soup.find(id="tablaDatos.grafica9")
                    time.sleep(1.5)

                    # new = codigo del centro, lo cargamos en la lista
                    data[z].append(new)

                    #####            obtencion de datos
                    try:
                        for td2 in Tabla_titulacion.find_all('tr'):
                            row2 = [i.text for i in td2.find_all('td')]
                            for i in row2:
                                data[z].append(i)
                    except:
                        # print('No se han podido obtener los datos de la tabla de titulacion', new)
                        titulacion = ('No se han podido obtener los datos de la tabla de titulacion')
                        data[z].append(titulacion)

                    try:
                        for td3 in Tabla_selectividad.find_all('tr'):
                            row3 = [i.text for i in td3.find_all('td')]
                            for i in row3:
                                data[z].append(i)
                    except:
                        # print('No se han podido obtener los datos de la tabla de selectividad', new)
                        selectividad = ('No se han podido obtener los datos de la tabla de selectividad')
                        data[z].append(selectividad)

                    z += 1
                    j += 1
                    if j == 2:
                        break

                except:

                    try:
                        resultados_academicos = driver.find_element_by_xpath('//*[@id="solapastab1"]/span')
                        click_resultados_academicos = resultados_academicos.click()
                        time.sleep(1)
                    except:
                        resultados_academicos = driver.find_element_by_xpath('//*[@id="solapastab1"]/span')
                        click_resultados_academicos = resultados_academicos.click()
                        time.sleep(3)

                    #####            Transformacion html bs4

                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    Tabla_titulacion = soup.find(id="tablaDatos.grafica5")
                    Tabla_selectividad = soup.find(id="tablaDatos.grafica9")
                    time.sleep(1.5)

                    # new = codigo del centro, lo cargamos en la lista
                    data[z].append(new)

                    #####            obtencion de datos
                    try:
                        for td2 in Tabla_titulacion.find_all('tr'):
                            row2 = [i.text for i in td2.find_all('td')]
                            for i in row2:
                                data[z].append(i)
                    except:
                        # print('No se han podido obtener los datos de la tabla de titulacion', new)
                        titulacion = ('No se han podido obtener los datos de la tabla de titulacion')
                        data[z].append(titulacion)

                    try:
                        for td3 in Tabla_selectividad.find_all('tr'):
                            row3 = [i.text for i in td3.find_all('td')]
                            for i in row3:
                                data[z].append(i)
                    except:
                        # print('No se han podido obtener los datos de la tabla de selectividad', new)
                        selectividad = ('No se han podido obtener los datos de la tabla de selectividad')
                        data[z].append(selectividad)

                    z += 1
                    j += 1
                    if j == 2:
                        break
    driver.close()
    # eliminar listado2

    # Trato de los datos
    df2 = pd.DataFrame(data)
    df2 = df2.drop(
        df2.columns[[3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 33, 34, 35, 36, 37, 38]],
        axis='columns')
    df2.columns = ['Nombre Centro', 'Telefono', 'COD Centro', 'Titulacion 2013/14', 'Titulacion 2014/15',
                   'Titulacion 2015/16', 'Titulacion 2016/17', 'Titulacion 2017/18', 'Evau 2013/14', 'Evau 2014/15',
                   'Evau 2015/16', 'Evau 2016/17', 'Evau 2017/18']
    df2 = df2.reindex(columns=['COD Centro', 'Nombre Centro', 'Telefono', 'Titulacion 2013/14', 'Titulacion 2014/15',
                               'Titulacion 2015/16', 'Titulacion 2016/17', 'Titulacion 2017/18', 'Evau 2013/14',
                               'Evau 2014/15', 'Evau 2015/16', 'Evau 2016/17', 'Evau 2017/18'])
    df2.set_index('COD Centro', inplace=True)

    # exportar todos los datos a un csv:
    print(
        'A continuación se descargará en datos_colegios.csv un listado con todos los colegios de la Comunidad de Madrid\n')
    df2.to_csv('datos_colegios.csv', sep=';')
    print('Se han descargado los datos')
    bandera = 1