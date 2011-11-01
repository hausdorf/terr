import os
import re

PATH="developset/test_dir_parsed/" 

EMPTY_LINE  = "\s*\n$" # checks if a line is empty
TAGGED_COMMA = "\s,\/,(?=\s)"  # selects commas in the pos tagged o/p of parser ..should we remove '(single quotes) as well ? 

def extract_np():
	


def clean_str(line):
	line = line.lstrip()
	line = line.rstrip(" \n")
	return line
	
def remove_tagged_comma(line):
	line = re.sub(TAGGED_COMMA,"",line)
	return line 

def isEmpty(line):	
	m = re.match(EMPTY_LINE,line)
	if(m):
		return True
	return False	
# returns (dict,dict,dict) i.e all the different kinds of parse for all the liens  
def pprocess_pfile(filename):

	## initialize three dicts
	pos_tags_dict = {}
	parse_tree_dict = {}
	parse_dependency_dict = {}

	# read  the pos tagged sentence and tokenize the sentence  
	fd = open(filename)
	curr_loc_read = 0 
	lines_processed = 0 
	dependency_list = [] 
	for line in fd:
		if(isEmpty(line)):
			continue
		line = clean_str(line)
		# first line is pos tagged 
		if(curr_loc_read==0):
			line = remove_tagged_comma(line) 
			# split line into word tokens 
			words_list = line.split("\s")
			pos_tags_dict[lines_processed] = words_list 
			current_loc_read += 1 
		elif(current_loc_read==1):
			parse_tree_dict[lines_processed] = line 
			current_loc_read += 1 
		elif(current_loc_read==2):
			#do something 
			if((m=re.match("***",line))):
					parse_dependency_dict[lines_processed]=dependency_list # makes a copy
					# moves to a new line
					lines_processed += 1
					# initialize vars for next line 
					current_loc_read = 0 
					dependency_list = []
			else:		
				dependency_list.append(line)	
			
	fd.close()
	return (pos_tags_dict,parse_tree_dict,parse_dependency_dict)

def main():
	for root, dirs, files in os.walk(PATH):
		for file in files:
			(meta,main) = pprocess_file(root + file)

if __name__== '__main__':
	# do something 
	main()

