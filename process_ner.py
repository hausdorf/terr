import sys
import re
import utility

DEBUG=False
# PERSON REGEX 
PERSON_NP = "(\w+?/PERSON\s*(\w+?/PERSON\s*)*)"
#PERSON_NP = "(\w+?/PERSON\s*)+"

# ORGANIZATION REGEX 
ORGANIZATION_NP = "(\w+?/ORGANIZATION\s*(\w+?/ORGANIZATION\s*)*)"
#picks the PEOPLE AND ORGAI 


def process_ne(match_list):
	e_list = [] 	
	for tup in match_list:
		# processes all the tuples/matches one at a time 
		entity_str = tup[0]
		entity_list = entity_str.split()
		temp_list = []
		for part in entity_list:
			#split part by /
			part_list = part.split('/')
			temp_list.append(part_list[0])
		temp_str = ' '.join(temp_list)	
		e_list.append(temp_str)
	return e_list 

# returns a dict with key as the np and the value as PERSON/ORG 	
def get_entities(filename):

	sem_dict = {}
	fd = open(filename)
	text = fd.read()
	m_persons = re.findall(PERSON_NP,text)	
#print m_persons
	p_list = process_ne(m_persons)
	# MAKE UNIQUE
	p_list_set = set(p_list)
	if(DEBUG):
		print "set of all the persos =",p_list_set
	temp_list = utility.remove_subsets(p_list_set)
	for np in temp_list:
		sem_dict[np] = "PERSON"
	if(DEBUG):	
		print temp_list
	m_organizations = re.findall(ORGANIZATION_NP,text)
#	print m_organizations
	o_list = process_ne(m_organizations)
	o_list_set = set(o_list)
	temp_list = utility.remove_subsets(p_list_set)
	if(DEBUG):
		print temp_list 
	for np in temp_list:
		sem_dict[np] = "ORGANIZATION"
	#print o_list_set 
	return sem_dict 

if __name__=="__main__":
	get_entities("out_ner")
