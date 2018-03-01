/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package clasificadordedocumentos;

import java.io.File;
import java.io.FileNotFoundException;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
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

    /** Obtenemos el filtrado de palabras del path al archivo utiluzando las banderas enviadas.
        @param filepath path al archivo. El archivo debe ser con extensión .arff
          y con los atributos texto(String), calificación(nominal{0,1}),
        @param lowercase bandera para que todas las palabras estén en lowercase.
        @param frequency bandera para que se tome la frecuencia de las palabras
          en el archivo.
        @param useStemmer bandera para que use un el Stemmer.
        @param stopwords bandera para que use los stopwords.
        @param idftT bandera para que utilice el IDFT Transform
        @param wordsToKeep numero de palabras a retener.
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
    
    public static void applyNaiveBayes(Instances dataset) {
        NaiveBayes nb = new NaiveBayes();
        int folds = 1;
        try {
            Evaluation eval = new Evaluation(dataset);
            eval.crossValidateModel(nb, dataset, folds, new Random(0));
            System.out.println(eval.toSummaryString());
        } catch (Exception e) {
            System.out.println(e);
        }
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        String filepath = "/Users/edervs/Documents/fciencias/semestre_6/ML/Machine-Learning/Clasificación de Documentos/ClasificadorDeDocumentos/src/clasificadordedocumentos/test1.arff";
        boolean lowercase = true;
        boolean frequency = false;
        boolean useStemmer = false;
        String stopwordsFile = "/Users/edervs/Documents/fciencias/semestre_6/ML/Machine-Learning/Clasificación de Documentos/ClasificadorDeDocumentos/src/clasificadordedocumentos/stopwords.txt";
        boolean idftT = false;
        int wordsToKeep = 1000;
        String delimiters = ".,;:'\"\\()!?-_	 +@&#$¬/";
        
        Instances filtered = filter(
            filepath, lowercase, frequency, useStemmer, stopwordsFile, idftT, wordsToKeep, delimiters
        );
        
        applyNaiveBayes(filtered);
    }
    
}
