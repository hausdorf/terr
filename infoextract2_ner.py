import sys,os
import re
import incident_predictor
import preprocess
import utility
import pattern_extractor
import matching
import process_ner 
from meta import proc_meta

#DEBUG=True
DEBUG=False

# REGEX PATTERNS 
PATTERN = "((DEV|TST1|TST2)\-MUC\d\-\d{4})"
EMPTY_LINE  = "\s*\n\s*$" # checks if a line is empty
NEWLINE = "\n(?=.)" # selects a new line if it occurs before some char
COLL_SPACES = "\s+"
SPACES_REPL = " "
SPATT = "'S"



if(len(sys.argv) == 1):
	print ("please enter an input file ")
	sys.exit()

input_file = sys.argv[1]

output_file = input_file + ".templates" 
# opening the output file for writing 
f_out = open(output_file,'w')


def print_outf(id_name,incident,weapon_l,perp_indiv_l,perp_org_l,target_l,victim_l):


	f_out.write("ID:            "+id_name+"\n")
	f_out.write("INCIDENT:      "+incident+"\n")
	if weapon_l:
		count = 0 
		for w in weapon_l:
			if(count==0):
				s = "WEAPON:        %s\n"%(w)
				count = 1
			else:
				s = "               %s\n"%(w)
			f_out.write(s)
	else:		 
		s = "WEAPON:        -\n"
		f_out.write(s)

	
	if perp_indiv_l:
		count = 0 
		for pi in perp_indiv_l:
			if(count==0):
				s = "PERP INDIV:    %s\n"%(pi)
				count = 1
			else:
				s = "               %s\n"%(pi)
			f_out.write(s)
	else:	 
		s = "PERP INDIV:    -\n"
		f_out.write(s)

	if perp_org_l:
		count =0 
		for po in perp_org_l:
			if(count==0):
				s = "PERP ORG:      %s\n"%(po)
				count = 1
			else:
				s = "               %s\n"%(po)
			f_out.write(s)
	else:
		s = "PERP ORG:      -\n"
		f_out.write(s)
	if target_l:
		count = 0 
		for t in target_l:
			if(count==0):
				s = "TARGET:        %s\n"%(t)
				count = 1
			else:
				s = "               %s\n"%(t)
			f_out.write(s)	
	else:
		s = "TARGET:        -\n"
		f_out.write(s)

	if victim_l:
		count =0 
		for v in victim_l:
			if(count==0):
				s = "VICTIM:        %s\n"%(v)
				count = 1
			else:
				s = "               %s\n"%(v)
			f_out.write(s)
	else:		 
		s = "VICTIM:        -\n"
		f_out.write(s)
	f_out.write("\n")
			 
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
		
	temp_victim_list = []
	final_victim_set =set([])
	temp_target_list = []
	final_target_set = set([])
	temp_perpi_list = []
	final_perpi_set = set([])

	file_text = re.sub(NEWLINE," ",main)
	file_text_list = file_text.split('\n')
	if(DEBUG):
		print ("processing text",main) 
		print ("")
	
	# pass file text instead of main in infoextract2.py 	
	incident_type = incident_predictor.get_predicted_event(main) 
	# TODO NER CALL A FUNCTION THAT returns NER DICT
	ner_tagged_text = process_ner.java_ner_tagger(file_text)
	if (ner_tagged_text):
		ner_tagged_text.strip()
		if(ner_tagged_text):
			ner_dict = process_ner.get_entities()

	if(ner_dict):
		print ner_dict
	# open file containing victim patterns
	text = utility.f_read('victim_out_patterns_regex2')
  	victim_patt_lines = text.split('\n')
	text = utility.f_read('target_out_patterns_regex2') # has only back patt
  	target_patt_lines = text.split('\n')
	text = utility.f_read('perp_out_patterns_regex2') # has both front and back patterns 
  	perp_patt_lines = text.split('\n')
	# ALGO read one line at a time .. if it matches one of the patterns then parse that line and do ur thing 


	# READ EACH LINE IN THE from input file   
	for line in file_text_list:
		line = line.strip()
		if(not line):
			continue

		# split each line into several sentences
		sents = utility.sent_splitter(line)
		for sent in sents:
			#print "processing line",line	
			# make sure no consecutive white spaces in ur line
			sent  = sent.strip()
			# TODO remove 's and `` from sentence remove `` as well ?
			sent = re.sub(SPATT,"",sent)			
			input_line = re.sub(COLL_SPACES,SPACES_REPL,sent)
			temp_victim_list = pattern_extractor.get_victims(input_line,victim_patt_lines)
			if temp_victim_list:
				for victim in temp_victim_list:
					victim  = victim.strip()
					if victim:
						final_victim_set.add(victim)
			# TARGET LIST
			temp_target_list = pattern_extractor.get_targets(input_line,target_patt_lines)
			if temp_target_list:
				for target in temp_target_list:
					target = target.strip()
					if target:
						final_target_set.add(target)
			# PERPI LIST
			temp_perpi_list = pattern_extractor.get_perpi(input_line,perp_patt_lines)
			if temp_perpi_list:
				for perp in temp_perpi_list:
					perp = perp.strip()
					if perp:
						final_perpi_set.add(perp)


			# now use algorithms to clean this list and to remove redundant stuff 
			# get target_list
	# a victim cannot be an org or location ?? has to be  a person 

	#subset removal
	v_new_list = list(final_victim_set)
	v_new_list  = utility.remove_subsets(v_new_list)	
	print "after subset removal"
	print v_new_list
	v_new_list = utility.remove_syn(v_new_list)
	print "after duplicate removal for ",id_name
	print v_new_list

	v_new_list = utility.rmv_flagged_np(v_new_list,'victim')# e.g headquarters
	print "after removing flag words   for ",id_name
	print v_new_list

	v_new_list = utility.first_word_flag(v_new_list,'victim')# e.g suspects 
	print "after one removing first word flags  for ",id_name
	print v_new_list

	v_new_list = utility.first_word_rmv(v_new_list)# e.g COLONEL REPORTER
	print "after removing first title words like COLONEL etc ",id_name
	print v_new_list

	v_new_list = utility.one_word_cleaner(v_new_list)
	print "after one word and digit removal for ",id_name
	print v_new_list
	v_new_list = utility.victim_hacks(v_new_list)# e.g hacks
	print "after adding some hacks make unique",id_name
	print v_new_list
	print "###########################"

	# a target cannot be a a person or location 

	t_new_list  = list(final_target_set)
	t_new_list  = utility.remove_subsets(t_new_list)	
	print "after subset removal"
	print t_new_list
	t_new_list = utility.remove_syn(t_new_list)
	print "after duplicate removal"
	print t_new_list


	t_new_list = utility.rmv_flagged_np(t_new_list,'target')# e.g headquarters
	print "after removing flag words   for ",id_name
	print t_new_list
	t_new_list = utility.first_word_flag(t_new_list,'target')# e.g suspects 
	print "after one removing first word flags  for ",id_name
	print t_new_list

	t_new_list = utility.one_word_cleaner(t_new_list)
	print "###Final after one word removal for ",id_name
	print t_new_list
	#print "###########################"


	# NER HINT a perpetrator cannot be a LOCATION or an org ??

	p_new_list  = list(final_perpi_set)
	p_new_list  = utility.remove_subsets(p_new_list)	
	print "after subset removal"
	print p_new_list
	p_new_list = utility.remove_syn(p_new_list)
	print "after duplicate removal"
	print p_new_list

	p_new_list = utility.rmv_flagged_np(p_new_list,'perp')# e.g headquarters
	print "after removing flag words   for ",id_name
	print p_new_list
	p_new_list = utility.first_word_flag(p_new_list,'perp')# e.g suspects 
	print "after one removing first word flags  for ",id_name
	print p_new_list

	p_new_list = utility.one_word_cleaner(p_new_list)
	print " Final after one word and digit removal for ",id_name
	print p_new_list
	#print "###########################"


	#dict_out    = matching.match(parsed_text)
	#print ("")
	print_outf(id_name,incident_type,[],p_new_list,[],t_new_list,v_new_list)

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
