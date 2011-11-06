import re
import sys
import os
from stat import *
import preprocess

#
DEBUG = False
# INPUT DIRS 
INPUT_DIR = 'developset/pptexts/'       # Processed data

# REGEX 
NEWLINE = "\n(?=.)" # selects a new line if it occurs before some char


# returns the k,v pair with max key
def get_max_kv(event_dict):

	max_v = 0 
	max_k = 0 
	for k,v in event_dict.iteritems():
		if( v > max_v ):
			max_v = v
			max_k = k 
	return (max_k,max_v)		

# currently using arson and burn ... could search for set the place on fire , or make a list of all possible things 
def get_arson_count(text):

	count = 0 
	m = re.findall("arson(?=\s)",text,re.IGNORECASE) # positive lookahead 
	if(m):
		count = len(m)
	m = re.findall("(?<=\s)burn",text,re.IGNORECASE)  # positive lookbehind 
	if(m):
		count += len(m)
	return count

# search for attack 
def get_attack_count(text):
	count = 0
	## AM NOT ADDING DEAD HERE AS LOTS OF INCEDENTS CAN HAVE DEAD ???? also 1013 has machinegunned ?? should we have gunned ? terrorist gunned ?
	## DEath of jesuit priest is a common occurence !!
	m = re.findall("(?<=\s)attack",text,re.IGNORECASE)
	if(m):
		count = len(m)
	m = re.findall("(?<=\s)murder",text,re.IGNORECASE)
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)kill",text,re.IGNORECASE) ## ambiguous ?? could conflict with bomb attack 
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)shot",text,re.IGNORECASE)
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)assassinat",text,re.IGNORECASE)
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)massacre",text,re.IGNORECASE)
	if(m):
		count += len(m)
	return count 

# search for bomb , l8r look for blew up 
def get_bomb_count(text):
	count = 0 
	m = re.findall("(?<=\s)bomb",text,re.IGNORECASE)
	if(m):
		count = len(m)
	m = re.findall("(?<=\s)explod",text,re.IGNORECASE)
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)explos",text,re.IGNORECASE)
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)dynamite",text,re.IGNORECASE)
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)blowing\-up",text,re.IGNORECASE)
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)blew\-up",text,re.IGNORECASE)
	if(m):
		count += len(m)

	return count

def get_kidnap_count(text):
	count = 0 
	m = re.findall("(?<=\s)kidnap",text,re.IGNORECASE)
	if(m):
		count = len(m)
	return count 

def get_robbery_count(text):
	count = 0 
	m = re.findall("(?<=\s)stole(?=\s)",text,re.IGNORECASE) # look ahead and look behind 
	if(m):
		count = len(m) 
	m = re.findall("(?<=\s)steal",text,re.IGNORECASE) # look behind   
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)robbery(?=\s)",text,re.IGNORECASE) # look ahead and look behind
	if(m):
		count += len(m) 
	m = re.findall("(?<=\s)robbed(?=\s)",text,re.IGNORECASE) # look ahead and look behind 
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)loot",text,re.IGNORECASE) # look ahead and look behind 
	if(m):
		count += len(m)
	return count 
		
def get_predicted_event(text):

	# init dictionary 
	event_type = {} 
	# arson count 
	event_type['arson'] = get_arson_count(text) 
	# attack count  
	event_type['attack'] = get_attack_count(text)
	# bomb count 
	event_type['bombing'] = get_bomb_count(text)
	# kidnap count 
	event_type['kidnapping'] = get_kidnap_count(text)
	# robbery 
	event_type['robbery'] = get_robbery_count(text)

	# TODO 
	# get max key with max value  .. CURRENTLY WE DONT HANDLE TIES 
	key,value = get_max_kv(event_type)
	# return max count event  
	if(key == 0):
		if(DEBUG):
			event = '-' # SHOULD WE SET ATTACK AS DEFAULT ..BECAUSE ELLEN SAID THAT EVERY DOC HAS ONE TERRORIST ATTACK..Also the docs with attack default are the most difficult ones for other slots too 
		event = 'attack'	
	else :
	  	event = key 

	return event

# Preprocess that file!
def pprocess_file(filename):
	text = preprocess.f_read(filename)
	return text 


def main():
	
	listing = os.listdir(INPUT_DIR)

	for file in listing :
		pathname = os.path.join(INPUT_DIR, file)
		mode = os.stat(pathname).st_mode
		if S_ISDIR(mode):
			continue 
		# if file name starts with meta skip 
		if(re.match("meta_",file) or re.match("\.",file)):
			continue 
		text = pprocess_file(pathname)
		# remove all new lines in this text == make it one big string  
		text = re.sub(NEWLINE," ",text)
		event_type = get_predicted_event(text)
		print "event type for the file ",file," is = ",event_type 


if __name__ == "__main__" :

	main()
	
