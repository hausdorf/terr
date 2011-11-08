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
	m = re.findall("arson(?=\s)",text,re.IGNORECASE|re.MULTILINE) # positive lookahead 
	if(m):
		count = 4*len(m)
	m = re.findall("(?<=\s)burn",text,re.IGNORECASE|re.MULTILINE)  # positive lookbehind 
	if(m):
		count += (4)*len(m)
	if(DEBUG):
		print (" CAME HERE ************************************ count ",count)
	return count

# search for attack 
def get_attack_count(text):
	count = 0
	## AM NOT ADDING DEAD HERE AS LOTS OF INCEDENTS CAN HAVE DEAD ???? also 1013 has machinegunned ?? should we have gunned ? terrorist gunned ?
	## DEath of jesuit priest is a common occurence !!
	m = re.findall("(dynamite|bomb|bombing)\sattack",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count = 0
	else :
		m = re.findall("(?<=\s)attack",text,re.IGNORECASE|re.MULTILINE)
		if(m):
			count = len(m)
	m = re.findall("(?<=\s)murder",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count += len(m)
	#m = re.findall("(?<=\s)kill",text,re.IGNORECASE|re.MULTILINE) ## ambiguous ?? could conflict with bomb attack 
#	if(m):
#		count += len(m)
	m = re.findall("(?<=\s)shot",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)assassinat",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count += 2*len(m)
	m = re.findall("(?<=\s)massacre",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count += len(m)
	if(DEBUG):
		print (" ATTACK ************************************ count ",count)
	return count 

# search for bomb , l8r look for blew up 
def get_bomb_count(text):
	count = 0 
	m = re.findall("(?<=\s)bomb",text,re.IGNORECASE|re.MULTILINE) # can be done by the military 
	if(m):
		count = 2*len(m)
	m = re.findall("(?<=\s)bombed rebel",text,re.IGNORECASE|re.MULTILINE) # discount bomb if followed  by rebel
	if(m):
		count = 0
	m = re.findall("(?<=\s)explod",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count += 2*len(m)
	m = re.findall("(?<=\s)explosi",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)dynamite",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)blowing\-up",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count += (2)*len(m)
	m = re.findall("(?<=\s)blew\-up",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count += (2)*len(m)
	if(DEBUG):
		print (" BOMB ************************************ count ",count)
	return count

def get_kidnap_count(text):
	count = 0 
	m = re.findall("(?<=\s)kidnap",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count = 3*len(m)
	m = re.findall("(?<=\s)abduct",text,re.IGNORECASE|re.MULTILINE)
	if(m):
		count += 3*len(m)
	if(DEBUG):
		print (" kidnap ************************************ count ",count)
	return count 

def get_robbery_count(text):
	count = 0 
	m = re.findall("(?<=\s)stole(?=\s)",text,re.IGNORECASE|re.MULTILINE) # look ahead and look behind 
	if(m):
		count = len(m) 
	m = re.findall("(?<=\s)steal",text,re.IGNORECASE|re.MULTILINE) # look behind   
	if(m):
		count += len(m)
	m = re.findall("(?<=\s)robbery(?=\s)",text,re.IGNORECASE|re.MULTILINE) # look ahead and look behind
	if(m):
		count += 4*len(m) 
	m = re.findall("(?<=\s)robbed(?=\s)",text,re.IGNORECASE|re.MULTILINE) # look ahead and look behind 
	if(m):
		count += 4*len(m)
	m = re.findall("(?<=\s)loot",text,re.IGNORECASE|re.MULTILINE) # look ahead and look behind 
	if(m):
		count += 4*len(m)
	if(DEBUG):			
		print (" ROBBERY ************************************ count ",count)
	return count 
		
def get_predicted_event(text):

	# init dictionary 
	event_type = {} 
	# arson count 
	event_type['ARSON'] = get_arson_count(text) 
	# attack count  
	event_type['ATTACK'] = get_attack_count(text)
	# bomb count 
	event_type['BOMBING'] = get_bomb_count(text)
	# kidnap count 
	event_type['KIDNAPPING'] = get_kidnap_count(text)
	# robbery 
	event_type['ROBBERY'] = get_robbery_count(text)

	# TODO 
	# get max key with max value  .. CURRENTLY WE DONT HANDLE TIES 
	key,value = get_max_kv(event_type)
	# return max count event  
	if(key == 0):
		if(DEBUG):
			event = '-' # SHOULD WE SET ATTACK AS DEFAULT ..BECAUSE ELLEN SAID THAT EVERY DOC HAS ONE TERRORIST ATTACK..Also the docs with attack default are the most difficult ones for other slots too 
		event = 'ATTACK'	
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
		print ("event type for the file ",file," is = ",event_type) 


if __name__ == "__main__" :

	main()
	
