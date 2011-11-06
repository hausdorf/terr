import java.io.IOException;
import java.io.StringReader;
import java.io.File ;
import java.io.FilenameFilter;
import java.io.FileFilter;
import java.io.BufferedWriter;
import java.io.PrintWriter;
import java.io.FileWriter;
import java.util.*;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Word;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;


class ParseFast {


	  static boolean DEBUG = false ; //
	  static String curr_parser = "englishPCFG.ser.gz";
	  static String out_prefix =".parsed";
	  //static String input_dir_path = "/home/vishayv/nlp_ee_project/terr/developset/test_dir";
	  //static String input_dir_path = "/home/vishayv/nlp_ee_project/terr/irrel-texts/texts";
	  static String input_file = "text.txt";
	  //static String out_dir_path = "/home/vishayv/nlp_ee_project/terr/developset/test_dir_parsed/";
	  static String out_file = "text_out.txt";

	  public static void main(String[] args) throws IOException {


		    LexicalizedParser lp = new LexicalizedParser(curr_parser);
		  	LexicalizedParser lp_backup ; 
		  	lp.setOptionFlags("-MAX_ITEMS","700000","-maxLength", "80", "-retainTmpSubcategories");
		  	TreebankLanguagePack tlp = new PennTreebankLanguagePack();
		  	GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();

		    // open file handle for writing 
			PrintWriter out = new PrintWriter(new FileWriter(out_file));
			Iterable< List<? extends HasWord> > sentences;
			DocumentPreprocessor dp = new DocumentPreprocessor(input_file);
			List<List<? extends HasWord>> tmp = new ArrayList<List<? extends HasWord>>();
			for (List<HasWord> sentence : dp) {
				tmp.add(sentence);
			}
			sentences = tmp;
			for (List<? extends HasWord> sentence : sentences) {
				if(DEBUG){
					System.out.println("Processing sentence "+sentence);
				}
				Tree parse = lp.apply(sentence);
				int depth = parse.depth();

				if(DEBUG){
					System.out.println("depth of tree"+depth);
				}
				TreePrint tp = new TreePrint("wordsAndTags,oneline,typedDependenciesCollapsed");
				tp.setPrintWriter(out);
				tp.printTree(parse);
				out.write("*************\n");

			}
			out.close();


				  
  }

}

