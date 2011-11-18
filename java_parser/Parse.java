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


class Parse {


	  static boolean DEBUG = false ; //
	  static String curr_parser = "englishFactored.ser.gz";
	  static String backup_parser = "englishPCFG.ser.gz";
	  static String out_prefix =".parsed";
	  //static String input_dir_path = "/home/vishayv/nlp_ee_project/terr/developset/test_dir";
	  static String input_dir_path = "/home/vishayv/nlp_ee_project/terr/developset/test_set/pptexts";
	  //static String out_dir_path = "/home/vishayv/nlp_ee_project/terr/developset/test_dir_parsed/";
	  static String out_dir_path = "/home/vishayv/nlp_ee_project/terr/developset/test_set/texts_parsed/";
	  static File dir ; 
	  public static void createOutDir(){

			  // CREAT DIRECTORY
		      File file = new File(out_dir_path);
			  if(file.exists()){
				  return ;
			  }	  
			  boolean success = file.mkdir();
					if (!success) {
						    // Directory creation failedi
							System.out.println("Directory creation failed");
							System.exit(1);
					}

	  }
	  public static File[] applyFileFilter(File files[]){ // everything is passed by reference in java

			  FileFilter fileFilter = new FileFilter() {
				      public boolean accept(File file) {
						          return !file.isDirectory();
								      }
			  };
			  files = dir.listFiles(fileFilter);
			  return files ; // have to return because we are changing the place the reference points too
	  }	  
	  public static File[] getFiles(){

			  //dir = new File(input_dir_path);
			  File[] files = dir.listFiles();
			  if(files == null){
					  System.out.println("Illegal Directory .Exiting");
					  System.exit(1);

			  }	  
			  files = applyFileFilter(files);
			  return files;  
	  }	  
	  public static void main(String[] args) throws IOException {

			  dir = new File(input_dir_path);
			  createOutDir() ;

		      LexicalizedParser lp = new LexicalizedParser(curr_parser);
			  LexicalizedParser lp_backup ; 
			  lp.setOptionFlags("-MAX_ITEMS","700000","-maxLength", "80", "-retainTmpSubcategories");
			  TreebankLanguagePack tlp = new PennTreebankLanguagePack();
			  GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();

			  // search for files in the directory
			  File [] files = getFiles();
		  	  // READ FILES 
			  for(File file : files	){
			  		String file_abs_path = file.getAbsolutePath();
					String filename  = file.getName();	
					String file_path = file.getPath();
			    	String new_abs_path = out_dir_path+filename + out_prefix ;
					// open file handle for writing 
					System.out.println("processing file "+file_path);
					if(DEBUG){
						System.out.println("processing file "+file_path);
						System.out.println("processing filename "+filename);
						System.out.println("processing filepath "+file_path);
						System.out.println("output abs path "+new_abs_path);
					}
					if(filename.startsWith(".")){
						  if(DEBUG){
						  	System.out.println("skipping  processing for file "+filename);
						  }
						  continue ;
					}	  
					if (filename.startsWith("meta")){
						  if(DEBUG){
						  	System.out.println("skipping  processing for file "+filename);
						  }
						  continue ;
					}
					PrintWriter out = new PrintWriter(new FileWriter(new_abs_path));
			  	  	Iterable< List<? extends HasWord> > sentences;
			  		DocumentPreprocessor dp = new DocumentPreprocessor(file_abs_path);
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
						if(depth == 2){
								//parse = null ;
								lp = null ;
		      				    lp_backup = new LexicalizedParser(backup_parser);
			  					lp_backup.setOptionFlags("-MAX_ITEMS","700000","-maxLength", "80", "-retainTmpSubcategories");
								parse = lp_backup.apply(sentence);
    							//out.write(parse.pennString());
								lp_backup = null ;
								lp = new LexicalizedParser(curr_parser);
			  					lp.setOptionFlags("-MAX_ITEMS","700000","-maxLength", "80", "-retainTmpSubcategories");
								// now extract info from backup
						}	
						TreePrint tp = new TreePrint("wordsAndTags,oneline,typedDependenciesCollapsed");
						tp.setPrintWriter(out);
			      		tp.printTree(parse);
						out.write("*************\n");

					}
    				out.close();
				}


				  
  }

}

