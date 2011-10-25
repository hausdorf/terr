import os, re, stat


# WHERE YOU PUT OUR DATA
PATH = 'developset/texts/'  # Old data
REPL_DIR = 'developset/pptexts/'       # Processed data

# REGEXES
ANY_META = '\[[\s\S]+\]' # Finds any thing inside brackets, e.g. [TEXT]
TEXT = '\[[TEXT]+\]'     # Everything before the [TEXT] tag


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
	m = re.search(ANY_META, text)
	if m:
		text = text[m.end(0):]

	return text


# Removes all brackets like [BEGIN] if present
def remove_if_brackets(text):
	m = re.split(ANY_META, text)
	if m:
		text = ' '.join(m)

	return text


# Preprocess that file!
def pprocess_file(filename):
	text = f_read(filename)

	text = remove_if_head(text)
	text = remove_if_brackets(text)

	return text


def main():
	for root, dirs, files in os.walk(PATH):
		for file in files:
			text = pprocess_file(root + file)
			f_write(REPL_DIR + file, text)


if __name__ == '__main__':
	main()
