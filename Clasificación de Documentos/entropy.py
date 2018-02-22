def calcular_entropia(atributo):
	""" 
	Devuelve la entropía discreta del atributo dado.
	Realiza la suma (con signo negativo) ponderada de la información
	transmitida por cada clase (posibles valores) por la proporción 
	de los elementos de la misma.
	La entropía (sorpresa) sin la división en los valores distintos, i.e.,
	para una misma columna, no se consideran los distintos valores que puede
	tomar el atributo.
    """
	entropia = 0										
	for x in set(atributo):										#No consideramos valores repetidos.
		proba_i = float(atributo.count(x))/len(atributo)		#La probabilidad es el número de veces que aparece en la columna cada valor único entre el número de valores totales.
		entropia -= proba_i * math.log(proba_i, 2)				#Aplicamos la sustracción de acuerdo con la fórmula para la entropía de la información; tomamos logaritmo base 2.
	return entropia

def calcular_resto(atributo, resultados):
	'''
	Calcula la suma acumulada de la ponderación de los valores
	posibles para la columna (atributo) por la entropía que nada
	más considera en cada caso a dichos valores de la columna.
	'''
	suma_acumulada = 0
	diccionario = {}
	for i in range(0,len(atributo)):							#Iterando sobre las filas de la columna.
		if atributo[i] in diccionario:							#Si vemos una categoría ya vista antes:
			diccionario[atributo[i]][0] += 1					#Aumentamos su número de apariciones.
			diccionario[atributo[i]][1].append(resultados[i])   #Agregamos a la lista de esa categoría lo que viene como resultado.
		else:													#En otro caso la agregamos, con una aparición
			diccionario[atributo[i]] = (1,list(resultados[i])) 	#e inicializamos su lista de resultados con el valor que aparece en la tabla.
	for llave in diccionario:									#Calculamos la entropía de cada categoría:
		veces_que_aparece = llave[0]							#Tenemos el contador.
		ponderacion_llave = float(veces_que_aparece/len(atributo))
		#Ahora calculamos la entropía de esa categoría (llave):
		entropia_llave = 0										
		for x in set(llave[1]):									#Cada categoría (llave) tiene su lista guardada.
		  proba_i = float(llave[1].count(x))/len(llave[1])		#La probabilidad es el número de veces que aparece.
		  entropia_llave -= proba_i * math.log(proba_i, 2)		#Aplicamos la sustracción de acuerdo con la fórmula para la entropía de la información; tomamos logaritmo base 2.
		  suma_acumulada += ponderacion_llave * entropia_llave
	return suma_acumulada

def calcular_ganancia(atributo):
	'''
	Función que devuelve la ganancia de información, esto es,
	la reducción en la entropía esperada al hacer la división 
	sobre el atributo en cuestión.
	'''
	return calcular_entropia(atributo) - calcular_resto(atributo)

def correr_c45():
	print("...working")

if __name__ == '__main__':
	correr_c45()