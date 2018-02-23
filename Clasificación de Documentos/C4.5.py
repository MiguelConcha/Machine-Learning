class Clase:
	"""Una Clase es un posible valor de un atributo."""
	"""
	Los atributos tienen un conjunto de clases que representan los valores que el
	atributo puede tomar.
	"""
	def __init__(self, valor):
		"""Inicializa la Clase con el valor dado."""
		self.valor = valor

class Atributo:
	"""Un Atributo es ..."""
	"""
	Los Atributos representan ...
	"""
	def __init__(self, nombre, clases):
		"""Inicializa el Atributo con el nombre y las clases dadas."""
		self.nombre = nombre
		self.clases = []
		for clase in clases:
			self.clases.append(clase)

class Ejemplo:
	"""Un Ejemplo es ..."""
	"""
	Los Ejemplos representan ...
	"""
	def __init__(self, lista_atributos, lista_valores):
		"""Inicializa el Ejemplo con los atributos y valores dados"""
		self.atr_val = dict(zip(lista_atributos, lista_valores))
		self.atributos = atributos

class Nodo:
	"""Un Nodo es ..."""
	"""
	Los Nodos representan ...
	No se tiene una referencia a la vecindad del Nodo porque un Nodo puede
	pertenecer a varias gráficas y tener vecindades distintas en cada una.
	Por lo tanto es información que pertenece a cada gráfica.
	"""
	def __init__(self, valor):
		"""Inicializa el nodo con el valor dado."""
		self.valor = valor

	def __str__(self):
		return str(self.valor)

	def __repr__(self):
		return str(self.valor)

	def __eq__(self, other):
		return self.valor == other.valor

	def __hash__(self):
		return hash(self.valor)

class Grafica:
	""" Una Digráfica simple etiquetada es un conjunto V de vértices (Nodos), un
	conjunto de aristas entre vértices y una función de las aristas a las
	etiquetas."""
	"""
	No existen aristas paralelas.
	Las Digráficas pueden revisar los vecinos de un vértice en tiempo O(1).
	Las Digráficas pueden revisar las aristas que salen de un vértice en tiempo
	O(1).
	Las Digráficas pueden revisar la etiqueta de una arista en tiempo O(1).
	Las Digráficas pueden revisar la etiqueta de la arista entre dos vértices en
	tiempo O(maxdeg(g))
	Las Digráficas pueden revisar adyacencia entre vértices en tiempo O(1).

	Operaciones comunes para una grafica g:
	g.insertar(v)                --     agrega v al conjunto de vértices.
	g.vecinos[v]                 --     obtiene el conjunto de vecinos de v.
	g.aristas_salida[v]          --     obtiene el conjunto de aristas que tienen a v como
	                                    fuente.
	g.etiqueta[a]                --     obtiene la etiqueta de la arista a.
	g.etiqueta_entre(v1,v2)      --     obtiene la etiqueta de la arista (v1,v2).
	g.conectar(v1,v2,etiqueta)   --     conecta v1 con v2, es decir, agrega la arista
	                                    (v1,v2) con la etiqueta dada.
	g.desconectar(v1,v2)         --     elimina la conexión de v1 a v2.
	g.son_adyacentes(v1,v2)      --     verifica si v1 está conectado a v2.
	"""
	class Arista:
		"""
		Un Arista de una Digráfica es un vértice fuente y uno destino (ambos
		elementos del conjuntod de vértices de la digráfica).
		"""
		def __init__(self, fuente, destino):
			"""Inicializa la arista con la fuente y destino dados"""
			self.fuente = fuente
			self.destino = destino

		def __eq__(self, other):
			return self.fuente == other.fuente and self.destino == other.destino

		def __hash__(self):
			return hash(frozenset([self.fuente,self.destino]))

	def __init__(self):
		"""Inicializa la gráfica, inicialmente no tiene vértices ni aristas."""
		self.nodos = set()
		self.aristas = set()
		# Vecinos será un mapeo v:Nodos -> P(Nodos). Con esto se revisan los
		# vecinos de cualquier nodo en tiempo O(1).
		self.vecinos = dict()
		# AristasSalida será un mapeo v:Nodos -> P(Aristas). Con esto se revisan
		# las aristas que salen de un nodo en tempo O(1).
		self.aristas_salida = dict()
		# Etiqueta será un mapeo e:Aristas -> Etiquetas.
		self.etiqueta = dict()

	def insertar(self,nodo):
		"""Agrega un nodo al conjunto de nodos."""
		"""
		Se garantiza que existirá la lista de vecinos después de agregar un nodo
		con este método, es decir, existirá vecinos[nodo].
		"""
		self.nodos.add(nodo)
		self.vecinos[nodo] = set()
		self.aristas_salida[nodo] = set()

	def eliminar(self,nodo):
		"""Elimina un nodo del conjunto de nodos, junto con las aristas en las
		que se ve involucrado."""
		self.nodos.remove(nodo)
		del self.vecinos[nodo]
		del self.aristas_salida[nodo]
		for arista in self.aristas:
			if arista.fuente == nodo or arista.destino == nodo:
				aristas.remove(arista)

	def conectar(self,fuente,destino,etiqueta):
		"""Hace adyacentes dos nodos en la gráfica con la etiqueta dada"""
		"""
		Si alguno de los vértices no está en la gráfica, la operación devolverá
		Exception.
		Si ya existía una arista entre los dos vértices en la gráfica, la
		operación devolverá Excepcion.
		"""
		if fuente not in nodos or destino not in nodos:
			raise Exception("Conectando nodos que no pertenecen a la gráfica")
		if destino in self.vecinos[fuente]:
			raise Exception("Conectando nodos que ya eran adyacentes")

		self.vecinos[fuente].add(destino)

		arista = Grafica.Arista(fuente,destino)
		self.aristas.add(arista)
		self.aristas_salida[fuente].add(arista)

		self.etiqueta[arista] = etiqueta

	def desconectar(self,fuente,destino):
		"""Elimina la adyacencia entre dos nodos en la gráfica"""
		"""
		Si alguno de los vértices no está en la gráfica, o la arista no exite,
		la operación devolverá Exception.
		"""
		if fuente not in nodos or destino not in nodos:
			raise Exception("Desconectando nodos que no pertenecen a la gráfica")
		if destino not in self.vecinos[fuente]:
			raise Exception("Desconectando nodos no adyacentes")
		# Sabemos que sólo habrá una.
		arista = { a for a in self.aristas_salida[fuente] if a.fuente == fuente and a.destino == destino }
		arista = arista.pop()

		self.vecinos[fuente].remove(destino)
		self.aristas_salida[fuente].remove(arista)
		del self.etiqueta[arista]

	def son_adyacentes(self,fuente,destino):
		"""Verifica la adyacencia en la gráfica entre dos nodos"""
		return destino in self.vecinos[fuente]

	def etiqueta_entre(self,fuente,destino):
		"""Devuelve la etiqueta de la arista entre fuente y destino"""
		"""
		Si destino no es vecino de fuente, la operación devolverá Exception
		"""
		if destino not in self.vecinos[fuente]:
			raise Exception("Solicitando etiqueta de arista no existente")
		# Sabremos que sólo habrá una
		arista = { a for a in self.aristas_salida[fuente] if a.fuente == fuente and a.destino == destino }
		arista = arista.pop()
		return self.etiqueta[arista]

