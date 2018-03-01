/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package clasificadordedocumentos;

import java.util.ArrayList;
import java.util.Scanner;
import java.util.InputMismatchException;
import java.io.File;
import java.io.FileNotFoundException;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.trees.J48;
import weka.core.Instance;
//import required classes
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.core.stemmers.LovinsStemmer;
import weka.core.stopwords.*;
import weka.classifiers.meta.FilteredClassifier;
import weka.classifiers.trees.J48;
import weka.core.Debug.Random;
import weka.core.stemmers.SnowballStemmer;
import weka.core.tokenizers.*;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;
import weka.filters.unsupervised.attribute.StringToWordVector;
/**
 *
 * @author edervs, ximenalh, miguelcv, leonardohc
 */
public class ClasificadorDeDocumentos {

    /** Obtenemos el filtrado de palabras del path al archivo utilizando las banderas enviadas.
        @param filepath path al archivo. El archivo debe ser con extensión .arff
          y con los atributos texto(String), calificación(nominal{0,1}),
        @param lowercase Bandera para que todas las palabras estén en lowercase.
        @param frequency Bandera para que se tome la frecuencia de las palabras
          en el archivo.
        @param useStemmer Bandera para que use el Snowball Stemmer.
        @param stopwords Stopwords a utilizar.
        @param idftT Bandera para que utilice el IDFT Transform
        @param wordsToKeep Número de palabras a retener.
        @param delimiters String que contiene los delimitadores a usar
    */
    public static Instances filter (String filepath, boolean lowercase, boolean frequency,
        boolean useStemmer, String stopwords, boolean idftT, int wordsToKeep, String delimiters) {
        
        StringToWordVector filter = new StringToWordVector();
        DataSource source;
        Instances dataset = null;
        Instances fileFiltered = null;
        
        try {
            source = new DataSource(filepath);
            dataset = source.getDataSet();
            // Asignar el índice de la clase a el el último atributo
            dataset.setClassIndex(dataset.numAttributes()-1);

            // Filtrado de archivo
            filter.setIDFTransform(idftT);
            filter.setTFTransform(false);
            filter.setAttributeIndices("first-last");
            filter.setDoNotCheckCapabilities(false);
            filter.setDoNotOperateOnPerClassBasis(false);
            filter.setInvertSelection(false);
            filter.setSaveDictionaryInBinaryForm(false);
            
            filter.setInputFormat(dataset);
            filter.setWordsToKeep(wordsToKeep);
            if (useStemmer) {
                SnowballStemmer stemmer = new SnowballStemmer();
                filter.setStemmer(stemmer);
            }
            filter.setLowerCaseTokens(lowercase);
            filter.setOutputWordCounts(frequency);
            
            // Delimitadores
            WordTokenizer tokenizer = new WordTokenizer();
            tokenizer.setDelimiters(delimiters);
            filter.setTokenizer(tokenizer);
            
            // Stopwords
            if (!stopwords.isEmpty()){
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
            
            // Aplicamos el filtrado.
            fileFiltered = Filter.useFilter(dataset, filter);
            
        } catch (Exception e) {
            System.out.println(e);
        }
        
        return fileFiltered;
        //return filter.getOutputFormat();
    }
        
    /**
     * Dividiendo el conjunto de ejemplos en Entrenamiento y Prueba
     * a partir del porcentaje de entrenamiento dado como argumento.
     * @param inst La instancia de ejemplos.
     * @param trainPerfectage El porcentaje de entrenamiento.
     * @return Un arreglo con los dos conjuntos: el de entrenamiento y de prueba.
     */
    public static Instances[] splitDataSet(Instances inst, double trainPerfectage) {
        int trainSize = (int) Math.round(inst.numInstances() * trainPerfectage / 100); 
        int testSize = inst.numInstances() - trainSize; 
        Instances train = new Instances(inst, 0, trainSize); 
        Instances test = new Instances(inst, trainSize, testSize); 
        Instances[] split = new Instances[2];
        split[0] = train;
        split[1] = test;
        return split;
    }
    
    public static void applyJ48(Instances dataset, boolean prunning, double confidenceFactor, int numFolds, double trainPercentage) {
        try{
        J48 tree = new J48();
        ArrayList<String> options = new ArrayList<>();
        if(!prunning)
            options.add("-U");
        options.add("-C " + String.valueOf(confidenceFactor));
        options.add("-N " + Integer.toString(numFolds));
        tree.setOptions(options.toArray(new String[options.size()]));
        Instances[] splitSet = splitDataSet(dataset, trainPercentage);
        Evaluation eval = new Evaluation(splitSet[0]);
        eval.evaluateModel(tree, splitSet[1]);
	System.out.println(eval.toSummaryString("\nSummary\n======\n", false));
	System.out.println(eval.toClassDetailsString("\nClass Details\n======\n"));
	System.out.println(eval.toMatrixString("\nConfusion Matrix: false positives and false negatives\n======\n"));			
        } catch(Exception e) {
            System.out.println("Ocurrió un problema.");
        }
    }
    
    public static void applyNaiveBayes(Instances dataset, int numFolds, double trainPercentage) {
        NaiveBayes nb = new NaiveBayes();
        int folds = numFolds;
        try {
            Instances[] splitSet = splitDataSet(dataset, trainPercentage);
            Evaluation eval = new Evaluation(splitSet[0]);
            eval.evaluateModel(nb, splitSet[1]);
            System.out.println(eval.toSummaryString());
        } catch (Exception e) {
            System.out.println(e);
        }
    }
    
    /**
     * @param args Los argumentos de línea de comandos.
     */
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        try {
            System.out.print("Ruta al archivo con extensión <<.arff>> a clasificar: ");
            String filepath = s.nextLine();
            
            System.out.println("Transformar todo a minúsculas (Sí o No): ");
            boolean lowercase;
            String lc = s.nextLine();
            lowercase = (lc.equals("Sí") || lc.equals("Si")) ? true : false;
            
            System.out.println("Usar frecuencias (Sí o No): ");
            boolean frequency;
            String fq = s.nextLine();
            frequency = (fq.equals("Sí") || fq.equals("Si")) ? true : false;
            
            System.out.println("Usar el Snowball Stemmer (Sí o No): ");
            boolean useStemmer;
            String st = s.nextLine();
            useStemmer = (st.equals("Sí") || st.equals("Si")) ? true : false;
            
            System.out.print("Ruta al archivo de Stopwords (puede ser un archivo vacío): ");
            String stopWordsFile = s.nextLine();
            
            System.out.println("Usar relevancia de palabra en el documento (Sí o No): ");
            boolean idfT;
            String id = s.nextLine();
            idfT = (id.equals("Sí") || id.equals("Si")) ? true : false;
            
            System.out.println("Número de palabras a conservar: ");
            int wordsToKeep = s.nextInt();
            
            System.out.println("Delimitadores para el filtro: ");
            String delimiters = s.nextLine();
            
            //Construir el filtro:
                    Instances filtered = filter(
                filepath, lowercase, frequency, useStemmer, stopWordsFile, idfT, wordsToKeep, delimiters
             );
            
            //Decisiones y configuración de los algoritmos de clasificación (J48 y Naive Bayes):
            System.out.println("Correr J48 (Sí o No): ");
            boolean j = (s.nextLine().equals("Sí") || s.nextLine().equals("Si")) ? true : false;
            
            System.out.println("Correr Naive Bayes (Sí o No): ");
            boolean bayes = (s.nextLine().equals("Sí") || s.nextLine().equals("Si")) ? true : false;
            
            if(j) {
                System.out.println("CONFIGURACIÓN DEL J48:\n");
                
                System.out.println("Usar poda (Sí o No): ");
                boolean poda = (s.nextLine().equals("Sí") || s.nextLine().equals("Si")) ? true : false;
                
                System.out.println("Confidence Factor: ");
                int cf = s.nextInt();
                
                System.out.println("Porntaje de entranamiento (0 - 100): ");
                double per = s.nextDouble();
                    
                applyJ48(filtered, poda, cf, 2, per);
            }
            
            System.out.println("#####################################");
         
            if(bayes) {
                System.out.println("CONFIGURACIÓN DE BAYES INGENUO:\n");
                   
                System.out.println("Porntaje de entranamiento (0 - 100): ");
                double perb = s.nextDouble();
                
                applyNaiveBayes(filtered, 1, perb);

            }
            
        } catch (InputMismatchException e) {
            System.out.println("Introduciste erróneamente el dato requerido.");
        } 

        //String filepath = "/Users/edervs/Documents/fciencias/semestre_6/ML/Machine-Learning/Clasificación de Documentos/ClasificadorDeDocumentos/src/clasificadordedocumentos/test1.arff";
        //boolean lowercase = true;
        //boolean frequency = false;
        //boolean useStemmer = false;
        //String stopwordsFile = "/Users/edervs/Documents/fciencias/semestre_6/ML/Machine-Learning/Clasificación de Documentos/ClasificadorDeDocumentos/src/clasificadordedocumentos/stopwords.txt";
        //boolean idftT = false;
        //int wordsToKeep = 1000;
        //String delimiters = ".,;:'\"\\()!?-_	 +@&#$¬/";
        
    }
    
}
