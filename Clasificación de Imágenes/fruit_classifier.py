# coding=utf-8
#!/usr/bin/env python

"""fruit_classifier.py: Implementación de una red neuronal convolucional
   para el reconocimiento de frutas en imágenes como parte del segundo
   proyecto de la materia de Reconocimiento de Patrones y Aprendizaje
   Automatizado impartida en la UNAM (Facultad de Ciencias) por el profesor
   Gustavo de la Cruz Martínez.

   Se incluyen las clases y métodos necesario para llevar a cabo el entrenamiento
   de la red neuronal, además de la definición de su arquitectura."""
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
import numpy as np
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, load_model
from keras.utils import to_categorical
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, Activation, BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import Adamax
from PIL import Image
import os.path
from os import listdir, remove
from os.path import isfile, join, isdir
from random import shuffle
import gc

class ClassifiedImage:
    '''
    Clase que representa a una imagen ya clasificada por la red neuronal.

    Parámetros:
    -----------

    image: Imagen
        La imagen clasificada.

    classificacion: dictionary:
        El resultado de su clasificación.
    '''
    def __init__(self,image,classification):
        self.image = image
        self.classification = classification

class FruitClassifier:
    """
    Un clasificador de frutas es un objeto que emplea la red
    neuronal con la arquitectura que se define en el método constructor del 
    modelo para la clasificación de frutas a través de imágenes.
    El constructor recibe la ruta con el folder que tiene carpetas para cada
    categoría, que a su vez contienen imagenes de la categoría.

    Ocupa una red neuronal como clasificador.
    """
    def __init__(self):
        self.target_size = (64,64)                                                              # Imágenes de 64x64 con 3 canales de color.
        self.image_shape = (64,64,3)
        path_training = "./fruits/Training"             
        path_validation = "./fruits/Validation"
        directories = [f for f in listdir(path_training) if isdir(join(path_training, f))]      # Tomando todos las carpetas para el entrenamiento a partir de la ruta.
        self.categories = sorted(directories)
        self.categories_map = dict(zip(self.categories, range(len(self.categories))))           # El map que asocia igual nombres de directorios a números que flow_from_directory

        classifier_path = "./FrutaLoca.h5"                                                      # Verificar si está guardado el modelo que ocupa el clasificador. 
        if os.path.isfile(classifier_path):
            print("FrutaLoca.h5 encontrado")
            self.model = load_model(classifier_path)                                            # En caso positivo, simpelemente se recupera el modelo ya entrenado.
        else:
            print("FrutaLoca.h5 no encontrado, se construirá. Tomará tiempo.")                  # En otro caso, se tiene que entrenar.
            self.model = self.build_model()                                                     # Definiendo la arquitectura de la red neuronal.
            """
            Se utilizan las clases provistas por Keras para definir la configuración de 
            las imágenes del conjunto de entrenamiento y prueba. En vez de llevar a cabo
            operaciones directamente sobre el dataset en la memoria, esta biblioteca
            es una interfaz de desarrollo (API) que nos permite llevar a cabo el proceso
            de aprendizaje ('fitting') con aprendizaje profundo iterativo creando datos
            de las imágenes sobre demanda en tiempo real.
            """
            train_datagen = ImageDataGenerator()
            train_generator = train_datagen.flow_from_directory(                                # Conjunto de entrenamiento y sus especificaciones,
                path_training,
                target_size = self.target_size,                                                 # Las dimensiones de la imagen.
                class_mode = "categorical",                                                     # Se especifica una clasificación por categorías, no binaria.
                color_mode = "rgb")                                                             # El modo de color de las imágenes (canales).
            test_datagen = ImageDataGenerator()
            validation_generator = test_datagen.flow_from_directory(
                path_validation,
                target_size = self.target_size,                                                 # Las dimensiones de la imagen.
                class_mode = "categorical",                                                     # Se especifica una clasificación por categorías, no binaria.
                color_mode = "rgb")                                                             # El modo de color de las imágenes (canales).
            self.model.fit_generator(                                                           # Ajustando los pesos de la red neuronal; se entrena por lotes en tiempo real.
                train_generator,                                                                
                epochs=10,                                                                      # Número de épocas de entrneamiento.
                validation_data=validation_generator,
                use_multiprocessing=True,                                                       # Acelerando un poco el proceso.
                workers=3,
                shuffle=True)
            self.model.save(classifier_path)                                                    # Luego del entrenamiento, el modelo lo almacenamos en el archivo para la siguiente vez.

    def build_model(self):
        """
        Método privado que construye 
        la red neuronal.
        """
        image_shape = self.image_shape
        output_nodes = len(self.categories)
        model = Sequential()                                                                    # La arquitectura usada es secuencial por capas.
        """
        La definición de la arquitectura convolucional de la red neuronal
        se basó en el tutorial de Keras y en los resultados obtenidos 
        por Naveen Chaudhary para el mismo dataset.
        """
        model.add(Conv2D(16,(3,3),input_shape=image_shape,padding='same'))                      # Capa convolucional bidimensional.
        model.add(LeakyReLU(0.5))                                                               # Función de activación relu (leaky): x si x > 0 y (0.01 * x) en caso contrario.
        model.add(BatchNormalization())                                                         # Método para mantener la media de activación de la capa previa cercada a cero y la desviación estándar cercana a uno.
        model.add(MaxPooling2D(pool_size=(2,2)))

        model.add(Conv2D(32,(3,3),padding='same'))                                              # Capa convolucional bidimensional.
        model.add(LeakyReLU(0.5))                                                               # Función de activación relu (leaky): x si x > 0 y (0.01 * x) en caso contrario.
        model.add(BatchNormalization())                                                         # Método para mantener la media de activación de la capa previa cercada a cero y la desviación estándar cercana a uno.
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(32,(3,3),padding='same'))                                              # Capa convolucional bidimensional.
        model.add(LeakyReLU(0.5))                                                               # Función de activación relu (leaky): x si x > 0 y (0.01 * x) en caso contrario.
        model.add(BatchNormalization())                                                         # Método para mantener la media de activación de la capa previa cercada a cero y la desviación estándar cercana a uno.
        model.add(MaxPooling2D(pool_size=(2,2)))

        model.add(Conv2D(64,(3,3),padding='same'))                                              # Capa convolucional bidimensional.
        model.add(LeakyReLU(0.5))                                                               # Función de activación relu (leaky): x si x > 0 y (0.01 * x) en caso contrario.
        model.add(BatchNormalization())                                                         # Método para mantener la media de activación de la capa previa cercada a cero y la desviación estándar cercana a uno.
        model.add(MaxPooling2D(pool_size=(2,2)))

        model.add(Flatten())                                                                    # Aplanando las capas.
        model.add(Dense(256,activation='elu'))                                                  # Función de activación elu ('Exponential Lineal Unit').
        model.add(Dropout(0.5))
        model.add(Dense(len(self.categories)))
        model.add(Activation("softmax"))                                                        # Empleamos a la función 'softmax' como función de activación en la salida, una generalización de la logística sigmoide.

        '''
        Antes de poder usar el modelo la siguiente vez, se tiene
        que compilar de tal manera que las predicciones del mismo
        usen el tiempo de cómputo apropiado.
        '''
        model.compile(loss='categorical_crossentropy',metrics=['accuracy'], optimizer=Adamax())             
        return model

    def classify(self,fruit_image):
        """
        Método que devuelve un diccionario cuyas llaves son diferentes frutas y el
        valor asociado a una llave es un número entre cero y uno que puede ser
        interpretado como la probabilidad de que la imagen sea de la fruta a la
        que refiere la llave.
        """
        fruit_image = self.normalize(fruit_image)
        fruit_image = np.array([fruit_image])
        preds = self.model.predict(fruit_image)
        predictions = {}
        for i in range(len(preds[0])):
            predictions[self.categories[i]] = preds[0][i]
        return predictions

    def show_model(self):
        """
        Método que permite la visualización de la red neuronal con la ayuda
        de una biblioteca que va de la mano con Keras y utiliza la biblioteca de 
        graficación graphviz de python con tal de prover una gráfica que la represente.

        Tuvimos que simular el modelo con sus capas importantes
        debido a que ann_vizualizer no tiene soporte para las últimas capas
        del modelo completo y de lo contrario el programa falla
        """
        from ann_visualizer.visualize import ann_viz
        image_shape = self.image_shape
        output_nodes = len(self.categories)
        model = Sequential()                                                                    # La arquitectura usada es secuencial por capas.
   
        model.add(Conv2D(16,(3,3),input_shape=image_shape,padding='same'))                      # Capa convolucional bidimensional.
        #model.add(LeakyReLU(0.5))                                                               # Función de activación relu (leaky): x si x > 0 y (0.01 * x) en caso contrario.
        #model.add(BatchNormalization())                                                         # Método para mantener la media de activación de la capa previa cercada a cero y la desviación estándar cercana a uno.
        model.add(MaxPooling2D(pool_size=(2,2)))

        model.add(Conv2D(32,(3,3),padding='same'))                                              # Capa convolucional bidimensional.
        #model.add(LeakyReLU(0.5))                                                               # Función de activación relu (leaky): x si x > 0 y (0.01 * x) en caso contrario.
        #model.add(BatchNormalization())                                                         # Método para mantener la media de activación de la capa previa cercada a cero y la desviación estándar cercana a uno.
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(32,(3,3),padding='same'))                                              # Capa convolucional bidimensional.
        #model.add(LeakyReLU(0.5))                                                               # Función de activación relu (leaky): x si x > 0 y (0.01 * x) en caso contrario.
        #model.add(BatchNormalization())                                                         # Método para mantener la media de activación de la capa previa cercada a cero y la desviación estándar cercana a uno.
        #model.add(MaxPooling2D(pool_size=(2,2)))

        model.add(Conv2D(64,(3,3),padding='same'))                                              # Capa convolucional bidimensional.
        #model.add(LeakyReLU(0.5))                                                               # Función de activación relu (leaky): x si x > 0 y (0.01 * x) en caso contrario.
        #model.add(BatchNormalization())                                                         # Método para mantener la media de activación de la capa previa cercada a cero y la desviación estándar cercana a uno.
        #model.add(MaxPooling2D(pool_size=(2,2)))

        model.add(Flatten())                                                                    # Aplanando las capas.
        model.add(Dense(256,activation='elu'))                                                  # Función de activación elu ('Exponential Lineal Unit').
        model.add(Dropout(0.5))
        model.add(Dense(len(self.categories)))
        model.add(Activation("softmax"))                                                        # Empleamos a la función 'softmax' como función de activación en la salida, una generalización de la logística sigmoide.
        #model.compile(loss='categorical_crossentropy',metrics=['accuracy'], optimizer=Adamax())  
        ann_viz(model)                                     # Basta con pasar el modelo que se quiere visualizar.

    def normalize(self,img):
        """
        Aplica el preprocesamiento necesario a una imagen para que pueda ser
        usado en el clasificador. Este es un método privado.

        Parámetro
        ---------
        img: Imagen
            La imagen que será clasificada.
        """
        if img.mode != "RGB":                              # Normalizamos siempre a formato RGB (red, green, blue).
            img = img.convert("RGB")
        if img.size != self.target_size:                   # Las ponemos siempre del mismo tamaño.
            img = img.resize(self.target_size)
        x = image.img_to_array(img)                        # Convierta la instancia PIL (la imagen) a una matriz de numpy.
        return x

    def delete_file(self):
        """
        Método que elimina al modelo entrenado.
        """
        classifier_path = "./FrutaLoca.h5"                 # Se le pasa la ruta al modelo entrenado y se suprime.
        remove(classifier_path)
