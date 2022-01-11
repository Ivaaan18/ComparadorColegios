import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
import os
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



def obtencion_datos():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.maximize_window()
    driver.get('https://gestiona3.madrid.org/wpad_pub/run/j/MostrarConsultaGeneral.icm')

    data = []

    df = pd.read_csv('listado2.csv', sep=';', engine='python')
    df.to_csv('datosssss.csv', sep=';')
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


def comparador_centros():
    respuesta1 = ''
    Codigos = []

    while respuesta1 != 'S' and respuesta1 != 'N':
        respuesta1 = input('¿Te gustaria comparar varios centros? S o N ')
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
    else:
        print("El programa se va a cerrar.")
        time.sleep(2)

def bucle1():
    respuesta =''
    bandera = 0
    print('Bienvenido al comparador de centros de la Comunidad de Madrid\n')
    while respuesta != 'S' and respuesta != 'N':
        respuesta = input('Si es la primera vez que ejecutas el programa diga S (S o N) ')
        respuesta = respuesta.upper()
    if respuesta != 'S' and respuesta != 'N':

if __name__ == '__main__':

    respuesta = bucle1()

    if respuesta == 'S':
        # csv1()
        listado2()
        obtencion_datos()
        # os.system ("cls")
        # comparador_centros()
    else:
        comparador_centros()

