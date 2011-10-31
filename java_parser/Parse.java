import java.io.IOException;
import java.io.StringReader;
import java.io.File ;
import java.io.FilenameFilter;
import java.io.FileFilter;
import java.io.BufferedWriter;
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


	  static String curr_parser = "englishFactored.ser.gz";
	  static String backup_parser = "englishPCFG.ser.gz";
	  static String out_prefix =".parsed";
	  static String input_dir_path = "/home/vishayv/nlp_ee_project/terr/developset/test_dir";
	  static String out_dir_path = "/home/vishayv/nlp_ee_project/terr/developset/test_dir_parsed/";
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
	  public static File[] applyFileFilter(File files[]){

			  FileFilter fileFilter = new FileFilter() {
				      public boolean accept(File file) {
						          return !file.isDirectory();
								      }
			  };
			  files = dir.listFiles(fileFilter);
			  return files ;
	  }	  
	  public static File[] getFiles(){

			  //dir = new File(input_dir_path);
			  File[] files = dir.listFiles();
			  if(files == null){
					  System.out.println("Illegal Directory .Exiting");
					  System.exit(1);

			  }	  
			  System.out.println("check for length of original children arr "+files.length);
			  files = applyFileFilter(files);
			  System.out.println("check for length of new  children arr "+files.length);
			  return files;
	  }	  
	  public static void main(String[] args) throws IOException {

			  dir = new File(input_dir_path);
			  createOutDir() ;

		      LexicalizedParser lp = new LexicalizedParser(curr_parser);
			  LexicalizedParser lp_backup ; 
		  	  // PARSE EACH LINE OF THE TEXT --options sentence input and other things
			  //lp.setOptionFlags("-outputFormat","penn,oneline,typedDependenciesCollapsed,wordsAndTags","-MAX_ITEMS","600000","-maxLength", "80", "-retainTmpSubcategories");
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
					BufferedWriter out = new BufferedWriter(new FileWriter(new_abs_path));
			  	  	System.out.println("processing file "+file_path);
			  	  	System.out.println("processing filename "+filename);
			  	  	System.out.println("processing filepath "+file_path);
			  	  	System.out.println("output abs path "+new_abs_path);
					if(filename.startsWith(".")){
						  System.out.println("skipping  processing for file "+filename);
						  continue ;
					}	  
					if (filename.startsWith("meta")){
						  System.out.println("skipping  processing for file "+filename);
						  continue ;
					}
			  	  	Iterable< List<? extends HasWord> > sentences;
			  		DocumentPreprocessor dp = new DocumentPreprocessor(file_abs_path);
      		  		//DocumentPreprocessor dp = new DocumentPreprocessor("test.txt");
      		  		List<List<? extends HasWord>> tmp = new ArrayList<List<? extends HasWord>>();
      		  		for (List<HasWord> sentence : dp) {
        				tmp.add(sentence);
      		  		}
      		  		sentences = tmp;
			  		for (List<? extends HasWord> sentence : sentences) {
						System.out.println("Processing sentence "+sentence);
      					Tree parse = lp.apply(sentence);
						int depth = parse.depth();

						System.out.println("depth of tree"+depth);
						if(depth == 2){
								//parse = null ;
								lp = null ;
		      				    lp_backup = new LexicalizedParser(backup_parser);
			  					lp_backup.setOptionFlags("-MAX_ITEMS","700000","-maxLength", "80", "-retainTmpSubcategories");
								parse = lp_backup.apply(sentence);
    							out.write(parse.pennString());
								lp_backup = null ;
								lp = new LexicalizedParser(curr_parser);
			  					lp.setOptionFlags("-MAX_ITEMS","700000","-maxLength", "80", "-retainTmpSubcategories");
								// now extract info from backup
						}	
				    	//parse.pennPrint();
				  		//System.out.println();
				  		//System.out.println(parse.taggedYield());
    					out.write(parse.pennString());
				  		//System.out.println();
						/*FOR Printing dependency in a line*/ 
				 		//GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
						//Collection tdl = gs.typedDependenciesCCprocessed(true);
						// out putting the typed dependency 
						//System.out.println(tdl);
				  		//System.out.println();
						TreePrint tp = new TreePrint("oneline,typedDependenciesCollapsed");
			      		//tp.printTree(parse);
						//out.write(tp.printTree(parse));
						//System.out.println();

					}
				  	/*List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();
				  	System.out.println(tdl);
				  	System.out.println();
				  	TreePrint tp = new TreePrint("penn,typedDependenciesCollapsed");
			      	tp.printTree(parse);
				  	*/
    				out.close();
										// now write 
				}


			    // WRITE FILE IN PARSEDTEXTS directory
				// CREATE A DIRECTORY 	
				  
  }

}

