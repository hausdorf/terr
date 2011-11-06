### Preprocessing Data

In order to do these experiments, you must preprocess the data. To do this:

1. Unzip Ellens data. This should produce a directory developset/.
2. Put this directory in the same directory as `preprocess.py`. Create a directory: `developset/pptexts/`. This is where `preprocess.py` will drop the "processed" data.
3. Run `python preprocess.py`.

## TODO LIST

1. ~~**Input Formatting : complete**~~ add support for [excerpts] and other [Text] tag substitutes
[Text] tag 
make use of [communique] contains : helps in retrieving organization names 
make use of [source] : organization name ? 


2. **sentence fragmentation + parsing : Owner <vishay.vanjani@gmail.com>** use nltk toolkit to create chunks    


3. **function that finds the incident ( arson , bomb , murder etc ) : + attach it to wordnet ??** --i dont think auto slug is going to perform well here . have to just search for incident words ; 

4. **write more/ Modify  heuristics**

5. **Algorithm for finding syntactic roles given sentence pos tags   // priority : before Nov 8** can we use semantic roles instead ? check 

6. **Functions that prints the relevant score and ranking score ( Autoslug TS)**

7. **AutoSlug Type Annotation  // Priority : After Nov 8**

	Annotate the input MUC texts with the Answer keys 

8. **semantic constraints checker : wordnet or basilisk like tool** check for semantic constraint like human weapon 

9. **using stanford NER ??** think of adding it some how but if we have np already then we dont need anything rite ... 


