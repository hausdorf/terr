import re
import sys

DEBUG = False
## BEGIN REGEX 
## TODO HAVE NOT HANDLED PARTICLES RP  ( RP and IN can be confused rite ? ) 
## VICTIM PATTERNS 
##v_1 = "<NP> VBD VBN"  # i think the stanford parser messes up on 
v_1_pattern = "\[.*?\]\/NP\s+(\w+?)\/VBD\s+(\w+?)\/VBN" # change \w+ from .*?
v_1_patt = re.compile(v_1_pattern)
##v_2 = "<NP> VBD NN*"  # i think the stanford parser messes up on 
v_2_pattern = "\[.*?\]\/NP\s+(\w+?)\/VBD\s+(\w+?)\/NN\w{0,2}\s+"
v_2_patt = re.compile(v_2_pattern)
##v_3 = "VBD <NP>"  # the heuristic says passive voice but replacing this with VBD i.e killed VICTIM 
v_3_pattern = "\s+(\w+?)\/VBD\s+\[.*?\]\/NP"
v_3_patt = re.compile(v_3_pattern)
##v_4 = "TO VB"  # vb is the base form of the berb 
v_4_pattern = "\s+(\w+?)\/VB\w{0,1}\s+(\w+?)\/TO\s+(\w+?)\/VB\s+\[.*?\]\/NP"  # vb is the base form of the berb 
v_4_patt = re.compile(v_4_pattern)
##v_5 = "VBG <NP>"# gerund 
v_5_pattern = "\s+(\w+?)\/VBG\s+\[.*?\]\/NP"# gerund 
v_5_patt = re.compile(v_5_pattern)
##v_6 = "noun VBD <NP>" # 
v_6_pattern = "\s+(\w+?)\/NN\w{0,2}\s+(\w+?)\/VBD\s+\[.*?\]\/NP" # 
v_6_patt = re.compile(v_6_pattern)


## PERP PATTERNS 

##perp_1 = "<NP> VBD"  # VBD past tense // it says active verb ? 
#perp_1_pattern = "\(.*?\)\/NP\s+(.*?)\/VB{0,1}"
perp_1_pattern = "\(.*?\)\/NP\s+(\w+?)\/VB{0,1}"
perp_1_patt = re.compile(perp_1_pattern)
##perp_2 = "<NP> word TO VB"
#perp_2_pattern = "\(.*?\)\/NP\s+(.*?)\/VBD\s+(.*?)\/TO\s+(.*?)\/VB" #e.g <perp> attempted to kill
perp_2_pattern = "\(.*?\)\/NP\s+(\w+?)\/VBD\s+(\w+?)\/TO\s+(\w+?)\/VB" #e.g <perp> attempted to kill
perp_2_patt = re.compile(perp_2_pattern)

## TARGET PATTERNS 
##target_1 = "word(verb) TO VB <NP>"  # VB is the base verb phrase # tried to attack XYZ
#target_1_pattern = "\s+(.*?)\/VB{0,1}\s+(.*?)\/TO\s+(.*?)\/VB\s+\(.*?\)\/NP"  # VB is the base verb phrase
target_1_pattern = "\s+(\w+?)\/VB{0,1}\s+(\w+?)\/TO\s+(\w+?)\/VB\s+\(.*?\)\/NP"  # VB is the base verb phrase
target_1_patt = re.compile(target_1_pattern)
##target_2 = "\s+(.*?)\/VBD <TARGET>"
#target_2_pattern = "\s+(.*?)\/VB{0,1}\s+\(.*?\)\/NP"
target_2_pattern = "\s+(\w+?)\/VB{0,1}\s+\(.*?\)\/NP"
target_2_patt  = re.compile(target_2_pattern)
##target_3 = "noun prep <NP>"
#target_3_pattern = "\s+(.*?)\/NN{0,2}\s+(.*?)\/IN\s+\(.*?\)\/NP" ## ? check 
target_3_pattern = "\s+(\w+?)\/NN{0,2}\s+(\w+?)\/IN\s+\(.*?\)\/NP" ## ? check 
target_3_patt = re.compile(target_3_pattern)
##target_4 = "VBD VB prep <NP>"
#target_4_pattern = "\s+(.*?)\/VBD\s+(.*?)\/VB\s+(.*?)\/prep\s+\(.*?\)\/NP"
target_4_pattern = "\s+(\w+?)\/VBD\s+(\w+?)\/VB\s+(\w+?)\/prep\s+\(.*?\)\/NP"
target_4_patt    = re.compile(target_4_pattern)


