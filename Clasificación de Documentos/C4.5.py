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
	