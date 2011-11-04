import sys
import re

DEBUG=True
PATTERN = "((DEV|TST1|TST2)\-MUC\d\-\d{4})"
EMPTY_LINE  = "\s*\n\s*$" # checks if a line is empty

input_file = sys.argv[1]
output_file = input_file + ".templates" 
# opening the output file for writing 
f_out = open(output_file,'w')


# THIS should handle multiple line for one slot as well  	 
def print_out(id_name,incident,weapon,perp_indiv,perp_org,target,victim):

	# now write output to this file  
	print "ID:            "+id_name
	print "INCIDENT:      "+incident
	print "WEAPON:        "+weapon
	print "PERP INDIV:    "+perp_indiv
	print "PERP ORG:      "+perp_org
	print "TARGET:        "+target
	print "VICTIM:        "+victim
	print ""

# the main function that processes each MUC text and produces the answer key 
def process_input_text(file_text,id_name):
	print "processing text",file_text 
	print ""
	print_out(id_name,"-","-","-","-","-","-")



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
				print "**********************************"
				id_name_old = id_name_new
				file_text = ""
		else:		
			# start collecting new line in file_text
			file_text = file_text + line
		line = f.readline()
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
