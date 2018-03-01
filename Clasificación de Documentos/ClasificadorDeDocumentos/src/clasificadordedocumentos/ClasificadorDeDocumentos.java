/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package clasificadordedocumentos;

import java.io.File;
import java.io.FileNotFoundException;
import weka.core.Instance;
//import required classes
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.core.stemmers.LovinsStemmer;
import weka.core.stopwords.*;
import weka.classifiers.meta.FilteredClassifier;
import weka.classifiers.trees.J48;
import weka.core.stemmers.SnowballStemmer;
import weka.core.tokenizers.*;
import weka.filters.unsupervised.attribute.Remove;
import weka.filters.unsupervised.attribute.StringToWordVector;
/**
 *
 * @author edervs
 */
public class ClasificadorDeDocumentos {

    public StringToWordVector filter (String filepath, boolean lowercase, boolean frequency,
        boolean useStemmer, String stopwords, boolean idftT, int wordsToKeep, String delimiters) {
        StringToWordVector filter = new StringToWordVector();
        try {
            DataSource source = new DataSource(filepath);
            Instances dataset = source.getDataSet();
            //set class index to the last attribute
            dataset.setClassIndex(dataset.numAttributes()-1);

            // Filtrado de archivo
            filter.setInputFormat(dataset);
            filter.setIDFTransform(idftT);
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
                    System.out.print("No se encontro el archivo de stop words");
                }
            }
        } catch (Exception e) {
            System.out.println("No se encontró el archivo");
        }
        return filter;
    }
    
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
    }
    
}
