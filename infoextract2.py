import sys,os
import re
import incident_predictor
import preprocess
import utility
import pattern_extractor
import matching
from meta import proc_meta

#DEBUG=True
DEBUG=False

# REGEX PATTERNS 
PATTERN = "((DEV|TST1|TST2)\-MUC\d\-\d{4})"
EMPTY_LINE  = "\s*\n\s*$" # checks if a line is empty
NEWLINE = "\n(?=.)" # selects a new line if it occurs before some char
COLL_SPACES = "\s+"
SPACES_REPL = " "




if(len(sys.argv) == 1):
	print ("please enter an input file ")
	sys.exit()

input_file = sys.argv[1]

output_file = input_file + ".templates" 
# opening the output file for writing 
f_out = open(output_file,'w')


# THIS should handle multiple line for one slot as well  	 
def print_out(id_name,incident,weapon,perp_indiv,perp_org,target,victim):

	# now write output to this file  
	f_out.write("ID:            "+id_name+"\n")
	f_out.write("INCIDENT:      "+incident+"\n")
	f_out.write("WEAPON:        "+weapon+"\n")
	f_out.write("PERP INDIV:    "+perp_indiv+"\n")
	f_out.write("PERP ORG:      "+perp_org+"\n")
	f_out.write("TARGET:        "+target+"\n")
	f_out.write("VICTIM:        "+victim+"\n")
	f_out.write("\n")

# the main function that processes each MUC text and produces the answer key 
def process_input_text(file_text,id_name):
	# remove the \n from in between the lines
	(meta,main) = preprocess.split_text(file_text)
	if (not meta):
		print "ERROR IN SPLITTING MAIN AND META"
		return 
	if(not main):
		print "ERROR IN SPLITTING MAIN AND META"
		return
	#print proc_meta(meta)
		

	file_text = re.sub(NEWLINE," ",main)
	file_text_list = file_text.split('\n')
	if(DEBUG):
		print ("processing text",main) 
		print ("")
	
	# pass file text instead of main in infoextract2.py 	
	incident_type = incident_predictor.get_predicted_event(main) 
	# TODO NER CALL A FUNCTION THAT returns NER DICT

	# open file containing victim patterns
	text = utility.f_read('victim_out_patterns_regex2')
  	victim_patt_lines = text.split('\n')
	# ALGO read one line at a time .. if it matches one of the patterns then parse that line and do ur thing 


	# READ EACH LINE IN THE from input file   
	for line in file_text_list:
		line = line.strip()
		if(not line):
			continue
		#print "processing line",line	
		# make sure no consecutive white spaces in ur line	
		input_line = re.sub(COLL_SPACES,SPACES_REPL,line)	
		victim_list = pattern_extractor.get_victims(input_line,victim_patt_lines)
		if victim_list:
			print victim_list
			print "###########################"
		# now use algorithms to clean this list and to remove redundant stuff 
		# get target_list 
			
	#dict_out    = matching.match(parsed_text)
	#print ("")
	#print_out(id_name,incident_type,dict_out['WEAPON'],dict_out['PERP INDIV'],dict_out['PERP ORG'],dict_out['TARGET'],dict_out['VICTIM'])

def	process_file():
	# compile the regex  patter 
	compiled_pattern = re.compile(PATTERN,re.IGNORECASE)
	# open file
	f = open(input_file)	
	# initialize vars 
	file_text = ""
	file_count = 0
	id_name_old = ""
	line = f.readline()
	while(line != ""):
		m = compiled_pattern.search(line)
		if(m):
			file_count += 1 
			# store starting patter 
			id_name_new = m.group(1) # group(0) is the whole string 
			if(file_count == 1):
				id_name_old	= id_name_new
			elif(file_count > 1):
				# process old text 
				ret = process_input_text(file_text,id_name_old)
				id_name_old = id_name_new
				file_text = ""
		else:		
			# start collecting new line in file_text
			file_text = file_text + line
		line = f.readline()
	# captures last text 
	ret = process_input_text(file_text,id_name_old)
	f.close()

#return text

def main():
	process_file()
	# close the answer.templates file 
	f_out.close()


if __name__== "__main__":
	main()
