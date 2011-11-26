import sys
import re
import incident_predictor
import preprocess
from answer_stats import answr_dict, get_weapon, get_perp_indiv, get_perp_org, get_target, get_victim

DEBUG=False
PATTERN = "((DEV|TST1|TST2)\-MUC\d\-\d{4})"
EMPTY_LINE  = "\s*\n\s*$" # checks if a line is empty
NEWLINE = "\n(?=.)" # selects a new line if it occurs before some char

KEY = None

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


def make_key():
	global KEY
	f = open('developset/test_set/answerkeys/AGGREGATE')

	key = {}
	lastid = ''
	for line in f.readlines():
		spl = line.split(':')
		if spl[0] == 'ID':
			lastid = spl[1].strip()

		if spl[0] == 'WEAPON':
			key[lastid] = spl[1].strip()

	KEY = key

# the main function that processes each MUC text and produces the answer key 
def process_input_text(file_text,id_name):
	global KEY

	(meta,main) = preprocess.split_text(file_text)
	if(not meta):
		print "ERROR IN SPLITTING MAIN AND META"
		return 
	if(not main):
		print "ERROR IN SPLITTING MAIN AND META"
		return

	file_text = re.sub(NEWLINE," ",main)
	if(DEBUG):
		print ("processing text",main) 
		print ("")

	d = answr_dict()

	if not KEY:
		make_key()

	weapon = get_weapon(file_text, d)
	print id_name
	print 'C', KEY[id_name], '\n', 'D', weapon
	print
	#perpindiv = get_perp_indiv(file_text, d)
	perpindiv = '-'
	#perporg = get_perp_org(file_text, d)
	perporg = '-'
	#target = get_target(file_text, d)
	target = '-'
	#victim = get_victim(file_text, d)
	victim = '-'

	incident_type = incident_predictor.get_predicted_event(main) 
	print_out(id_name,incident_type,weapon,perpindiv,perporg,target,victim)



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
	# read the file name
	process_file()
	f_out.close()
	# find the start 

	#  run ur basic algo 

if __name__== "__main__":
	main()
