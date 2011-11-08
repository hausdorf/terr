from __future__ import with_statement
import os, re, sys


# Directories
PARSED_DIR = 'developset/test_dir_parsed/'

# Regexes
NP = '(\S+)/(NP|NNS)(\s+)(was|were|are'


def groups(l, key=lambda x:x):
	grp = []
	curr = key(l[0])
	for e in l:
		if curr == key(e):
			grp.append(e)
		else:
			yield grp
			grp = [e]
			curr = key(e)

		if e == l[-1]:
			yield grp

# Walk through files in the parsed files directory
def walk_parsed():
	for dir, folders, files in os.walk(PARSED_DIR):
		for file in files:
			f, ext = os.path.splitext(file)
			if ext == '.parsed':
				f = open(dir + file)
				yield f
				f.close()

# Outputs all Stanford Parse information associated with a sentence, as 
# list of sentences separated by '\n'.
def walk_sentences():
	for f in walk_parsed():
		curr = []
		for line in f.readlines():
			if line.find('*****') > -1:
				yield curr
				curr = []
				continue
			curr.append(line)

def patt1(grps):
	lgrps = len(grps)

	curr = []
	i = 0
	while i < len(grps):
		_, tag = grps[i][0].split('/')

		if tag == 'NNS' or tag == 'NNP':
			curr.append(grps[i])

			i += 1

			if i >= lgrps:
				break

			_, tag = grps[i][0].split('/')
			
			if tag == ',':
				i += 1
			if i >= lgrps:
				break

			if tag == 'VBD':
				curr.append(grps[i])

				i += 1

				if i >= lgrps:
					break

				_, tag = grps[i][0].split('/')

				if tag == ',':
					i += 1
				if i >= lgrps:
					break

				if tag == 'NNS' or tag == 'NNP':
					curr.append(grps[i])
					yield curr

					i += 1
		else:
			i += 1

		curr = []

def process_sent(sent):
	split = sent.split()
	grps = list(groups(split, key=lambda x:x.split('/')[1]))

	for match in patt1(grps):
		print match
		for e in match:
			print e
		print
	return

def aslog_phase_1():
	for s in walk_sentences():
		process_sent(s[0])


if __name__ == '__main__':
	aslog_phase_1()
