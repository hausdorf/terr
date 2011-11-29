import re
import sys
import os
import utility
import collections
import process_parse

DEBUG = False
PATT_ORIG = "<.*?>"
PATT_REPL2 = r"(\[[^/]*?\])\/NP"
PATT_REPL = " "
COLL_SPACES = "\s+"
SPACES_REPL = " "

PATT_NP = r"(\[[^/]*?\])\/NP"
PATT_RHALF_NP = r"([^/]*?\])\/NP"
PATT_LHALF_NP = r"(\[[^/]*)"

FRONT = 1
BACK = 0

## IMPORTANT make room for multiple spaces in ur regex  victim was killed  in text or victim was  killed 
def is_front(patt):
	if(patt[0] == ' '):
		return True	
	
def get_np(word,parsed_sent,is_front,meta):

	out_list  = []
	word = word.strip()
	parsed_sent = parsed_sent.strip()
	if(is_front):
		# ABC WAS ASSASINATED 
		# splits according to first occurence of word  
		temp_arr = parsed_sent.split(word)
		if(len(temp_arr)) > 2:
			if(DEBUG):
				print "sent has more than two "+word+" parsed sent = "+parsed_sent
			for i in xrange(len(temp_arr)-1):
				first_half  = temp_arr[i]
				# search for NP thing here
				if(DEBUG):
					print "first part",first_half
				# check if there was a half split 	
				#m_half = re.search(PATT_LHALF_NP,first_half)
				m_half = re.findall(PATT_LHALF_NP,first_half)
				m = re.findall(PATT_NP,first_half)
				if m_half:
					#np = m_half.group(0)
					for np in m_half:
						np_clean  = utility.np_cleaner(np)
						if (np_clean):
							out_list.append(np_clean)
				if m:
					#  we need the rightmost pattern found m[-1] not necessarily for Front patterns look at all NP ? 
					for np in m:
					#np = m[-1]
						np_clean  = utility.np_cleaner(np)
						if (np_clean):
							out_list.append(np_clean)
		else:	
			first_half  = temp_arr[0]
			# search for NP thing here
			if (DEBUG):
				print "first half",first_half
			# check if there was a half split 	
			#m_half = re.search(PATT_LHALF_NP,first_half)
			m_half = re.findall(PATT_LHALF_NP,first_half)
			m = re.findall(PATT_NP,first_half)
			if m_half:
				
				#np = m_half.group(0)
				for np in m_half:
					np_clean  = utility.np_cleaner(np)
					if(np_clean):
						out_list.append(np_clean)
			if m:
				#  we need the rightmost pattern found m[-1] 
				for np in m:
				#np = m[-1]
					np_clean  = utility.np_cleaner(np)
					if (np_clean):
						out_list.append(np_clean)
	else:
		# murder of DEf 

		temp_arr = parsed_sent.split(word)
		if(len(temp_arr)) > 2:
			# murder of dEF and murder of eFg and murder of xyz
			if(DEBUG):
				print "sent has more than two "+word+"parsed sent = "+parsed_sent
			for i in xrange(len(temp_arr)-1):
				# for e.g for two instance of murder we will have temp_arr[1] and temp_arr[2]
				second_half  = temp_arr[i+1]
				# search for NP thing here
				if(DEBUG):
					print "second part",second_half
				# search usually progresses from left to right so this should be good
				#m_half = re.search(PATT_RHALF_NP,second_half)
				m_half = re.findall(PATT_RHALF_NP,second_half)
				#m = re.search(PATT_NP,second_half)
				m = re.findall(PATT_NP,second_half)
				if m_half:
					#np = m_half.group(0)
					for np in m_half:
						np_clean  = utility.np_cleaner(np)
						if (np_clean):
							out_list.append(np_clean)
				if m:
					#np = m.group(0)
					for np in m:
						np_clean  = utility.np_cleaner(np)
						if (np_clean):
							out_list.append(np_clean)
		elif(len(temp_arr) == 2):	
			second_half  = temp_arr[1]
			# search for NP thing here
			if(DEBUG):
				print "second half",second_half
			# search usually progresses from left to right so this should be good
			#m_half = re.search(PATT_RHALF_NP,second_half)
			m_half = re.findall(PATT_RHALF_NP,second_half)
			#m = re.search(PATT_NP,second_half)
			m = re.findall(PATT_NP,second_half)
			if m_half:
				#np = m_half.group(0)
				for np in m_half:
					np_clean  = utility.np_cleaner(np)
					if (np_clean):
						out_list.append(np_clean)
			if m:
				#np = m.group(0)
				for np in m:
					np_clean  = utility.np_cleaner(np)
					if (np_clean):
						out_list.append(np_clean)
	
	out_set = set(out_list)
	# further process this list 
	out_list = list(out_set)
	new_list = utility.common_cleaner(out_list)
	if(meta =='victim'):
		new_list = utility.victim_cleaner(new_list)
		if(DEBUG):
			print "####victim removal list"
	elif(meta == 'target'):
		new_list = utility.target_cleaner(new_list)
		if(DEBUG):
			print "####target removal list"
	elif(meta == 'perpi'):
		new_list = utility.perpi_cleaner(new_list)
		if(DEBUG):
			print "####perp removal list"

	if(DEBUG):		
		print new_list

	return new_list 

