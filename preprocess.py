import os, re, stat

# WHERE YOU PUT OUR DATA
PATH = 'developset/texts/'  # Old data
REPL_DIR = 'developset/pptexts/'       # Processed data

# REGEXES
ANY_TAG = '\[[\s\S]+?\]' # Finds any thing inside brackets, e.g. [TEXT]
TEXT = '\[[TEXT]+\]'   # Everything before the [TEXT] tag
START_TAG= '\[TEXT\]|\[EXCERPT\]|\[EXCERPTS\]' # SELECT MAIN TAG 
FIRST =".+?\n" # selects first line of each text 
REDUNDANT_NEWLINE = "\n(?=.)" # selects a new line if it occurs before some char
COMMA =",(?=\s)"  # selects a comma if it is followed by a space 
DOUBLE_QUOTES = "\"" # selects double quotes

# Helper: iterates through file by line, then closes file
def f_iter(filename):
	f = open(filename)

	for line in f.readlines():
		yield line

	f.close()

# Helper: reads all text from file, then closes file
def f_read(filename):
	f = open(filename)
	text = f.read()
	f.close()

	return text

def f_write(filename, text):
	f = open(filename, 'w')
	f.write(text)
	f.close()

# Removes everything before [TEXT] if such a tag is present
def remove_if_tscript(text):
	m = re.search(TEXT, text)
	if m:
		text = text[m.end(0):]

	return text

# Removes everything before first [TAG] if such a tag is present
def remove_if_head(text):
	m = re.search(ANY_TAG, text)
	if m:
		text = text[m.end(0):]

	return text


# Removes all brackets like [BEGIN] if present
def remove_if_brackets(text):
	m = re.split(ANY_TAG, text)
	if m:
		text = ' '.join(m)

	return text

# removes first line 	
def remove_first_line(text):
	text = re.sub(FIRST,"",text,1)
	return text

# splits the input text into meta_info and main_text,squishes brackets in main
# and returns a tuple
def split_text(text):
	text_arr  = re.split(START_TAG,text,1)
	if(len(text_arr) != 2):
		return (-1,-1) 
	else:
		# remove blank line if exists in meta text 
		text_arr[0] = re.sub(REDUNDANT_NEWLINE,"",text_arr[0])
		#remove any tags in main_text 
		text_arr[1] = re.sub(ANY_TAG,"",text_arr[1])
		return (text_arr[0],text_arr[1])
	 
# split into sentence 
def sent_splitter(text):
	sent_tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer() 
	sent_list = sent_tokenizer.tokenize(text)
	for i in range(len(sent_list)):
		# remove \n in the middle of the line if it exists 
		sent_list[i] = re.sub(REDUNDANT_NEWLINE," ",sent_list[i])

		# STANFORD PARSER CONSIDERS COMMAS DONT DELETE  
		# Remove double quotes 
#sent_list[i] = re.sub(DOUBLE_QUOTES,"",sent_list[i])
		# replace comma (if its followed by space) with ""
#sent_list[i] = re.sub(COMMA,"",sent_list[i]) 

	return "\n".join(sent_list) 

# Preprocess that file!
def pprocess_file(filename):
	text = f_read(filename)
	text = remove_first_line(text) 
	(meta,main) = split_text(text)
	if(meta == -1 ):
		print ("error splitting file",filename,"\n")

	return (meta,main)


def main():
	for root, dirs, files in os.walk(PATH):
		for file in files:
			(meta,main) = pprocess_file(root + file)
			meta_tag = "meta_" 
			main_tag = "main_"
			f_write(REPL_DIR + meta_tag+file, meta)
			# send main to sent splitter -->stanford Parser takes care of this U.
			#main_text = sent_splitter(main)
			f_write(REPL_DIR + main_tag+file, main)
			

if __name__ == '__main__':
	main()
