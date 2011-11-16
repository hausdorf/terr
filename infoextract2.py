import sys,os
import re
import incident_predictor
import matching

DEBUG=False
PATTERN = "((DEV|TST1|TST2)\-MUC\d\-\d{4})"
EMPTY_LINE  = "\s*\n\s*$" # checks if a line is empty
NEWLINE = "\n(?=.)" # selects a new line if it occurs before some char

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
	file_text = re.sub(NEWLINE," ",file_text)
	if(DEBUG):
		print ("processing text",file_text) 
		print ("")
		
	incident_type = incident_predictor.get_predicted_event(file_text) 
	parsed_text = parse_file(file_text)
	# call process parsed here to get the processed part we want TODO
	#print ("txt ",parsed_text)
	dict_out    = matching.match(parsed_text)
	#print ("")
	# call alex's code 
	print_out(id_name,incident_type,dict_out['WEAPON'],dict_out['PERP INDIV'],dict_out['PERP ORG'],dict_out['TARGET'],dict_out['VICTIM'])

def parse_file(text):

	fj = open("text.txt",'w')
	fj.write(text)
	fj.close()
	os.system("java -mx1000m -cp .:./stanford-parser.jar ParseFast ")
	fo = open("text_out.txt")
	txt = fo.read()
	return txt 
	# delete this text file 
	# return success or failure 

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
	# close the answer.templates file 
	f_out.close()


if __name__== "__main__":
	main()
