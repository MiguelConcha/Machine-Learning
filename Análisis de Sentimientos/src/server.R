# ---------------------------------------- #
#                SERVIDOR                  #
# ---------------------------------------- #
shinyServer(
  # Activo todo el tiempo.
  function(input, output, session) {
    # A la espera de clicks en el boton para bajar tweets.
    observeEvent(input$bajar_tweets, {   
      hashtag <- input$hashtag
      # En caso de que el usuario quiera otro tema, lo actualizamos.
      if(hashtag == 'Otro') {
        hashtag <- input$otroHashtag     
      }
      # Informacion de autenticacion de la cuenta developer de Twitter.
      api_key <- 'TI8NRQd65Ijuc9m5v6VFTxZUk'
      api_secret <- 'gdNFt7ht4YF10hNXEbHq9mrhTLQTbXCr3gb7iXtL3WSg73kUFU'
      access_token <- '1003785782228934656-UO4b26k2LCQ4Wt0xDWiSpiEKNhwWQS'
      access_token_secret <- 'Ux7a6HWEjjnD48mh7wEM2UaOTE2dJMeicTEjoC69IUSGO'
      # Importando la biblioteca para bajar los tweets.
      library(twitteR)
      # Autorizando la cuenta con los datos previos.
      setup_twitter_oauth(api_key, api_secret, access_token, access_token_secret)
      # Buscando los tweets con los parametros dados por el usuario de cantidad, fecha y tema.
      tweets <- searchTwitter(hashtag, n=as.numeric(input$numTweets), since=as.character(input$fecha), lang = 'es')
      # Convirtiendo los datos a un formato tabular estructurado (dataframe).
      tweets_df <- twListToDF(tweets)
      # Escribiendo el archivo en el lugar en donde sea indicado por el usuario.
      write.csv(tweets_df, file=file.choose(), row.names=F)
      print(">> El archivo ha sido escrito.")
    })
    # A la espera de click para analizar los sentimientos.
    # Caso de ruta seleccionada por el usuario.
    observeEvent(input$seleccion, {
      # Importando las bibliotecas de mineria de textos y la que tiene los diccionarios de palabras-sentimientos.
      library(tm)
      library(syuzhet)
      # Leyendo el .csv especificado.
      tweets <- read.csv(file=file.choose(), header = T)
      # La unica columna importante en este caso es la del contenido mismo del tweet.
      sentimientos_terminos <- iconv(tweets$text)
      # Obteniendo la matriz de sentimientos.
      sentimientos <- get_nrc_sentiment(sentimientos_terminos)
      # Graficando los sentimientos.
      output$grafica <- renderPlot({barplot(colSums(sentimientos), las = 2, col = rainbow(10), ylab = 'Cuenta', main = 'Sentimientos')})
    })
    # A la espera de click en el boton para el an. sentimientos.
    # Caso de ruta a los archivos predefinida.
    observeEvent(input$predefinido, {
      # Importando las bibliotecas de mineria de textos y la que tiene los diccionarios de palabras-sentimientos.
      library(tm)
      library(syuzhet)
      # A partir del tema seleccionado, podemos dar la ruta relativa al archivo .csv.
      ruta_archivo = ""
      if(input$tema == "#AMLO") {
        ruta_archivo = "..\\Data\\amlo.csv"
      } else if(input$tema == "#RicardoAnaya") {
        ruta_archivo = "..\\Data\\anaya.csv"
      } else if(input$tema == "#Meade") {
        ruta_archivo = "..\\Data\\meade.csv"
      } else if(input$tema == "#ElBronco") {
        ruta_archivo = "..\\Data\\bronco.csv"
      } else if(input$tema == "#Elecciones2018") {
        ruta_archivo = "..\\Data\\elecciones.csv"
      } else {
        ruta_archivo = "..\\Data\\ine.csv"
      }
      # Leyendo el archivo a partir de la ruta predefinida.
      tweets <- read.csv(ruta_archivo, header = T)
      # La unica columna importante en este caso es la del contenido mismo del tweet.
      sentimientos_terminos <- iconv(tweets$text)
      # Obteniendo la matriz de sentimientos.
      sentimientos <- get_nrc_sentiment(sentimientos_terminos)
      # Graficando los sentimientos.
      output$grafica <- renderPlot({barplot(colSums(sentimientos), las = 2, col = rainbow(10), ylab = 'Cuenta', main = 'Sentimientos')})
    })
    # CAso para cuando se quieren analizar palabras comunes.
    # Caso de ruta seleccionada por el usuario.
    observeEvent(input$seleccion_t, {
      # Bibilioteca de mineria de textos es importada.
      library(tm)
      # Leyendo el CSV dado por el usuario.
      tweets <- read.csv(file=file.choose(), header = T)
      # Creamos la coleccion de documentos, en donde cada uno es un tweet y nos interesa solo el texto.
      corpus <- iconv(tweets$text)
      corpus <- Corpus(VectorSource(corpus))
      # Limpiando el contenido: a minusculas todo, sin signos de puntuacion, nums., quitando URLs
      # y ademas agregando una lista predefinida de stopwords que agregamos a los de siempre.
      corpus <- tm_map(corpus, tolower)
      corpus <- tm_map(corpus, removePunctuation)
      corpus <- tm_map(corpus, removeNumbers)
      removeURL <- function(x) gsub('http[[:alnum:]]*', '', x)
      cleanset <- tm_map(corpus, content_transformer(removeURL))
      stopwords <- read.csv("..\\Data\\stopwords.csv", header = FALSE)
      stopwords <- as.character(stopwords$V1)
      stopwords <- c(stopwords, stopwords())
      cleanset <- tm_map(corpus, removeWords, stopwords)
      # De igual manera, dependiendo del hashtag elegido, quitamos palabras que evidentemente seran las que aparezcan en mayor grado.
      if(input$tema_t == "#AMLO") {
        cleanset <- tm_map(cleanset, removeWords, c('amlo', 'andresmanuel', 'lopezobrador'))
      } else if(input$tema_t == "#RicardoAnaya") {
        cleanset <- tm_map(cleanset, removeWords, c('anaya', 'ricardoanaya', 'ricardoanayac'))
      } else if(input$tema_t == "#Meade") {
        cleanset <- tm_map(cleanset, removeWords, c('meade', 'joseantoniomeade', 'joseantoniomeadek'))
      } else if(input$tema_t == "#ElBronco") {
        cleanset <- tm_map(cleanset, removeWords, c('bronco', 'elbronco', 'jaimerodriguez', 'jaimerodriguezcalderon'))
      } else if(input$tema_t == "#Elecciones2018") {
        cleanset <- tm_map(cleanset, removeWords, c('elecciones', 'eleccionesmexico', 'elecciones2018', 'mexico'))
      } else {
        cleanset <- tm_map(cleanset, removeWords, c('ine', 'inemexico', 'institutoelectoral', 'debate', 'institutonacionalelectoral'))
      }
      # Quitando multi-espacios en blanco.
      cleanset <- tm_map(cleanset, stripWhitespace)
      # Crando la matriz de terminos.
      tdm <- TermDocumentMatrix(cleanset)
      tdm <- as.matrix(tdm)
      # Contando cuantas veces aparecen las palabras.
      apariciones <- rowSums(tdm)
      # Nos quedamos solamente con las que aparezcan mas del numero especificado.
      apariciones <- subset(apariciones, apariciones >= as.numeric(input$min_apariciones))
      # Graficando las palabras comunes con barras.
      output$grafica <- renderPlot({barplot(apariciones,                                    
                                            las = 2,
                                            col = rainbow(50),
                                            ylab = 'Num. Apariciones',
                                            xlab = 'Palabra',
                                            cex.names = 0.5)})
    })
    # Cuando se quieren analizar las palabras mas usadas.
    # Caso para cuando la ruta al archivo CSV es predefinida.
    observeEvent(input$predefinido_t, {
      # Importando la biblioteca de mineria de textos.
      library(tm)
      # Se construye la ruta relativa al archivo dependiendo del tema especificado por el usuario.
      ruta_archivo = ""
      if(input$tema_t == "#AMLO") {
        ruta_archivo = "..\\Data\\amlo.csv"
      } else if(input$tema_t == "#RicardoAnaya") {
        ruta_archivo = "..\\Data\\anaya.csv"
      } else if(input$tema_t == "#Meade") {
        ruta_archivo = "..\\Data\\meade.csv"
      } else if(input$tema_t == "#ElBronco") {
        ruta_archivo = "..\\Data\\bronco.csv"
      } else if(input$tema_t == "#Elecciones2018") {
        ruta_archivo = "..\\Data\\elecciones.csv"
      } else if(input$tema_t == "#INE") {
        ruta_archivo = "..\\Data\\ine.csv"
      }
      # Leyendo el archivo.
      tweets <- read.csv(ruta_archivo, header = T)
      # Creamos la coleccion de documentos, en donde cada uno es un tweet y nos interesa solo el texto.
      corpus <- iconv(tweets$text)
      corpus <- Corpus(VectorSource(corpus))
      # Limpiando el contenido: a minusculas todo, sin signos de puntuacion, nums., quitando URLs
      # y ademas agregando una lista predefinida de stopwords que agregamos a los de siempre.
      corpus <- tm_map(corpus, tolower)
      corpus <- tm_map(corpus, removePunctuation)
      corpus <- tm_map(corpus, removeNumbers)
      removeURL <- function(x) gsub('http[[:alnum:]]*', '', x)
      cleanset <- tm_map(corpus, content_transformer(removeURL))
      stopwords <- read.csv("..\\Data\\stopwords.csv", header = FALSE)
      stopwords <- as.character(stopwords$V1)
      stopwords <- c(stopwords, stopwords())
      cleanset <- tm_map(corpus, removeWords, stopwords)
      # De igual manera, dependiendo del tema particular elegido, podemos descartar palabras que evidentemente seran las del hashtag.
      if(input$tema_t == "#AMLO") {
        cleanset <- tm_map(cleanset, removeWords, c('amlo', 'andresmanuel', 'lopezobrador'))
      } else if(input$tema_t == "#RicardoAnaya") {
        cleanset <- tm_map(cleanset, removeWords, c('anaya', 'ricardoanaya', 'ricardoanayac'))
      } else if(input$tema_t == "#Meade") {
        cleanset <- tm_map(cleanset, removeWords, c('meade', 'joseantoniomeade', 'joseantoniomeadek'))
      } else if(input$tema_t == "#ElBronco") {
        cleanset <- tm_map(cleanset, removeWords, c('bronco', 'elbronco', 'jaimerodriguez', 'jaimerodriguezcalderon'))
      } else if(input$tema_t == "#Elecciones2018") {
        cleanset <- tm_map(cleanset, removeWords, c('elecciones', 'eleccionesmexico', 'elecciones2018', 'mexico'))
      } else {
        cleanset <- tm_map(cleanset, removeWords, c('ine', 'inemexico', 'institutoelectoral', 'debate', 'institutonacionalelectoral'))
      }
      # Quitando multi-espacios en blanco.
      cleanset <- tm_map(cleanset, stripWhitespace)
      # Crando la matriz de palabras.
      tdm <- TermDocumentMatrix(cleanset)
      tdm <- as.matrix(tdm)
      # Obteniendo la cantidad de veces que aparecen.
      apariciones <- rowSums(tdm)
      # Nos quedamos con aquellas que aparezcan mas del numero especificado.
      apariciones <- subset(apariciones, apariciones >= as.numeric(input$min_apariciones))
      # Graficando con barras las palabras que mas aparecieron.
      output$grafica <- renderPlot({barplot(apariciones,                                    
              las = 2,
              col = rainbow(50),
              ylab = 'Num. Apariciones',
              xlab = 'Palabra',
              cex.names = as.numeric(input$tam_etiquetas))})
    })
    # Caso para cuando se quiere crear nube de palabras.
    # Cuando el usuario selecciona personalmente el archivo.
    observeEvent(input$seleccion_n, {
      # Bibliotecas para mineria de textos y para la nube de palabras.
      library(tm)
      library(wordcloud2)
      # Leyendo el archivo especificado.
      tweets <- read.csv(file=file.choose(), header = T)
      # Creamos la coleccion de documentos, en donde cada uno es un tweet y nos interesa solo el texto.
      corpus <- iconv(tweets$text)
      corpus <- Corpus(VectorSource(corpus))
      # Limpiando el contenido: a minusculas todo, sin signos de puntuacion, nums., quitando URLs
      # y ademas agregando una lista predefinida de stopwords que agregamos a los de siempre.
      corpus <- tm_map(corpus, tolower)
      corpus <- tm_map(corpus, removePunctuation)
      corpus <- tm_map(corpus, removeNumbers)
      removeURL <- function(x) gsub('http[[:alnum:]]*', '', x)
      cleanset <- tm_map(corpus, content_transformer(removeURL))
      stopwords <- read.csv("..\\Data\\stopwords.csv", header = FALSE)
      stopwords <- as.character(stopwords$V1)
      stopwords <- c(stopwords, stopwords())
      cleanset <- tm_map(corpus, removeWords, stopwords)
      # Quitando los multiespacios.
      cleanset <- tm_map(cleanset, stripWhitespace)
      # Creando la matriz de terminos.
      tdm <- TermDocumentMatrix(cleanset)
      tdm <- as.matrix(tdm)
      # Viendo la cantidad de veces que aparecen las palabras.
      apariciones <- rowSums(tdm)
      apariciones <- subset(apariciones, apariciones >= as.numeric(input$min_apariciones_n))
      # Metiendo la informacion a una estructura tabular.
      apariciones <- data.frame(names(apariciones), apariciones)
      # Le pegamos nombres a las columnas.
      colnames(apariciones) <- c('word', 'freq')
      # Rendereamos la nube de palabras.
      output$grafica <- renderPlot({wordcloud2(apariciones, shape = input$forma, size = as.numeric(input$tamanio), minSize = as.numeric(input$tam_chico))})
    })
    # Caso para la nube de palabras.
    # Escendario para usar rutas a los archivos predefinidas.
    observeEvent(input$predefinido_n, {
      # Bivliotecas para la mineria de textos y la nube de palabras.
      library(tm)
      library(wordcloud2)
      # La ruta relativa a los arhivos CSVs se construyen a partir del tema.
      ruta_archivo = ""
      if(input$tema_n == "#AMLO") {
        ruta_archivo = "..\\Data\\amlo.csv"
      } else if(input$tema_n == "#RicardoAnaya") {
        ruta_archivo = "..\\Data\\anaya.csv"
      } else if(input$tema_n == "#Meade") {
        ruta_archivo = "..\\Data\\meade.csv"
      } else if(input$tema_n == "#ElBronco") {
        ruta_archivo = "..\\Data\\bronco.csv"
      } else if(input$tema_n == "#Elecciones2018") {
        ruta_archivo = "..\\Data\\elecciones.csv"
      } else if(input$tema_n == "#INE") {
        ruta_archivo = "..\\Data\\ine.csv"
      }
      # Obteniendo el archivo al leerlo.
      tweets <- read.csv(ruta_archivo, header = T)
      # Creamos el corpus, que es la coleccion de documentos en donde cada uno es un tweet; nos interesa el texto mismo.
      corpus <- iconv(tweets$text)
      corpus <- Corpus(VectorSource(corpus))
      # Limpiando el contenido: a minusculas todo, sin signos de puntuacion, nums., quitando URLs
      # y ademas agregando una lista predefinida de stopwords que agregamos a los de siempre.
      corpus <- tm_map(corpus, tolower)
      corpus <- tm_map(corpus, removePunctuation)
      corpus <- tm_map(corpus, removeNumbers)
      removeURL <- function(x) gsub('http[[:alnum:]]*', '', x)
      cleanset <- tm_map(corpus, content_transformer(removeURL))
      stopwords <- read.csv("..\\Data\\stopwords.csv", header = FALSE)
      stopwords <- as.character(stopwords$V1)
      stopwords <- c(stopwords, stopwords())
      # Dependiendo del tema elegido, es posible descartar las palabras que evidentemente estaran.
      cleanset <- tm_map(corpus, removeWords, stopwords)
      if(input$tema_n == "#AMLO") {
        cleanset <- tm_map(cleanset, removeWords, c('amlo', 'andresmanuel', 'lopezobrador'))
      } else if(input$tema_n == "#RicardoAnaya") {
        cleanset <- tm_map(cleanset, removeWords, c('anaya', 'ricardoanaya', 'ricardoanayac'))
      } else if(input$tema_n == "#Meade") {
        cleanset <- tm_map(cleanset, removeWords, c('meade', 'joseantoniomeade', 'joseantoniomeadek'))
      } else if(input$tema_n == "#ElBronco") {
        cleanset <- tm_map(cleanset, removeWords, c('bronco', 'elbronco', 'jaimerodriguez', 'jaimerodriguezcalderon'))
      } else if(input$tema_n == "#Elecciones2018") {
        cleanset <- tm_map(cleanset, removeWords, c('elecciones', 'eleccionesmexico', 'elecciones2018', 'mexico'))
      } else {
        cleanset <- tm_map(cleanset, removeWords, c('ine', 'inemexico', 'institutoelectoral', 'debate', 'institutonacionalelectoral'))
      }
      # Quitando multi-espacios en blanco.
      cleanset <- tm_map(cleanset, stripWhitespace)
      # Creamos la matriz de terminos.
      tdm <- TermDocumentMatrix(cleanset)
      tdm <- as.matrix(tdm)
      # Contando el num. de veces que aparecen.
      apariciones <- rowSums(tdm)
      # Nos quedamos con aquellas que aparecen mas del numero especificado.
      apariciones <- subset(apariciones, apariciones >= as.numeric(input$min_apariciones_n))
      # Las estructuramos las apariciones en forma tabular por palabra.
      apariciones <- data.frame(names(apariciones), apariciones)
      # Agragando nombres a las columnas.
      colnames(apariciones) <- c('word', 'freq')
      # Rendereamos y mandamos a la salida la nube de palabras formada.
      output$grafica <- renderPlot({wordcloud2(apariciones, shape = input$forma, size = as.numeric(input$tamanio), minSize = as.numeric(input$tam_chico))})
      })
    # Caso para recomendar el numero de clusters al graficar las inercias.
    observeEvent(input$recomendar_c, {
      # Importando las bibliotecas auxiliares.
      library(NLP)       
      library(tm)        
      require(graphics)  
      library(tidyverse)
      # COmo el archivo es predefinido, se construye la ruta a partir del nombre del tema.
      ruta_archivo = ""
      if(input$tema_c == "#AMLO") {
        ruta_archivo = "..\\Data\\amlo.csv"
      } else if(input$tema_c == "#RicardoAnaya") {
        ruta_archivo = "..\\Data\\anaya.csv"
      } else if(input$tema_c == "#Meade") {
        ruta_archivo = "..\\Data\\meade.csv"
      } else if(input$tema_c == "#ElBronco") {
        ruta_archivo = "..\\Data\\bronco.csv"
      } else if(input$tema_c == "#Elecciones2018") {
        ruta_archivo = "..\\Data\\elecciones.csv"
      } else if(input$tema_c== "#INE") {
        ruta_archivo = "..\\Data\\ine.csv"
      }
      # Fijando la semilla de aleatoriedad para la repl. de resultados.
      set.seed(80)
      # Leyendo los tweets a partir de la ruta construida.
      tweets <- read.csv(ruta_archivo, header = T)
      # Creando el corpues que es la col. de documentos en donde cada tweet es visto como un documento.
      corpus <- iconv(tweets$text)
      corpus <- Corpus(VectorSource(corpus))
      #Limpiando los datos.
      corpus <- tm_map(corpus, tolower)
      corpus <- tm_map(corpus, removePunctuation)
      corpus <- tm_map(corpus, removeNumbers)
      removeURL <- function(x) gsub('http[[:alnum:]]*', '', x)
      cleanset <- tm_map(corpus, content_transformer(removeURL))
      stopwords <- read.csv("..\\Data\\stopwords.csv", header = FALSE)
      stopwords <- as.character(stopwords$V1)
      stopwords <- c(stopwords, stopwords())
      cleanset <- tm_map(corpus, removeWords, stopwords)
      # Es posible quitar palabras que evidentemente estaran presentes a partir del tema eledigo (hashtag).
      if(input$tema_t == "#AMLO") {
        cleanset <- tm_map(cleanset, removeWords, c('amlo', 'andresmanuel', 'lopezobrador'))
      } else if(input$tema_t == "#RicardoAnaya") {
        cleanset <- tm_map(cleanset, removeWords, c('anaya', 'ricardoanaya', 'ricardoanayac'))
      } else if(input$tema_t == "#Meade") {
        cleanset <- tm_map(cleanset, removeWords, c('meade', 'joseantoniomeade', 'joseantoniomeadek'))
      } else if(input$tema_t == "#ElBronco") {
        cleanset <- tm_map(cleanset, removeWords, c('bronco', 'elbronco', 'jaimerodriguez', 'jaimerodriguezcalderon'))
      } else if(input$tema_t == "#Elecciones2018") {
        cleanset <- tm_map(cleanset, removeWords, c('elecciones', 'eleccionesmexico', 'elecciones2018', 'mexico'))
      } else {
        cleanset <- tm_map(cleanset, removeWords, c('ine', 'inemexico', 'institutoelectoral', 'debate', 'institutonacionalelectoral'))
      }
      # Quitando los multi-espacios en blanco.
      cleanset <- tm_map(cleanset, stripWhitespace)
      # Crando la matriz de terminos.
      dtm = DocumentTermMatrix(cleanset)
      # Creamos la matriz de distancias entre los terminos.
      distancias = dist(dtm)
      # Vemos la inercia al considerar un solo cluster.
      vector <- kmeans(distancias, centers = 1)$betweens
      # Y evaluamos al itera sobre mas clusters.
      for(i in 2:15) vector[i] <- kmeans(distancias, centers = i)$betweenss
      # Mandamos a la salida el render resultante de graficar las inercias de 1-15.
      output$grafica <- renderPlot({plot(1:15, vector, type = "b", xlab = "num. clusters", ylab = "inercia inter-cluster")})
    })
    # Caso para cuando se quiere recomendar el numero de clusters, pero especificando el archivo.
    observeEvent(input$recomendar_c1, {
      # Importanto las bibliotecas auxiliares.
      library(NLP)       
      library(tm)        
      require(graphics)  
      library(tidyverse)
      # Fijando la semilla de aleatoriedad.
      set.seed(80)
      # Leyendo el archivo, dando la libertad de elegirlo.
      tweets <- read.csv(file=file.choose(), header = T)
      # Crando el corpus de los documentos, en donde cada tweet es uno.
      corpus <- iconv(tweets$text)
      corpus <- Corpus(VectorSource(corpus))
      #Limpiando los datos.
      corpus <- tm_map(corpus, tolower)
      corpus <- tm_map(corpus, removePunctuation)
      corpus <- tm_map(corpus, removeNumbers)
      removeURL <- function(x) gsub('http[[:alnum:]]*', '', x)
      cleanset <- tm_map(corpus, content_transformer(removeURL))
      stopwords <- read.csv("..\\Data\\stopwords.csv", header = FALSE)
      stopwords <- as.character(stopwords$V1)
      stopwords <- c(stopwords, stopwords())
      cleanset <- tm_map(corpus, removeWords, stopwords)
      cleanset <- tm_map(cleanset, stripWhitespace)
      # Crando la matriz de terminos.
      dtm = DocumentTermMatrix(cleanset)
      # Evaluando las distancias entre los tweets.
      distancias = dist(dtm)
      # Nuevamente, evaluamos las inercias al graficarlas desde usar uno hasta quince clusters.
      vector <- kmeans(distancias, centers = 1)$betweens
      for(i in 2:15) vector[i] <- kmeans(distancias, centers = i)$betweenss
      # La grafica resultante que es rendereada la mandamos a la salida.
      output$grafica <- renderPlot({plot(1:15, vector, type = "b", xlab = "num. clusters", ylab = "inercia inter-cluster")})
    })
    # Caso para hacer clustering; usando ruta predefinida para los hashtags (temas).
    observeEvent(input$predefinido_c, {
      # Importando las bibliotecas auxiliares.
      library(NLP)       
      library(tm)        
      require(graphics)  
      library(tidyverse)
      # Se construye la ruta al archivo a partir del tema.
      ruta_archivo = ""
      if(input$tema_c == "#AMLO") {
        ruta_archivo = "..\\Data\\amlo.csv"
      } else if(input$tema_c == "#RicardoAnaya") {
        ruta_archivo = "..\\Data\\anaya.csv"
      } else if(input$tema_c == "#Meade") {
        ruta_archivo = "..\\Data\\meade.csv"
      } else if(input$tema_c == "#ElBronco") {
        ruta_archivo = "..\\Data\\bronco.csv"
      } else if(input$tema_c == "#Elecciones2018") {
        ruta_archivo = "..\\Data\\elecciones.csv"
      } else if(input$tema_c== "#INE") {
        ruta_archivo = "..\\Data\\ine.csv"
      }
      # Fijando la semilla de aleatoriedad.
      set.seed(80)
      # Leyendo el archivo de los tweets en formato CSV a partir de la ruta construida.
      tweets <- read.csv(ruta_archivo, header = T)
      # Creamos el corpus (col. de documentos en donde cada uno es un tweet).
      corpus <- iconv(tweets$text)
      corpus <- Corpus(VectorSource(corpus))
      #Limpiamos con el preprocesamiento de siempre.
      corpus <- tm_map(corpus, tolower)
      corpus <- tm_map(corpus, removePunctuation)
      corpus <- tm_map(corpus, removeNumbers)
      removeURL <- function(x) gsub('http[[:alnum:]]*', '', x)
      cleanset <- tm_map(corpus, content_transformer(removeURL))
      stopwords <- read.csv("..\\Data\\stopwords.csv", header = FALSE)
      stopwords <- as.character(stopwords$V1)
      stopwords <- c(stopwords, stopwords())
      # Podemos en este caso quitar o descartar aquellas palabras que evidentemente seran las que mas aparezcan.
      cleanset <- tm_map(corpus, removeWords, stopwords)
      if(input$tema_t == "#AMLO") {
        cleanset <- tm_map(cleanset, removeWords, c('amlo', 'andresmanuel', 'lopezobrador'))
      } else if(input$tema_t == "#RicardoAnaya") {
        cleanset <- tm_map(cleanset, removeWords, c('anaya', 'ricardoanaya', 'ricardoanayac'))
      } else if(input$tema_t == "#Meade") {
        cleanset <- tm_map(cleanset, removeWords, c('meade', 'joseantoniomeade', 'joseantoniomeadek'))
      } else if(input$tema_t == "#ElBronco") {
        cleanset <- tm_map(cleanset, removeWords, c('bronco', 'elbronco', 'jaimerodriguez', 'jaimerodriguezcalderon'))
      } else if(input$tema_t == "#Elecciones2018") {
        cleanset <- tm_map(cleanset, removeWords, c('elecciones', 'eleccionesmexico', 'elecciones2018', 'mexico'))
      } else {
        cleanset <- tm_map(cleanset, removeWords, c('ine', 'inemexico', 'institutoelectoral', 'debate', 'institutonacionalelectoral'))
      }
      # Quitando los multi-espacios en blanco.
      cleanset <- tm_map(cleanset, stripWhitespace)
      # Creando la matriz de terminos y evaluando las distancias entre ellos.
      dtm = DocumentTermMatrix(cleanset)
      distancias = dist(dtm)
      # Aplicando el algoritmo de k-means con los parametros del usuario.
      resultados <- kmeans(distancias, centers = as.numeric(input$num_clusters), algorithm = input$algoritmo)
      # Rendereamos la categorizacion por clusters y la mandam el resultado a la salida.
      output$grafica <- renderPlot({plot(resultados$cluster, xlab="Tweet", ylab ="cluster", col = resultados$cluster)})
    })
    # Caso para llevar a cabo el custering con la ruta predefinida por el usuario.
    observeEvent(input$seleccion_c, {
      # Importando las bibliotecas auxiliares.
      library(NLP)       
      library(tm)        
      require(graphics)  
      library(tidyverse)
      # Fijando la semilla de aleatoriedad.
      set.seed(80)
      # Leyendo el archivo de los tweets, construyendo el corpus luego.
      tweets <- read.csv(file=file.choose(), header = T)
      corpus <- iconv(tweets$text)
      corpus <- Corpus(VectorSource(corpus))
      # Preprocesando con una limpia el contenido.
      corpus <- tm_map(corpus, tolower)
      corpus <- tm_map(corpus, removePunctuation)
      corpus <- tm_map(corpus, removeNumbers)
      removeURL <- function(x) gsub('http[[:alnum:]]*', '', x)
      cleanset <- tm_map(corpus, content_transformer(removeURL))
      stopwords <- read.csv("..\\Data\\stopwords.csv", header = FALSE)
      stopwords <- as.character(stopwords$V1)
      stopwords <- c(stopwords, stopwords())
      cleanset <- tm_map(corpus, removeWords, stopwords)
      # Quitando los multi-espacios en blanco.
      cleanset <- tm_map(cleanset, stripWhitespace)
      # Crando la matriz de terminos y evaluando las distancias entre ellos.
      dtm = DocumentTermMatrix(cleanset)
      distancias = dist(dtm)
      # Aplicando el algoritmo de k-means con los parametros dados por el usuario.
      resultados <- kmeans(distancias, centers = as.numeric(input$num_clusters), algorithm = input$algoritmo)
      # Finalmente, el resultado del render lo mandamos a la salida.
      output$grafica <- renderPlot({plot(resultados$cluster, xlab="Tweet", ylab ="cluster", col = resultados$cluster)})
    })
  }
)
