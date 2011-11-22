import re
import sys 
import utility 
PATT = "#"
def get_hash_lines(text):
	lines = text.split('\n')
	out_list = []
	for line in lines:
		# handle empty lines 
		if(not line):
			print "line",line
			print "skipped a line"
			continue 
		m = re.match(PATT,line)
		if(m):
			line = line.lstrip('#')
			line = line.strip()
			out_list.append(line)
	# sort list so that we can identify duplicate patterns 		
	out_list.sort()
	return out_list

if (__name__=="__main__"):

	 filename = sys.argv[1]
	 print filename
	 text  = utility.f_read(filename)
	 out_lines = get_hash_lines(text)
	 filename_n = filename+"_patterns"
	 f_w = open(filename_n,'w')
	 for line in out_lines:
	 	s = "%s"%(line,)
	 	f_w.write(s)
		f_w.write("\n")
	 f_w.close()	

