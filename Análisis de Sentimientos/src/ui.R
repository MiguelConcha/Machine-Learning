# ---------------------------------------- #
#           INTERFFAZ DE USUARIO           #
# ---------------------------------------- #
shinyUI(
  pageWithSidebar(
    headerPanel("Elecciones 2018"),       
    # El panel que aparece del lado izquierdo.
    sidebarPanel(
      # Permite elegir al usuario lo que quiere realizar.
      selectInput("accion", "Selecciona lo que deseas realizar",
                  choices = c("Obtener datos (ya hay por ahora suficientes)", "Clustering k-means", "Palabras comunes","Nube de palabras","Estudio de sentimientos")),
      # En el caso que quiera bajar tweets (temas predefinidos u otros), parametrizando el num. de tweets y fecha de inicio.
      conditionalPanel(condition = "input.accion == 'Obtener datos (ya hay por ahora suficientes)'",
                       # Seleccionando el tema. 
                       selectInput("hashtag", "Selecciona el hashtag electoral de tu interes",
                                    choices = c("#AMLO", "#RicardoAnaya", '#Meade', '#ElBronco', '#Elecciones2018', '#INE', 'Otro')),
                       # Cuando desea un tema no presenta directamente, se le permite escribir el hashtag. 
                       conditionalPanel(condition = "input.hashtag == 'Otro'",
                                         textInput("otroHashtag", "Escribe el hashtag que te interesa")),
                       # Especificando el num. de tweets a recabar. 
                       sliderInput("numTweets", "Selecciona el numero de tweets a recabar: ",
                                    min = 1000, max = 5000, value = 1000, step = 100),
                       # Desde que fecha considerarlos. 
                       dateInput("fecha", "Fecha desde la cual tomar los tweets:",
                                       "2017-12-14"),
                       # Boton que inicia la accion. 
                       actionButton("bajar_tweets", "Recopilar Tweets", icon("paper-plane"), style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
                        ),
      # En caso de que quiera hacer un an. de los sentimientos (puede elegir ruta predefinida al .csv o elegirlo directamente).
      conditionalPanel(condition = "input.accion == 'Estudio de sentimientos'",
                       # Seleccionando el tema a analizar.
                       selectInput("tema", "Selecciona el hashtag electoral sobre el cual analizar",
                                   choices = c("#AMLO", "#RicardoAnaya", '#Meade', '#ElBronco', '#Elecciones2018', '#INE', 'Otro')),
                       # Diciendo si quire una ruta predefinida o elegirla personalmente.
                       selectInput("ruta", "Tu ruta del archivo",
                                   choices = c("Predefinida por el tema", "Seleccionarla yo mismo")),
                       # Boton para iniciar la accion en caso de indicar la ruta personalmente.
                       conditionalPanel(condition = "input.ruta == 'Seleccionarla yo mismo'",
                                        actionButton("seleccion", "Seleccionar archivo .csv y analizar", style="color: #fff; background-color: #337ab7; border-color: #2e6da4")),
                       # Boton para iniciar la accion en caso de usar la ruta predefinida.
                       conditionalPanel(condition = "input.ruta == 'Predefinida por el tema'",
                                        actionButton("predefinido", "Analizar", style="color: #fff; background-color: #337ab7; border-color: #2e6da4"))),
      # En caso de que el usuario quiera graficar las palabras mas usadas (puede elegir ruta predefinida al .csv o elegirlo directamente).
      conditionalPanel(condition = "input.accion == 'Palabras comunes'",
                       # Seleccionando el tema a analizar.
                       selectInput("tema_t", "Selecciona el hashtag electoral sobre el cual analizar",
                                   choices = c("#AMLO", "#RicardoAnaya", '#Meade', '#ElBronco', '#Elecciones2018', '#INE', 'Otro')),
                       # Diciendo si quire una ruta predefinida o elegirla personalmente.
                       selectInput("ruta_t", "Tu ruta del archivo",
                                   choices = c("Predefinida por el tema", "Seleccionarla yo mismo")),
                       # Min. de apariciones de las palabras a considerar en la nube.
                       sliderInput("min_apariciones", "Selecciona el min. de apariciones a partir del cual considerar",
                                   min = 25, max = 100, value = 30, step = 1),
                       # Dimensiones de las etiquetas de las palabras en la grafica.
                       sliderInput("tam_etiquetas", "Dimensiones de las etiquetas para palabras",
                                   min = 0.1, max = 1, value = 0.25, step = 0.01),
                       # Boton para iniciar la accion en caso de indicar la ruta personalmente.
                       conditionalPanel(condition = "input.ruta_t == 'Seleccionarla yo mismo'",
                                        actionButton("seleccion_t", "Seleccionar archivo .csv y analizar", style="color: #fff; background-color: #337ab7; border-color: #2e6da4")),
                       # Boton para iniciar la accion en caso de usar la ruta predefinida.
                       conditionalPanel(condition = "input.ruta_t == 'Predefinida por el tema' & input.tema_t != 'Otro'",
                                        actionButton("predefinido_t", "Graficar palabras frecuentes", style="color: #fff; background-color: #337ab7; border-color: #2e6da4"))),
      # En caso de que el usuario hacer una nube de palabras (puede elegir ruta predefinida al .csv o elegirlo directamente).
      conditionalPanel(condition = "input.accion == 'Nube de palabras'",
                       selectInput("tema_n", "Selecciona el hashtag electoral sobre el cual analizar",
                                   choices = c("#AMLO", "#RicardoAnaya", '#Meade', '#ElBronco', '#Elecciones2018', '#INE', 'Otro')),
                       # Diciendo si quire una ruta predefinida o elegirla personalmente.
                       selectInput("ruta_n", "Tu ruta del archivo",
                                   choices = c("Predefinida por el tema", "Seleccionarla yo mismo")),
                       # El min. de apariciones a considerar para poder estar en la nube.
                       sliderInput("min_apariciones_n", "Selecciona el min. de apariciones a partir del cual considerar",
                                   min = 25, max = 100, value = 30, step = 1),
                       # Forma de la nube de palabras.
                       selectInput("forma", "Forma de la nube",
                                   choices = c('circle', 'triangle', 'star')),
                       # Tam. de la nube.
                       sliderInput("tamanio", "Dimensiones de la nube (0.1-1)",
                                   min = 0.1, max = 1, value = 0.3, step = .1),
                       # Tam. mas chico para las palabras.
                       sliderInput("tam_chico", "Selecciona el min. de dimensiones para las palabras (0.1-2)",
                                   min = .1, max = 2, value = 1, step = .1),
                       # Boton para iniciar la accion en caso de indicar la ruta personalmente.
                       conditionalPanel(condition = "input.ruta_n == 'Seleccionarla yo mismo'",
                                        actionButton("seleccion_n", "Seleccionar archivo .csv y generar nube", style="color: #fff; background-color: #337ab7; border-color: #2e6da4")),
                       # Boton para iniciar la accion en caso de usar la ruta predefinida.
                       conditionalPanel(condition = "input.ruta_n == 'Predefinida por el tema' & input.tema_n != 'Otro'",
                                        actionButton("predefinido_n", "Generar nube de palabras", style="color: #fff; background-color: #337ab7; border-color: #2e6da4"))),
      # En caso de que el usuario quiera hacer clustering de los tweets del archivo seleccionedo (directa o indirectamente).
      # De igual forma, se ofrece un boton para poder graficar las inercias de los clusters y tener una idea de cuantos usar.
      conditionalPanel(condition = "input.accion == 'Clustering k-means'",
                       # Seleccionando el tema a analizar.
                       selectInput("tema_c", "Selecciona el hashtag electoral para trabajar",
                                   choices = c("#AMLO", "#RicardoAnaya", '#Meade', '#ElBronco', '#Elecciones2018', '#INE', 'Otro')),
                       # Seleccionando el num. de clusters.
                       sliderInput("num_clusters", "Selecciona el num. de clusters",
                                   min = 1, max = 20, value = 8, step = 1),
                       # Seleccionar el sub-algoritmo de k-means clustering.
                       selectInput("algoritmo", "Selecciona el algoritmo de k-means",
                                   choices = c("Hartigan-Wong", "Lloyd", 'Forgy', 'MacQueen')),
                       # Seleccionando si quiere ruta de archivo predefinida o no.
                       selectInput("ruta_c", "Tu ruta del archivo",
                                   choices = c("Predefinida por el tema", "Seleccionarla yo mismo")),
                       # Caso para eleccion personal de la ruta. Hay un boton para iniciar el clustering y otro para graficar las inercias.
                       conditionalPanel(condition = "input.ruta_c == 'Seleccionarla yo mismo'",
                                        actionButton("recomendar_c1", "Seleccionar archivo y graficar inercias", style="color: #fff; background-color: #337ab7; border-color: #2e6da4"),
                                        actionButton("seleccion_c", "Seleccionar archivo e iniciar", style="color: #fff; background-color: #337ab7; border-color: #2e6da4")),
                       # Caso para eleccion predefinida de la ruta. Hay un boton para iniciar el clustering y otro para graficar las inercias.
                       conditionalPanel(condition = "input.ruta_c == 'Predefinida por el tema' & input.tema_c != 'Otro'",
                                        actionButton("recomendar_c", "Graficar inercias", style="color: #fff; background-color: #337ab7; border-color: #2e6da4"),
                                        actionButton("predefinido_c", "Iniciar clustering", style="color: #fff; background-color: #337ab7; border-color: #2e6da4")))
    ),
    # Graficando los resultados en la parte lateral derecha.
    mainPanel(
      plotOutput("grafica")
    )
  )
)
