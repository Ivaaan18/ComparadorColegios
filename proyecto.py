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

respuesta =''
bandera = 0

while respuesta != 'S' and respuesta != 'N':
    respuesta = input('Si es la primera vez que ejecutas el programa diga S (S o N) ')
    respuesta = respuesta.upper()
    if respuesta != 'S' and respuesta != 'N':
        print('¡¡ERROR!!: Escriba S o N')