## WEAPON PATTERNS 

#w_1 = "VBA with(prep) <NP>"  # VBA means all verbs does not have ( rule is for active verbs only) ?
#w_1_pattern = "\s+(.*?)\/VB{0,1}\s+(.*?)\/IN\s+\(.*?\)\/NP"
w_1_pattern = "\s+(\w+?)\/VB{0,1}\s+(\w+?)\/IN\s+\(.*?\)\/NP"
w_1_patt    = re.compile(w_1_pattern)


## END REGEX 
def get_instrument_pattern():
	instrument_heuristics = [] 

def get_perp_pattern():

	perp_heuristics = [] 
		
def get_target_pattern():

	target_heuristics = [] 
	
def get_victim_pattern(sent):
	
	extracted_patt = [] 
	patt_type="<VICTIM>"
	# fpattern i.e NP in the front 
	m = v_1_patt.findall(sent) 
	if m:
		temp_list = ret_fpatterns(patt_type,m)
		extracted_patt += temp_list
	# fpattern i.e NP in the front /beginning of the sent 
	m = v_2_patt.findall(sent)
	if m:
		temp_list = ret_fpatterns(patt_type,m)
		extracted_patt += temp_list
	# v3 is bpattern i.e NP at the end 	of the sent : one word i.e str
	m = v_3_patt.findall(sent)	
	if m:
		temp_list = ret_bpatterns(patt_type,m)
		extracted_patt += temp_list
	# v4 is bpattern i.e NP at the end 	of the sent : Each pattern tuple of len 3 
	m = v_4_patt.findall(sent)
	if m:
		temp_list = ret_bpatterns(patt_type,m)
		extracted_patt += temp_list
	# v5 is bpattern  : Each pattern is one string 	
	m = v_5_patt.findall(sent)
	if m:
		temp_list = ret_bpatterns(patt_type,m)
		extracted_patt += temp_list
	# v6 is bpattern  : Each pattern is two tuple  	
	m = v_6_patt.findall(sent)
	if m:
		temp_list = ret_bpatterns(patt_type,m)
		extracted_patt += temp_list
	if DEBUG:	
		print "TEST ",extracted_patt
	return extracted_patt 
# m is a list of tuples i.e the patterns extracted 	
def ret_fpatterns(patt_type,m):
	temp_list = [] 
	# process each match one at a time 
	for o in m:
		ext_patt=patt_type
		# case where one pattern extracted # o is string 
		if(isinstance(o,basestring)):
				ext_patt += " "+o  
				temp_list.append(ext_patt)
		else:
		# case where two patterns need to be extracted # o is tuple 
			for i in xrange(len(o)):
				ext_patt += " "+o[i] 
			temp_list.append(ext_patt)
	return temp_list
def ret_bpatterns(patt_type,m):
	temp_list = []
	# process each match one at a time 
	for o in m:
		ext_patt=""
		# case where one pattern extracted # o is string 
		if(isinstance(o,basestring)):
			ext_patt += " "+o 
			ext_patt  = ext_patt.lstrip()	
			ext_patt += " "+patt_type
			temp_list.append(ext_patt)
		else:
		# case where two patterns need to be extracted # o is tuple 
			for i in xrange(len(o)):
				ext_patt += " "+o[i]
			# once we have the whole string do the foll 	
			ext_patt  = ext_patt.lstrip()	
			ext_patt += " "+patt_type
			temp_list.append(ext_patt)
	return temp_list
# do we want to return all the patterns + (NP+filename)  in 4 dicts # havin an NP will help in judging the results  	
def match_rules(sent):
	#get instance patterns for victims 
	victim_pattern_list = get_victim_pattern(sent)
	return victim_pattern_list
	target_pattern_list = get_target_pattern()
	instrument_pattern_list = get_instrument_pattern()
	perp_pattern_list = get_perp_pattern()
	
