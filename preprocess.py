import os, re, stat


# WHERE YOU PUT OUR DATA
PATH = 'developset/texts/'  # Old data
REPL_DIR = 'developset/pptexts/'       # Processed data

# REGEXES
ANY_TAG = '\[[\s\S]+?\]' # Finds any thing inside brackets, e.g. [TEXT]
TEXT = '\[[TEXT]+\]'   # Everything before the [TEXT] tag
START_TAG= '\[TEXT\]|\[EXCERPT\]|\[EXCERPTS\]' # SELECT MAIN TAG 
FIRST =".+?\n" # selects first line of each text 

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

def remove_first_line(text):
	text = re.sub(FIRST,"",text,1)
	return text

# splits the input text into meta_info and main_text,squishes brackets in main
# and returns a join separated by 3 lines 
def split_text(text):
	text_arr  = re.split(START_TAG,text,1)
	if(len(text_arr) != 2):
		return -1 
	else:
		#remove any tags in main_text 
		text_arr[1] = re.sub(ANY_TAG,"",text_arr[1])
		return "\n\n\n".join(text_arr)
	 
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


# Preprocess that file!
def pprocess_file(filename):
	text = f_read(filename)
	text = remove_first_line(text) 
	ret = split_text(text)
	if(ret == -1):
		print "error splitting file",filename,"\n"
	else:
		text = ret 

#text = remove_if_head(text)
#text = remove_if_brackets(text)

	return text


def main():
	for root, dirs, files in os.walk(PATH):
		for file in files:
			text = pprocess_file(root + file)
			f_write(REPL_DIR + file, text)


if __name__ == '__main__':
	main()
