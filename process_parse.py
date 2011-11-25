import os
import re
import gen_patterns
import utility
import matching

#DEBUG = True
DEBUG = False
PATH_TEST = "java_parser/test_patt2_out/"
PATH="developset/pptexts_parsed/" 
PATH_2="developset/test_set/full_parsed/" 
IPATH="java_parser/test_patterns_out/"
IRREL_PATH="irrel-texts/texts_parsed/"

#NP_CHUNK_1="(\(NP\s+(\(.*?\)+?)\))"
NP_CHUNK_1="\(NP\s+(\(.*?\)+?)\)"
#NP_CHUNK_2="(\(NP\-TMP\s+(\(.*?\)+?\))"
NP_CHUNK_2="\NP\-TMP\s+(\(.*?\)+?)\)"

NP_CHUNK_REPL=r"[ \1 ]/NP"
#NP_CHUNK_2_REPL=r"(\(NP\-TMP\s+\(.*?\)+?\))"

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
# does the same thing as pprocess_pfile but for a line 
def pprocess_pline(text):

	lines = text.split('\n')
	## initialize three dicts
	pos_tags_dict = {}
	parse_tree_dict = {}
	parse_dependency_dict = {}

	curr_loc_read = 0 
	lines_processed = 0 
	dependency_list = [] 
	for line in lines:
		line = line.strip()
		if (not line):
			continue
		if(utility.isEmpty(line)):
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
			
	return (pos_tags_dict,parse_tree_dict,parse_dependency_dict)

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
		if(utility.isEmpty(line)):
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

	# open output files 
	target_fd = open("target_out",'w')
	victim_fd = open("victim_out",'w')
	perp_fd = open("perp_out",'w')
	weapon_fd = open("weapon_out",'w')
	# init patterns lists 
	t_rel_patt_list = [] 
	v_rel_patt_list = [] 
	p_rel_patt_list = []
	w_rel_patt_list = [] 
	irrel_patt_list = []


	for root,dirs,files in os.walk(IRREL_PATH):

		for file in files:
			if(DEBUG):
				print "processing file",file
			# ignore swp files 	
			if(re.search("\.swp",file)):
					continue 
			(pos_tags_dict,parse_tree_dict,parse_dependency_dict) = pprocess_pfile(root + file)
			for sent_no in pos_tags_dict.keys() :
				
				sent= extract_np(pos_tags_dict[sent_no],parse_tree_dict[sent_no])
				sent = assemble_extracts(sent)
				#if(DEBUG):
				#print "np chunked sentece "+sent+"\n"
				temp_patt_list0,temp_patt_list1,temp_patt_list2,temp_patt_list3 = gen_patterns.match_rules(sent)
#print len(temp_patt_list)
#				print len(temp_patt_list2)
#				print len(temp_patt_list3)
				irrel_patt_list += temp_patt_list0 +temp_patt_list1 + temp_patt_list2 + temp_patt_list3 
	#print "irrel len ",irrel_patt_list
	#print "***********************" 
	print "no of irrel patt",len(irrel_patt_list)	


	for root, dirs, files in os.walk(PATH):
		for file in files:
			if(DEBUG):
				print "processing file",file
			# ignore swp files 	
			if(re.search("\.swp",file)):
					continue 
			(pos_tags_dict,parse_tree_dict,parse_dependency_dict) = pprocess_pfile(root + file)
			for sent_no in pos_tags_dict.keys() :
				sent= extract_np(pos_tags_dict[sent_no],parse_tree_dict[sent_no])
				sent = assemble_extracts(sent)
#if(DEBUG):
#					print "np chunked sentece "+sent+"\n"
				temp_patt_t,temp_patt_v,temp_patt_w,temp_patt_p = gen_patterns.match_rules(sent)
#print "victim len",len(temp_patt_list)
#				print "perp len",len(temp_patt_list2)
#				print "weapon len",len(temp_patt_list3)
				t_rel_patt_list += temp_patt_t 
				v_rel_patt_list += temp_patt_v 
				w_rel_patt_list += temp_patt_w 
				p_rel_patt_list += temp_patt_p
			
	print "the number of target patterns after dev ",len(t_rel_patt_list)
	print "the number of victim patterns after dev ",len(v_rel_patt_list)
	print "the number of perp patterns after dev",len(p_rel_patt_list)
	print "the number of weapon patterns after dev ",len(w_rel_patt_list)
	for root, dirs, files in os.walk(PATH_2):
		for file in files:
			if(DEBUG):
				print "processing file",file
			# ignore swp files 	
			if(re.search("\.swp",file)):
					continue 
			(pos_tags_dict,parse_tree_dict,parse_dependency_dict) = pprocess_pfile(root + file)
			for sent_no in pos_tags_dict.keys() :
				sent= extract_np(pos_tags_dict[sent_no],parse_tree_dict[sent_no])
				sent = assemble_extracts(sent)
				#	if(DEBUG):
				#	print "np chunked sentece "+sent+"\n"
				temp_patt_t,temp_patt_v,temp_patt_w,temp_patt_p = gen_patterns.match_rules(sent)
#print "victim len",len(temp_patt_list)
#				print "perp len",len(temp_patt_list2)
#				print "weapon len",len(temp_patt_list3)
				t_rel_patt_list += temp_patt_t 
				v_rel_patt_list += temp_patt_v 
				w_rel_patt_list += temp_patt_w 
				p_rel_patt_list += temp_patt_p
		
	#print v_rel_patt_list
	#print "***********************" 
	#print p_rel_patt_list
	#print "***********************" 
	#print w_rel_patt_list
	print "the number of target patterns after dev ",len(t_rel_patt_list)
	print "the number of victim patterns after test",len(v_rel_patt_list)
	print "the number of perp patterns after test",len(p_rel_patt_list)
	print "the number of weapon patterns after test",len(w_rel_patt_list)
	t_rel_set = matching.cmp(irrel_patt_list, t_rel_patt_list)
	for target_patt in t_rel_set:
		s = "(%s)"%(target_patt,)
		target_fd.write(s)
		target_fd.write("\n")

	v_rel_set = matching.cmp(irrel_patt_list, v_rel_patt_list)
	for victim_patt in v_rel_set:
		s = "(%s)"%(victim_patt,)
		victim_fd.write(s)
		victim_fd.write("\n")
	p_rel_set = matching.cmp(irrel_patt_list, p_rel_patt_list)
	for perp_patt in p_rel_set:
		s = "(%s)"%(perp_patt,)
		perp_fd.write(s)
		perp_fd.write("\n")
	if(len(w_rel_patt_list) > 0):
		w_rel_set = matching.cmp(irrel_patt_list, w_rel_patt_list)
		for weapon_patt in w_rel_set:
			s = "(%s)"%(weapon_patt,)
			weapon_fd.write(s)
			weapon_fd.write("\n")
	else:
		print "no patterns found for weapon WTF "
	#print rel_set
	victim_fd.close()
	perp_fd.close()
	weapon_fd.close()

if __name__== '__main__':
	# do something 
	main()
