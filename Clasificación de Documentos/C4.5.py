class Clase: 
	def __init__(self, valor):
		self.valor = valor

class Atributo:
	def __init__(self, nombre, clases):
		self.nombre = nombre
		for clase in clases:
			self.lista_clases.append(clase)

class Ejemplo:
	def __init__(self, lista_atributos, lista_valores):
		self.atr_val = dict(zip(lista_atributos, lista_valores))

class Nodo:
	def __init__(self, atributo):
		self.atributo = atributo

class Grafica:

	class Arista:
		pass

	pass

def calcular_entropia(conjunto_ejemplos, atributo_objetivo):
	entropia = 0
	clases_objetivo = []
	for ejemplo in conjunto_ejemplos:
		clases_objetivo.append(ejemplo.atr_val[atributo_objetivo])
	for valor in set(clases_objetivo):
		proba_i = float(clases_objetivo.count(valor))/len(clases_objetivo)
		proba_i -= proba_i * math.log(proba_i, 2)		
	return entropia

def calcular_entropia_condicional(conjunto_ejemplos, atributo_fijo, atributo_objetivo):
	suma_acumulada = 0
	clases_atr_fijo = []
	for ejemplo in conjunto_ejemplos:
		clases_atr_fijo.append(ejemplo.atr_val[atributo_fijo])
	clases_objetivo = []
	for ejemplo in conjunto_ejemplos:
		clases_objetivo.append(ejemplo.atr_val[atributo_objetivo])
	for valor in set(clases_atr_fijo):
		proba_i = float(clases_atr_fijo.count(valor))/len(clases_atr_fijo) 		#Frecuencia del valor del atributo fijo.
		lista_ejemplos_atributo_actual = []
		for ejemplo in conjunto_ejemplos:
			if ejemplo.atr_val[atributo_fijo] is valor:
				lista_ejemplos_atributo_actual.append(ejemplo)
		suma_acumulada += proba_i * calcular_entropia(lista_ejemplos_atributo_actual, atributo_objetivo)		
	return suma_acumulada

def calcular_ganancia(conjunto_ejemplos, atributo_a_partir, atributo_objetivo):
	return calcular_entropia(conjunto_ejemplos, atributo_objetivo) - calcular_entropia_condicional(conjunto_ejemplos, atributo_a_partir, atributo_objetivo)



if __name__ == '__main__':
	pass