# THIS IS CALLED FOR EACH SENTENCE i.e we check for all victim patterns in each sentence  
def get_victims(sent,patt_lines):
	pot_victim_list = []
	matched_patt_word = []
	for patt in patt_lines:

		if (not patt):
			continue
		#m2 = re.search('MURDERED',patt)
		#if m2:
		#	print "patt",patt
		# collapse multiple white spaces 
		patt = re.sub(COLL_SPACES,SPACES_REPL,patt)
		# check if any of the victim patterns exist for this line
		m = re.findall(patt,sent)
		if m:
			# check forward or backward 
			if(DEBUG):
				print "pattern matched ",m,"for patt ",patt,"and sent",sent
			# Now parse this line
			parsed_sent = parse_file(sent)
			if (not parsed_sent):
				print "could not parse line continuing "+parsed_sent
				continue 
			# NOW NP CHUNK THE SENTENCE
			# First make sense of parsed input  	
			pos_dict,parse_dict,_ = process_parse.pprocess_pline(parsed_sent)
			# the above might return multiple lines 
			for i in xrange(len(pos_dict.keys())):
				pos_sent = pos_dict[i]
				parsed_sent = parse_dict[i]
				# NP chunking algo
				np_sent= process_parse.extract_np(pos_sent,parsed_sent)
				np_chunk_sent = process_parse.assemble_extracts(np_sent)

				# this ALGO WORKS FOR VICTIM CHECK FOR OTHERS 
				if(is_front(patt)):
					#use the last word to split the parsed sentence
					patt = patt.strip()
					if(not patt):
						print "patt was empty line move to next"
						continue
					split_patt = patt.split(r"\s*[\w]*\s*")
					split_word = split_patt[-1]
					split_word = split_word.strip()
					#matched_patt_word.append(split_word)
					m_temp  = re.search(split_word,np_chunk_sent)
					if(not m_temp):
						print "split word=",split_word,"not in sent"
						continue 
					pot_victim_list = get_np(split_word,np_chunk_sent,FRONT,'victim')
					if(len(pot_victim_list) > 0): 
						# THIS MAKES SURE THAT a FONT PATT IS NOT MATCHED AGAIN BY BACK PATT 
						matched_patt_word.append(split_word)
				else:
					# MATCHES BACK PATTERN 
					# use the first word in the patt to split the parsed sentence 
					patt = patt.strip()
					if(not patt):
						print "patt was empty line move to next"
						continue
					split_patt = patt.split()
					split_word = split_patt[0]
					split_word = split_word.strip()
					if split_word in matched_patt_word:
						if(DEBUG):
							print "###not matching back pattern since back pattern with same key word was matched ,back key word =",split_word
						continue

					m_temp  = re.search(split_word,np_chunk_sent)
					if(not m_temp):
						print "split word=",split_word,"not in sent continuing"
						continue 
					pot_victim_list = get_np(split_word,np_chunk_sent,BACK,'victim')
					 
	# search for AND IN THE np if it exists divide the np into two parts 		
	new_list = and_detector(pot_victim_list)	
	
	return new_list

