### Preprocessing Data

In order to do these experiments, you must preprocess the data. To do this:

1. Unzip Ellens data. This should produce a directory developset/.
2. Put this directory in the same directory as `preprocess.py`. Create a directory: `developset/pptexts/`. This is where `preprocess.py` will drop the "processed" data.
3. Run `python preprocess.py`.

## TODO LIST

##### Input Formatting : complete 

add support for [excerpts] and other [Text] tag substitutes
[Text] tag 
make use of [communique] contains : helps in retrieving organization names 
make use of [source] : organization name ? 


##### sentence fragmentation + parsing : Owner <vishay.vanjani@gmail.com> 
 
   use nltk toolkit to create chunks    


##### function that finds the incident ( arson , bomb , murder etc ) : + attach it to wordnet ??
   --i dont think auto slug is going to perform well here . have to just search for incident words ; 

##### write more/ Modify  heuristics 

##### Algorithm for finding syntactic roles given sentence pos tags   // priority : before Nov 8 
   can we use semantic roles instead ?
   check 

##### Functions that prints the relevant score and ranking score ( Autoslug TS) 

##### AutoSlug Type Annotation  // Priority : After Nov 8 

	Annotate the input MUC texts with the Answer keys 

##### semantic constraints checker : wordnet or basilisk like tool 
	check for semantic constraint like human weapon 
#####	using stanford NER ?? think of adding it some how but if we have np already then we dont need anything rite ... 

	



