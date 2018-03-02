
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
     * @param filter
     * @return 
     */
    public static StringToWordVector configureFilter(StringToWordVector filter, boolean lowercase, boolean frequency, 
                                         String stopwords, boolean idtfT, int wordsToKeep,
                                         String delimiters) {
            filter.setIDFTransform(idtfT);
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
            tokenizer.setDelimiters(delimiters);
            filter.setTokenizer(tokenizer);
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
        return filter;
    }
    
    /**
     * Se ejecuta el algoritmo J48 basado en el C4.5 para crear el árbol de decisión.
     * @param args 
     */
     public static void applyJ48(String testing_file, String training_file, boolean lowercase, 
                                boolean frequency, String stopwords, boolean idtfT, int wordsToKeep,
                                String delimiters, boolean pruning, double confidenceFactor) {
        try{
            StringToWordVector filter = new StringToWordVector();
            J48 tree = new J48();
            ArrayList<String> options = new ArrayList<>();
            if(!pruning)
                options.add("-U");
            tree.setOptions(options.toArray(new String[options.size()]));
            filter = configureFilter(filter, lowercase, frequency, stopwords, idtfT, wordsToKeep, delimiters);
            //training data
            Instances train = new Instances(new BufferedReader(new FileReader(training_file)));
            int lastIndex = train.numAttributes() - 1;
            train.setClassIndex(lastIndex);
            filter.setInputFormat(train);
            train = Filter.useFilter(train, filter);
            //testing data
            Instances test = new Instances(new BufferedReader(new FileReader(testing_file)));
            test.setClassIndex(lastIndex);
            filter.setInputFormat(test);
            test = Filter.useFilter(test, filter);
            tree.buildClassifier(train);
            Evaluation eval = new Evaluation(train);
            eval.evaluateModel(tree,test);
            System.out.println(eval.toSummaryString("\nSummary\n======\n", false));
            System.out.println(eval.toClassDetailsString("\nClass Details\n======\n"));
            System.out.println(eval.toMatrixString("\nConfusion Matrix: false positives and false negatives\n======\n"));	
        } catch(Exception e){
            System.out.println(e);
        }
    }
     
     /**
     * Se ejecuta el algoritmo Naive Bayes.
     * @param args 
     */
     public static void applyNB(String testing_file, String training_file) {
        try{
            StringToWordVector filter = new StringToWordVector();
            NaiveBayes naive = new NaiveBayes();
            //training data
            Instances train = new Instances(new BufferedReader(new FileReader(training_file)));
            int lastIndex = train.numAttributes() - 1;
            train.setClassIndex(lastIndex);
            filter.setInputFormat(train);
            train = Filter.useFilter(train, filter);
            //testing data
            Instances test = new Instances(new BufferedReader(new FileReader(testing_file)));
            test.setClassIndex(lastIndex);
            filter.setInputFormat(test);
            test = Filter.useFilter(test, filter);
            naive.buildClassifier(train);
            Evaluation eval = new Evaluation(train);
            eval.evaluateModel(naive,test);
            System.out.println(eval.toSummaryString());
        } catch(Exception e){
            System.out.println(e);
        }
    }

    public static void main(String[] args) {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        try{
            System.out.print("Ruta al archivo con extensión <<.arff>> de entrenamiento: ");
            String training_file = reader.readLine();
            System.out.print("Ruta al archivo con extensión <<.arff>> de prueba: ");
            String test_file = reader.readLine();
            System.out.println("Algoritmo a utilizar:\n[1] J48\n[2] Bayes Ingenuo");
            int tipoAlgoritmo = Integer.parseInt(reader.readLine());
            if(tipoAlgoritmo == 1) {
                System.out.println("J48:\n");
                ///
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
                System.out.print("Delimitadores para el filtro: ");
                String delimiters = reader.readLine();
                System.out.println("Usar poda (Sí o No): ");
                boolean poda = (reader.readLine().equals("Sí") || reader.readLine().equals("Si")) ? true : false;
                System.out.println("Confidence Factor: ");
                double cf = Double.parseDouble(reader.readLine());
                applyJ48(training_file, test_file, lowercase, frequency, stopWordsFile, idfT, wordsToKeep, delimiters, poda, cf);
                ///
            } 
            else {
                System.out.println("Naive Bayes:\n");
                applyNB(training_file, test_file);
            }
        } catch(Exception e) {
            System.out.println(e);
        }
    }
    
}