def get_perpi(sent,patt_lines):

	pot_perpi_list = []
	matched_patt_word = []
	for patt in patt_lines:

		if (not patt):
			continue
		#m2 = re.search('MURDERED',patt)
		#if m2:
		#	print "patt",patt
		# collapse multiple white spaces 
		patt = re.sub(COLL_SPACES,SPACES_REPL,patt)
		# check if any of the victim patterns exist for this line
		m = re.findall(patt,sent)
		if m:
			# check forward or backward 
			if(DEBUG):
				print "pattern matched ",m,"for patt ",patt,"and sent",sent
			# Now parse this line
			parsed_sent = parse_file(sent)
			if (not parsed_sent):
				print "could not parse line"+parsed_sent
				continue 
			# NOW NP CHUNK THE SENTENCE
			# First make sense of parsed input  	
			pos_dict,parse_dict,_ = process_parse.pprocess_pline(parsed_sent)
			# the above might return multiple lines 
			for i in xrange(len(pos_dict.keys())):
				pos_sent = pos_dict[i]
				parsed_sent = parse_dict[i]
				# NP chunking algo
				np_sent= process_parse.extract_np(pos_sent,parsed_sent)
				np_chunk_sent = process_parse.assemble_extracts(np_sent)

				if(is_front(patt)):
					#perpi just have one word ( as of now) so just split by word
					patt = patt.strip()
					if(not patt):
						print "patt was empty line move to next"
						continue
					split_patt = patt.split()
					split_word = split_patt[0]
					split_word = split_word.strip()
					# THIS MAKES SURE THAT a FONT PATT IS NOT MATCHED AGAIN BY BACK PATT 
					#matched_patt_word.append(split_word)
					m_temp  = re.search(split_word,np_chunk_sent)
					if(not m_temp):
						print "split word=",split_word,"not in sent"
						continue 
					pot_perpi_list = get_np(split_word,np_chunk_sent,FRONT,'perpi')
					if(len(pot_perpi_list) > 0): 
						# THIS MAKES SURE THAT a FONT PATT IS NOT MATCHED AGAIN BY BACK PATT 
						matched_patt_word.append(split_word)
				else:
					# MATCHES BACK PATTERN 
					# Back patterns have three words ..second last word is the main word / split word  
					patt = patt.strip()
					if(not patt):
						print "patt was empty line move to next"
						continue
					split_patt = patt.split()
					# second last word or second word is the main word  
					split_word = split_patt[1]
					split_word = split_word.strip()
					if split_word in matched_patt_word:
						print "###not matching back pattern since back pattern with same key word was matched ,back key word =",split_word
						continue
					m_temp  = re.search(split_word,np_chunk_sent)
					if(not m_temp):
						print "split word=",split_word,"not in sent"
						continue 
					pot_perpi_list = get_np(split_word,np_chunk_sent,BACK,'perpi')
					 
	# search for AND IN THE np if it exists divide the np into two parts 		
	new_list = and_detector(pot_perpi_list)	
	
	return new_list



def get_targets(sent,patt_lines):

	pot_target_list = []
	matched_patt_word = []
	for patt in patt_lines:
		if (not patt):
			continue
		patt = re.sub(COLL_SPACES,SPACES_REPL,patt)

		m = re.findall(patt,sent)
		if m:
			# check forward or backward 
			if(DEBUG):
				print "pattern matched ",m,"for patt ",patt,"and sent",sent
			# Now parse this line
			parsed_sent = parse_file(sent)
			if (not parsed_sent):
				print "could not parse line"+parsed_sent
				continue 
			# NOW NP CHUNK THE SENTENCE
			# First make sense of parsed input  	
			pos_dict,parse_dict,_ = process_parse.pprocess_pline(parsed_sent)
			# the above might return multiple lines 
			for i in xrange(len(pos_dict.keys())):
				pos_sent = pos_dict[i]
				parsed_sent = parse_dict[i]
				# NP chunking algo
				np_sent= process_parse.extract_np(pos_sent,parsed_sent)
				np_chunk_sent = process_parse.assemble_extracts(np_sent)
				# MATCHES BACK PATTERN 
				# use the first word in the patt to split the parsed sentence 
				patt = patt.strip()
				if(not patt):
					print "patt was empty line move to next"
					continue
				split_patt = patt.split()
				split_word = split_patt[0]
				split_word = split_word.strip()
				if split_word in matched_patt_word:
					if(DEBUG):
						print "###not matching back pattern since back pattern with same key word was matched ,back key word =",split_word
					continue
				m_temp  = re.search(split_word,np_chunk_sent)
				if(not m_temp):
					print "split word=",split_word,"not in sent"
					continue 
				pot_target_list = get_np(split_word,np_chunk_sent,BACK,'target')
					 
	# search for AND IN THE np if it exists divide the np into two parts 		
	new_list = and_detector(pot_target_list)	
	return new_list
	
