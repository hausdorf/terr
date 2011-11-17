import os
import re
import gen_patterns

DEBUG = False
#PATH="developset/test_dir_parsed_1/" 
PATH="java_parser/test_patterns_out/"

#NP_CHUNK_1="(\(NP\s+(\(.*?\)+?)\))"
NP_CHUNK_1="\(NP\s+(\(.*?\)+?)\)"
#NP_CHUNK_2="(\(NP\-TMP\s+(\(.*?\)+?\))"
NP_CHUNK_2="\NP\-TMP\s+(\(.*?\)+?)\)"

NP_CHUNK_REPL=r"[\1]/NP"
#NP_CHUNK_2_REPL=r"(\(NP\-TMP\s+\(.*?\)+?\))"

EMPTY_LINE  = "\s*\n\s*$" # checks if a line is empty
TAGGED_COMMA = "\s,\/,(?=\s)"  # selects commas in the pos tagged o/p of parser ..should we remove '(single quotes) as well ? 
COMMA  = ","
NOUN_DEP = "nn"

# processes the dependency list parse of a line and extracts np from them and adds those np to the pos tagged sentence

def extract_np(pos_sent,parse_tree): # string , num ,tuple immutable , list ,dict mutable 

	prev_pattern = "2" # init with some random pattern

	# split sentences by space
	pos_sent_list = pos_sent.split(" ")
	# search the list for nn types only for now 

	m1  = re.sub(NP_CHUNK_1,NP_CHUNK_REPL,parse_tree)
	m2  = re.sub(NP_CHUNK_2,NP_CHUNK_REPL,m1)
	return m2 	
	#return " ".join(pos_sent_list)


def extract_np2(pos_sent,dep_list): # string , num ,tuple immutable , list ,dict mutable 

	prev_pattern = "2" # init with some random pattern

	# split sentences by space
	pos_sent_list = pos_sent.split(" ")
	# search the list for nn types only for now 
	for dep in dep_list:
		m = re.match(NOUN_DEP,dep)
		if(m):
			# read the first nn extract the token numbers 
			# split by comma 
			split_arr = dep.split(COMMA)
			if(prev_pattern == split_arr[0]):
				continue
			# save the pattern to avoid next match 
			prev_pattern = split_arr[0]
			# left,right for identifying np 
			right = split_arr[1]
			left = split_arr[0] 
			end_index,start_index = extract_num(left,right)
			if(DEBUG):
				print "end index",(end_index-1),pos_sent_list[(end_index-1)]
				print "start",(start_index-1),pos_sent_list[(start_index-1)]
			
			# Add paranthesis to the noun phrase 
			pos_sent_list[(start_index-1)] = "%s %s" %("(",str(pos_sent_list[(start_index-1)]))
			pos_sent_list[(end_index-1)] = "%s %s" %(str(pos_sent_list[(end_index-1)]),")/NP")
			
	return " ".join(pos_sent_list)

# extracts noun phrase range as numbers  from the NN dependency  	
def extract_num(left,right):
	temp_arr = left.rsplit("-")
	if(len(temp_arr)!=2 ): 
		return -1 
	left_num = temp_arr[1]
	temp_arr = right.rsplit("-")
	if( len(temp_arr) !=2 ): 
		return -1
		
	right_num = temp_arr[1]
	# remove the trailing ) from right_num
	right_num = right_num.rstrip(")")	

	# convert to ints 
	left_num = int(left_num)
	right_num = int(right_num)
	return (left_num,right_num)

# removes any white spaces from left and right end of the string and removes \n from right end.	
def clean_str(line):
	line = line.lstrip()
	line = line.rstrip(" \n")
	return line

# remove parsed or Tagged commas(ie ',/,') from line 	
def remove_tagged_comma(line):
	line = re.sub(TAGGED_COMMA,"",line)
	return line 
# checks if a line is empty i.e \s*\n
def isEmpty(line):	
	m = re.match(EMPTY_LINE,line)
	if(m):
		return True
	return False	
# returns (dict,dict,dict) i.e all the different kinds of parse(i.e pos_tags,parse tree,dependency list) for all the lines in a file 
def pprocess_pfile(filename):

	## initialize three dicts
	pos_tags_dict = {}
	parse_tree_dict = {}
	parse_dependency_dict = {}

	# read the pos tagged sentence and tokenize the sentence  
	fd = open(filename)
	curr_loc_read = 0 
	lines_processed = 0 
	dependency_list = [] 
	for line in fd:
		if(isEmpty(line)):
			continue
		line = clean_str(line)
		# first part of each line is the pos tag
		if(curr_loc_read==0):
			#line = remove_tagged_comma(line) 
			pos_tags_dict[lines_processed] = line
			curr_loc_read += 1
		# second part of each line is the parse tree	
		elif(curr_loc_read==1):
			parse_tree_dict[lines_processed] = line 
			curr_loc_read += 1 
		# third part of each line is the dependency list 	
		elif(curr_loc_read==2):
			m = re.match("\*\*\*",line)	
			if(m):
					parse_dependency_dict[lines_processed]=dependency_list # makes a copy
					# move to a next line in text 
					lines_processed += 1
					# initialize vars for next line 
					curr_loc_read = 0 
					dependency_list = []
			else:		
				dependency_list.append(line)	
			
	fd.close()
	return (pos_tags_dict,parse_tree_dict,parse_dependency_dict)


def rmv_irrelevant(prsd):
	spl = prsd.split()
	lspl = len(spl)

	if lspl < 2:
		return ''

	wrds = []

	i = 1
	curr = spl[0]
	while i < lspl:
		if curr[0][0] == '(' and spl[i][-1] == ')':
			s1 = curr.strip('(')
			s2 = spl[i].strip(')')
			wrds.append('%s/%s' % (s2, s1))

		curr = spl[i]
		i += 1

	if len(wrds) > 0:
		return ' '.join(wrds)
	else:
		return ''

def assemble_extracts(cntnt):
	extrcts = []

	spl = re.split('(\[.*?\]\/NP)', cntnt)
	for e in spl:

		if e[0] == '[' and e[-3:] == '/NP':
			extrcts.append(e)
			continue

		extrct = rmv_irrelevant(e)
		if extrct != '':
			extrcts.append(extrct)
	return ' '.join(extrcts)



def main():
	rel_patt_list = [] 
	irrel_patt_list = [] 
	for root, dirs, files in os.walk(PATH):
		for file in files:
			if(DEBUG):
				print "processing file",file
			# ignore swp files 	
			if(re.search("\.swp",file)):
					continue 
			(pos_tags_dict,parse_tree_dict,parse_dependency_dict) = pprocess_pfile(root + file)
			for sent_no in pos_tags_dict.keys() :
				#sent= extract_np2(pos_tags_dict[sent_no],parse_dependency_dict[sent_no])
				
				sent= extract_np(pos_tags_dict[sent_no],parse_tree_dict[sent_no])

				sent = assemble_extracts(sent)
				if(DEBUG):
					print "np chunked sentece "+sent+"\n"
				if(re.search("\.irrel.parsed",file)):
					temp_patt_list = gen_patterns.match_rules(sent)
					irrel_patt_list += temp_patt_list
				else:
					temp_patt_list = gen_patterns.match_rules(sent)	
					rel_patt_list  += temp_patt_list
		print irrel_patt_list
		print "***********************" 
		print rel_patt_list 

if __name__== '__main__':
	# do something 
	main()
