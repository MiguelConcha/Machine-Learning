
package proyecto1;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.core.Instances;
import weka.core.stemmers.SnowballStemmer;
import weka.core.stopwords.WordsFromFile;
import weka.core.tokenizers.WordTokenizer;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.StringToWordVector;
import weka.classifiers.trees.J48;


public class Proyecto1 {

    /**
     * Se configura un filtro con los argumentos dados.
     * @param filter El filtro que será configurado.
     * @param lowercase Si se consideran o no iguales las minúsuculas y mayúsculas.
     * @param frequency Booleano para saber si tomamos en cuanta la frecuencia.
     * @param stopwords Un string que se refiere a la ruta del archivo de stopwords en caso 
     * de quererlo.
     * @boolean idtfT Booleano para saber si consideramos la importancia de cada palabra en el texto
     * a partir de una ponderación de las veces que aparece y el número total de instancias.
     * @boolean wordsToKeep El número de palabras con el que nos quedaremos.
     * @return El filtro configurado con los argumentos dados.
     */
    public static StringToWordVector configureFilter(StringToWordVector filter, boolean lowercase, boolean frequency, 
                                         String stopwords, boolean idtfT, int wordsToKeep) {
            filter.setIDFTransform(idtfT);                            //Colocamos la congfiguración en el filtro pasado como argumento.
            filter.setTFTransform(false);
            filter.setAttributeIndices("first-last");
            filter.setDoNotCheckCapabilities(false);
            filter.setDoNotOperateOnPerClassBasis(false);
            filter.setInvertSelection(false);
            filter.setSaveDictionaryInBinaryForm(false);
            filter.setWordsToKeep(wordsToKeep);
            filter.setLowerCaseTokens(lowercase);
            filter.setOutputWordCounts(frequency);
            WordTokenizer tokenizer = new WordTokenizer();
            tokenizer.setDelimiters(".,;:'\"\\()!?-_	 +@&#$¬/");   //El tokenizador será fijo para evitar problemas.
            filter.setTokenizer(tokenizer);                           //En caso de existir el archivo de stopwords:
            if (!stopwords.isEmpty()){                                //Lo tratamos de arbir y lo asociamos al filtro.          
                try {
                    File stopwordsFile = new File(stopwords);
                    WordsFromFile handler = new WordsFromFile();
                    handler.setStopwords(stopwordsFile);
                    filter.setStopwordsHandler(handler);
                } catch (Exception e) {
                    System.out.println(e);
                    System.out.println("No se encontro el archivo de stop words");
                }
            }
        return filter;                                                //Se devuelve el filtro ya configurado.
    }
    