def and_detector(v_list):
	v_new_l  = []
	# For each of the potential patterns search for AND 
	for v in v_list:
		v = v.strip()
		v = re.sub(COLL_SPACES,SPACES_REPL,v)
		# ADD INCLUDING 
		m = re.search("\\bAND\\b",v)
		m_include = re.search("\\bINCLUDING\\b",v)
		m_accomp = re.search("\\bACCOMPANIED\\b",v)
		m_their = re.search("\\bTHEIR\\b",v)
		if m:
			v_arr = v.split("AND")
			# JUst add all the splits to new_list 
			for v_part in v_arr:
					v_part = v_part.strip()
					if v_part:
						v_new_l.append(v_part)
		elif m_include:
			v_arr = v.split("INCLUDING")
			# JUst add all the splits to new_list 
			for v_part in v_arr:
					v_part = v_part.strip()
					if v_part:
						v_new_l.append(v_part)
		elif m_accomp:
			v_arr = v.split("ACCOMPANIED")
			# JUst add all the splits to new_list 
			for v_part in v_arr:
					v_part = v_part.strip()
					if v_part:
						v_new_l.append(v_part)
		elif m_their:
			v_arr = v.split("THEIR")
			# JUst add all the splits to new_list 
			for v_part in v_arr:
					v_part = v_part.strip()
					if v_part:
						v_new_l.append(v_part)
		else:
			v_new_l.append(v)

	return v_new_l

def parse_file(line):

	fj = open("text.txt",'w')
	fj.write(line)
	fj.close()
	os.system("java -mx1000m -cp .:./stanford-parser.jar ParseFast ")
	fo = open("text_out.txt")
	txt = fo.read()
	fo.close()
	return txt 
	# delete this text file 
	# return success or failure 
	
def process_patterns(text):
	new_dict = collections.defaultdict(lambda:0)			
 
	lines = text.split("\n")

	for line in lines:
		if(not line):
			continue 
		# extract the pattern (pattern,score,example list) from line .. line is string 
		patt = line.strip()
		# split by comma 
		patt_l = patt.split(',')
		new_patt = patt_l[0]
		#remove all trailing ( and ' and whitespaces
		new_patt = new_patt.strip("( '")
		# collapse multiple whitespace into one whitespace
		new_patt_1 = re.sub(COLL_SPACES,SPACES_REPL,new_patt)
		# substitute the <NP> to the corresponding regex
		patt_new = re.sub(PATT_ORIG,PATT_REPL,new_patt_1)
		new_dict[patt_new] += 1 
	return new_dict.keys()


def get_victims2(parsed_sent,p_sent,lines):
# read victim patterns file 
	print "in get i"
#print sent
# for testing only 
	m1  = re.search('VIOLENTLY',parsed_sent)
	if m1:
		print parsed_sent
		print p_sent 
	for patt in lines:
		if (not patt):
			continue
	m2 = re.search('MURDERED',patt)
	if m2:
		print "patt",patt
	m = re.findall(patt,p_sent)
	if m:
		# check forward or backward 	
		print "pattern matched ",m
		# this ALGO WORKS FOR VICTIM CHECK FOR OTHERS 
		if(is_front(patt)):
			#use the last word to split the parsed sentence
			patt = patt.strip()
			split_patt = patt.split()
			split_word = split_patt[-1]
			if(not patt):
				print "something went wrong"
			get_np(split_word,parsed_sent,FRONT)
		else:
			# use the first word in the patt to split the parsed sentence 
			patt = patt.strip()
			get_np(split_word,parsed_sent,BACK)
			


# this file reads a file which contains the extracted pattern tuples , takes those patterns and used it extract NP from a parsed file 
# writes the regex patterns to a file , The actual matching can be done easily 	
if __name__ =="__main__":

	# reads the patterns tuples filename from the command line 

	filename = sys.argv[1]
	filename_out = filename +"_regex2"
	text = utility.f_read(filename)
	new_list = process_patterns(text)
	new_list.sort()
	# write each of these into a file 
	f_w = open(filename_out,'w')
	for line in new_list:
		f_w.write(line)
		f_w.write("\n")

	f_w.close()


	text = utility.f_read('victim_out_patterns_regex2')
  	lines = text.split('\n')
"""
	# read sample parsed text file 
	(pos_tags_dict,parse_tree_dict,parse_dependency_dict) = process_parse.pprocess_pfile("main_DEV-MUC3-1299.parsed")
	for sent_no in pos_tags_dict.keys() :
				pos_tagged_sent = pos_tags_dict[sent_no]
				sent= process_parse.extract_np(pos_tags_dict[sent_no],parse_tree_dict[sent_no])
				sent = process_parse.assemble_extracts(sent)
				# for each sentence remove multiple white spaces
				new_sent = re.sub(COLL_SPACES,SPACES_REPL,sent)
				# for each sentence look for all the victim patterns
				plain_sent = utility.pos_to_plain(pos_tagged_sent)
				victim_list = get_victims(new_sent,plain_sent,lines)

	# define a function that goes over all the patterns and returns a list of probable victim
"""
	
