import re
import sys
import utility

DEBUG = False
## BEGIN REGEX 
## TODO HAVE NOT HANDLED PARTICLES RP  ( RP and IN can be confused rite ? ) 
## VICTIM PATTERNS 

v_1_pattern_str = "NP VBD VBN"
v_1_pattern = "(\[.*?\])\/NP\s+(\w+?)\/VBD\s+(\w+?)\/VBN" # change \w+ from .*?
v_1_patt = re.compile(v_1_pattern)

v_2_pattern_str = "NP VBD NN"	
v_2_pattern = "(\[.*?\])\/NP\s+(\w+?)\/VBD\s+(\[.*?\])\/NP\s+"
v_2_patt = re.compile(v_2_pattern)

v_3_pattern_str = "VBD NP"
v_3_pattern = "\s+(\w+?)\/VBD\s+(\[.*?\])\/NP"
v_3_patt = re.compile(v_3_pattern)

v_4_pattern_str = "VB(all) TO VB NP"
v_4_pattern = "\s+(\w+?)\/VB\w{0,1}\s+(\w+?)\/TO\s+(\w+?)\/VB\s+(\[.*?\])\/NP"  # vb is the base form of the berb 
v_4_patt = re.compile(v_4_pattern)

v_5_pattern_str = "VBG NP"
v_5_pattern = "\s+(\w+?)\/VBG\s+(\[.*?\])\/NP"# gerund 
v_5_patt = re.compile(v_5_pattern)

v_6_pattern_str = "NN VBD NP"
v_6_pattern = "(\[.*?\])\/NP\s+(\w+?)\/VBD\s+(\[.*?\])\/NP" # fatality was victim  
v_6_patt = re.compile(v_6_pattern)


## PERP PATTERNS 

p_1_pattern_str = "NP VB(all)"	
p_1_pattern = "(\[.*?\])\/NP\s+(\w+?)\/VB\w{0,1}"
p_1_patt = re.compile(p_1_pattern)

p_2_pattern_str = "NP VBD TO VB"	
p_2_pattern = "(\[.*?\])\/NP\s+(\w+?)\/VBD\s+(\w+?)\/TO\s+(\w+?)\/VB" #e.g <perp> attempted to kill
p_2_patt = re.compile(p_2_pattern)


## WEAPON PATTERNS 

w_1_pattern_str = "VB IN NP"	
w_1_pattern = "\s+(\w+?)\/VB\w{0,1}\s+(\w+?)\/IN\s+(\[.*?\])\/NP"
w_1_patt    = re.compile(w_1_pattern)


## END REGEX 
def get_instrument_pattern(sent):

	extracted_patt = [] 
	patt_type="<WEAPON>"
	m = w_1_patt.findall(sent) 
	if m:
		temp_list = ret_bpatterns(patt_type,m,w_1_pattern_str)
		extracted_patt += temp_list

	# return list
	return extracted_patt 	

def get_perp_pattern(sent):

	extracted_patt = [] 
	patt_type="<PERP INDIV>"
	m = p_1_patt.findall(sent) 
	if m:
		temp_list = ret_fpatterns(patt_type,m,p_1_pattern_str)
		extracted_patt += temp_list
	m = p_2_patt.findall(sent) 
	if m:
		temp_list = ret_fpatterns(patt_type,m,p_2_pattern_str)
		extracted_patt += temp_list

	# return list 	
	return extracted_patt 	
		
def get_victim_pattern(sent):
	
	extracted_patt = [] 
	patt_type="<VICTIM>"
	# fpattern i.e NP in the front 
	m = v_1_patt.findall(sent) 
	if m:
		temp_list = ret_fpatterns(patt_type,m,v_1_pattern_str)
		extracted_patt += temp_list
	# fpattern i.e NP in the front /beginning of the sent 
	m = v_2_patt.findall(sent)
	if m:
		temp_list = ret_fpatterns(patt_type,m,v_2_pattern_str)
		extracted_patt += temp_list
	# v3 is bpattern i.e NP at the end 	of the sent : one word i.e str
	m = v_3_patt.findall(sent)	
	if m:
		temp_list = ret_bpatterns(patt_type,m,v_3_pattern_str)
		extracted_patt += temp_list
	# v4 is bpattern i.e NP at the end 	of the sent : Each pattern tuple of len 3 
	m = v_4_patt.findall(sent)
	if m:
		temp_list = ret_bpatterns(patt_type,m,v_4_pattern_str)
		extracted_patt += temp_list
	# v5 is bpattern  : Each pattern is one string 	
	m = v_5_patt.findall(sent)
	if m:
		temp_list = ret_bpatterns(patt_type,m,v_5_pattern_str)
		extracted_patt += temp_list
	# v6 is bpattern  : Each pattern is two tuple  	
	m = v_6_patt.findall(sent)
	if m:
		temp_list = ret_bpatterns(patt_type,m,v_6_pattern_str)
		extracted_patt += temp_list
	if DEBUG:	
		print "Extracted Victim phrase list  ",extracted_patt
	return extracted_patt 
# m is a list of tuples i.e the patterns extracted 	

def ret_fpatterns(patt_type,m,patt_str):
	temp_list = [] 
	# process each match one at a time 
	for grp in m:
		ext_patt=patt_type
		# the first member of tuple is NP extract that 
		np = grp[0]
		ext_patt = patt_str+":"+ext_patt
		# copy the remaing tuple so that it can be processed separately
		o = grp[1:]
		# o is always a tuple 
		for i in xrange(len(o)):
			ext_patt += " "+o[i]
		if(patt_str == "NP VBD NN"):
			ext_patt = remove_npstuff(ext_patt)
		# ADD the NP: thing to the extracted pattern  now the patt becomes NP:PATT_STR:EXTRACTED_PATT 
		ext_patt = np +":" + ext_patt	
		temp_list.append(ext_patt)
	return temp_list
   
def ret_bpatterns(patt_type,m,patt_str):
	temp_list = []
	# process each match one at a time 
	for grp in m:
		ext_patt=""
		# np is the last index 
		np = grp[-1]
		ext_patt =  patt_str + ":"+ext_patt
		# copy everything except the last index to 
		o = grp[:-1]
		# o is tuple 
		for i in xrange(len(o)):
			ext_patt += " "+o[i]
		# once we have the whole string do the foll 	
		if(patt_str == "NN VBD NP"):
			ext_patt = remove_npstuff(ext_patt)
		ext_patt += " "+patt_type
		# ADD the NP: thing to the extracted pattern  now the patt becomes NP:PATT_STR:EXTRACTED_PATT 
		ext_patt = np +":" + ext_patt	
		temp_list.append(ext_patt)
	return temp_list

def remove_npstuff(sent):
	extrcts = []

	spl = re.split('(\[.*?\])', sent)
	# loop over all whole extracted pattern and find the []/NP pattern for cleaning 
	for e in spl:

		lspl = len(e)
		if lspl < 4:
			extrcts.append(e)
		elif e[0] == '[' and e[-1] == ']':
			extrct = utility.np_cleaner(e)
			if extrct != '':
				extrcts.append(extrct)
		else:
			extrcts.append(e)
	return ' '.join(extrcts)	

# do we want to return all the patterns + (NP+filename)  in 4 dicts # havin an NP will help in judging the results  	
def match_rules(sent):
	#get instance patterns for victims 
	victim_pattern_list = get_victim_pattern(sent)
	inst_pattern_list = get_instrument_pattern(sent)
	perp_pattern_list = get_perp_pattern(sent)
	return (victim_pattern_list,inst_pattern_list,perp_pattern_list)
	
