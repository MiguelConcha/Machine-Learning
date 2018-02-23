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

if __name__ == '__main__':
	pass