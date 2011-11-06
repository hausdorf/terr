import os
import re

DEBUG = False
PATH="developset/test_dir_parsed_1/" 

EMPTY_LINE  = "\s*\n\s*$" # checks if a line is empty
TAGGED_COMMA = "\s,\/,(?=\s)"  # selects commas in the pos tagged o/p of parser ..should we remove '(single quotes) as well ? 
COMMA  = ","
NOUN_DEP = "nn"

# processes the dependency list parse of a line and extracts np from them and adds those np to the pos tagged sentence
def extract_np(pos_sent,dep_list): # string , num ,tuple immutable , list ,dict mutable 

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

def main():
	for root, dirs, files in os.walk(PATH):
		for file in files:
			if(DEBUG):
				print "processing file",file
			# ignore swp files 	
			if(re.search("\.swp",file)):
					continue 
			(pos_tags_dict,parse_dependency_dict,parse_dependency_dict) = pprocess_pfile(root + file)
			for sent_no in pos_tags_dict.keys() :
				sent= extract_np(pos_tags_dict[sent_no],parse_dependency_dict[sent_no])
				print sent 

if __name__== '__main__':
	# do something 
	main()