    /**
     * Se ejecuta J48 o Naive Bayes.
     * A partir de los argumentos dados es que se configrua con el otro método el filtro
     * de tipo StringToWordsVector que es creado aquí. Luego, se parte el conjunto en el porcentaje dado,
     * se hace la prueba y se evalúa el modelo comparando con los otros resultados,
     * @param J48 True si usaremos este árbol de decisión y false para usar bayes ingenuo.
     * @param file El String que se refiere a la ruta en donde tenemos el archivo .arff con los ejemplares a
     * clasificar.
     * @param lowercase Nos dice si queremos que tome igual mayúsuculas que minúsculas.
     * @param frequency Booleano para saber si tomamos en cuanta la frecuencia.
     * @param stopwords Un string que se refiere a la ruta del archivo de stopwords en caso 
     * de quererlo.
     * @boolean idtfT Booleano para saber si consideramos la importancia de cada palabra en el texto
     * a partir de una ponderación de las veces que aparece y el número total de instancias.
     * @boolean wordsToKeep El número de palabras con el que nos quedaremos.
     * @boolean pruning True si queremos usar poda o false en otro caso.
     * @boolean El factor del árbol.
     * @double percentageSplit El porcentaje en que dividiremos al conjunto de ejemplares en prueba y entrenamiento.
     */
     public static void applyAlgorithm(boolean J48, String file, boolean lowercase, 
                                boolean frequency, String stopwords, boolean idtfT, int wordsToKeep, boolean pruning, float confidenceFactor, double percentageSplit) {
        try{
            StringToWordVector filter = new StringToWordVector();       //Creando el filtro y las intancias de los algoritmos e inicializando.
            J48 tree = new J48();                               
            NaiveBayes naive = new NaiveBayes();
            if(J48){                                                    //Caso para J48:                    
                ArrayList<String> options = new ArrayList<>();
                if(!pruning)
                    options.add("-U");                                  //Opción para hacer poda.
                tree.setConfidenceFactor(confidenceFactor);             //Establecemos el confidence factor.
                tree.setMinNumObj(2);
                tree.setOptions(options.toArray(new String[options.size()]));  //Configurando el algoritmo con las opciones.
            }
            filter = configureFilter(filter, lowercase, frequency, stopwords, idtfT, wordsToKeep); //Se personaliza el filtro.
            // Datos de entrenamiento.
            Instances train = new Instances(new BufferedReader(new FileReader(file)));
            int lastIndex = train.numAttributes() - 1;
            train.setClassIndex(lastIndex);                                           //Estableciendo la clase objetivo (la última).
            filter.setInputFormat(train);
            train = Filter.useFilter(train, filter);                                  //Usando el filtro en la instancia.
            //Datos de prueba.
            train.randomize(new java.util.Random(0));
            int trainSize = (int) Math.round(train.numInstances() * percentageSplit);  //Sacando la cantidad en que debemos partir el conjunto.
            int testSize = train.numInstances() - trainSize;
            Instances uno = new Instances(train, 0, trainSize);                        //Dividiendo los ejemplares.
            Instances dos = new Instances(train, trainSize, testSize);
            if(J48) tree.buildClassifier(uno);                                         //Creamos el clasificador para el algoritmo según sea el caso.
            else naive.buildClassifier(uno);
            Evaluation eval = new Evaluation(uno);
            if(J48){
                eval.evaluateModel(tree,dos);                                          //Evaluamos el modelo con el conjunto de prueba.
                System.out.println(eval.toSummaryString("\nSummary\n======\n", false));
                System.out.println(eval.toClassDetailsString("\nClass Details\n======\n"));
                System.out.println(eval.toMatrixString("\nConfusion Matrix: false positives and false negatives\n======\n"));	
            } 
            else{
                eval.evaluateModel(naive,dos);
                System.out.println(eval.toSummaryString());
            }
        } catch(Exception e){
            System.out.println(e);
        }
    }
    
     /**
      * Se solicita poco a poco al usuario la configuración del algoritmo.
      * @param args Los argumentos de línea de comandos.
      */
    public static void main(String[] args) {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        try{
            System.out.print("Ruta al archivo con extensión <<.arff>>: ");
            String file = reader.readLine();
            System.out.println("Crearemos el filtro (StringToWordsVector personalizado)");
            System.out.println("Algoritmo a utilizar:\n[1] J48\n[2] Bayes Ingenuo");
            int tipoAlgoritmo = Integer.parseInt(reader.readLine());
            System.out.print("Transformar todo a minúsculas (Sí o No): ");
            boolean lowercase;
            String lc = reader.readLine();
            lowercase = (lc.equals("Sí") || lc.equals("Si")) ? true : false;
            System.out.print("Usar frecuencias (Sí o No): ");
            boolean frequency;
            String fq = reader.readLine();
            frequency = (fq.equals("Sí") || fq.equals("Si")) ? true : false;
            System.out.print("Ruta al archivo de Stopwords (puede ser un archivo vacío): ");
            String stopWordsFile =reader.readLine();
            System.out.print("Usar relevancia de palabra en el documento (Sí o No): ");
            boolean idfT;
            String id = reader.readLine();
            idfT = (id.equals("Sí") || id.equals("Si")) ? true : false;
            System.out.print("Número de palabras a conservar: ");
            int wordsToKeep = Integer.parseInt(reader.readLine());
            if(tipoAlgoritmo == 1) {
                System.out.println("J48:\n");
                System.out.println("Usar poda (Sí o No): ");
                boolean poda = (reader.readLine().equals("Sí") || reader.readLine().equals("Si")) ? true : false;
                System.out.println("Confidence Factor: ");
                float cf = Float.parseFloat(reader.readLine());
                System.out.println("Porcentaje de Split del conjunto (0.0 - 1.00): ");
                double porcentaje = Double.parseDouble(reader.readLine());
                applyAlgorithm(true, file, lowercase, frequency, stopWordsFile, idfT, wordsToKeep, poda, cf, porcentaje);
            } 
            else {
                System.out.println("Naive Bayes:\n");
                System.out.println("Porcentaje de Split del conjunto (0.0 - 1.00): ");
                double porcentaje = Double.parseDouble(reader.readLine());
                applyAlgorithm(false,file, lowercase, frequency, stopWordsFile, idfT, wordsToKeep, false, 0.00f, porcentaje);
            }
        } catch(Exception e) {
            System.out.println(e);
        }
    }
    
}