if __name__ == "__main__":
	# TEST
	g = Grafica()

	print("++Test de inserción de nodos")
	nodos = [ Nodo(x) for x in range(10) ]
	for nodo in nodos:
		g.insertar(nodo)
	print(g.nodos)

	print()

	print("++Test de inserción de aristas")
	print("Conectando nodo '1' y nodo '4', con la etiqueta 'excelente'")
	g.conectar(nodos[1],nodos[4],"excelente")
	print("Conectando nodo '1' y nodo '5', con la etiqueta 'asdf'")
	g.conectar(nodos[1],nodos[5],"asdf")
	print("Vecinos de nodo '1'?")
	print(g.vecinos[nodos[1]])
	print("Están conectados nodo '1' y nodo '4'?")
	print(g.son_adyacentes(nodos[1],nodos[4]))
	print("Etiqueta en la arista nodo'1',nodo'4'?")
	print(g.etiqueta_entre(nodos[1],nodos[4]))
	print("Están conectados nodo '1' y nodo '5'?")
	print(g.son_adyacentes(nodos[1],nodos[4]))
	print("Etiqueta en la arista nodo'1',nodo'5'?")
	print(g.etiqueta_entre(nodos[1],nodos[5]))

	print()

	print("++Test de eliminación de aristas")
	print("Desconectando nodo'1' de nodo '4'")
	g.desconectar(nodos[1],nodos[4])
	print("Vecinos de nodo '1'?")
	print(g.vecinos[nodos[1]])
	print("Están conectados nodo '1' y nodo '4'?")
	print(g.son_adyacentes(nodos[1],nodos[4]))
	print("Están conectados nodo '1' y nodo '5'?")
	print(g.son_adyacentes(nodos[1],nodos[5]))
	print("Etiqueta en la arista nodo'1',nodo'5'?")
	print(g.etiqueta_entre(nodos[1],nodos[5]))

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