# coding=utf-8
#!/usr/bin/env python

"""proyecto2.py: Implementación de una red neuronal convolucional
   para el reconocimiento de frutas en imágenes como parte del segundo
   proyecto de la materia de Reconocimiento de Patrones y Aprendizaje
   Automatizado impartida en la UNAM (Facultad de Ciencias) por el profesor
   Gustavo de la Cruz Martínez.

   El usuario del programa puede solicitar el entrenamiento de la red neuronal
   para posteriormente llevar a cabo el periodo de prueba con nuevas imágenes de
   otros directorios o bien dadas a través de un URL; dado que el tiempo de entrenamiento
   consume alrededor de una hora, el modelo entrenado es almacenado para su recuperación
   de tal manera que se pueda probar directamente o solicitar la opción de un nuevo entrenamiento."""
__author__ = "Lezama Hernández María Ximena, Hernández Cano Leonardo, Vázquez Salcedo Eduardo Eder, Concha Vázquez Miguel"
__copyright__ = "Copyright (C) 2018 Reconocimiento de Patrones y Aprendizaje Automatizado, Facultad de Ciencias, UNAM"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Hernández Cano Leonardo"
__email__ = "leon_hc@ciencias.unam.mx"
__status__ = "Terminado"

# Haciendo la importación de las bibliotecas y el clasificador definido para este proyecto.
# Es necesiario tener instaladas las bibliotecas.
# El administrador de paquetes pip puede instalarlas con la instruccion 'pip install <nombre_biblioteca>'
# o bien ver si las tenemos ya con la instrucción 'pip freeze'.
# En el PDF del proyecto se detallan las funciones de estas bibliotecas usadas.
from fruit_classifier import FruitClassifier
import requests
from PIL import Image
from io import BytesIO
import os.path
import pickle

def request_image():
    '''
    Función que solicita una imagen (su ruta relativa o absoluta) al usuario a través de la entrada
    estándar y la abre antes de devolverla.
    '''
    print("Ruta de una imagen de una fruta:")
    filename = str(input())
    img = Image.open(filename)
    return img

def request_image_url():
    '''
    Función que solicita una imagen (su url) al usuario a través de la entrada
    estándar y la abre antes de devolverla.
    '''
    print("Url de una imagen de una fruta:")
    url = str(input())
    response = requests.get(url)                                             # Hace la petición a través del URL.        
    img = Image.open(BytesIO(response.content))                              # Abre lo que devuelve (el contenido) de la solicitud.
    return img

def print_classification(classification):
    '''
    Función que despliega el resulado de la clasificación.

    Parámetro
    ---------
    classification: dictionary
        El diccionario resultante de la clasificación de las frutas, cuyas llaves
        son las distintas frutas y el valor una probabilidad de que la fruta sea 
        de la clase indicada.
    '''
    tuples = [ (x,classification[x]) for x in classification.keys() ]
    tuples.sort(key=lambda x: -1 * x[1])
    for tup in tuples[:5]:                                                  # Nos muestra solamente las cinco clasificaciones más probables.
        print(tup)

if __name__=="__main__":
    exit = False
    print("Proyecto 2. ¡Clasificador de frutas!")
    fruit_classifier = FruitClassifier()
    while not exit:             
        print("0: Salir")                                                    # Opciones de interacción con el usuariod el programa.
        print("1: Clasificar imagen local")
        print("2: Clasificar imagen en url")
        print("3: Reentrenar")
        print("4: Mostrar representación gráfica del modelo")
        option = int(input())                                                # Leyendo la solicitud del usuario de la entrada estándar.
        if option == 0:
            exit = True
        elif option == 3:                                                    # En caso de solicitud de entrnamiento, borramos el modelo almacenado.
            fruit_classifier.delete_file()                                   # Se tiene que volver a entrenar la red.
            fruit_classifier = FruitClassifier()                 
        elif option == 4:
            fruit_classifier.show_model()                                    # Opción para la visulización del modelo especificada en el archivo 'fruit_classifier.py'.                       
        else:
            if option == 1:
                fruit_image = request_image()                                # Opción para probar una imagen dada la ruta de la misma.
            if option == 2:
                fruit_image = request_image_url()                            # Opción para probar una imagen dado su url.
            print_classification(fruit_classifier.classify(fruit_image))     # Imprimimos el resulado de la clasificación en ambos casos.
