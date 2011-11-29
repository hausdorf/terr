import sys
import re
import utility

DEBUG=False
# PERSON REGEX 
PERSON_NP = "([^/]+?/PERSON\s*([^/]+?/PERSON\s*)*)"
#PERSON_NP = "(\w+?/PERSON\s*)+"

# ORGANIZATION REGEX 
ORGANIZATION_NP = "([^/]+?/ORGANIZATION\s*([^/]+?/ORGANIZATION\s*)*)"
#picks the PEOPLE AND ORGAI 


def java_ner_tagger(txt):

	fj = open("ner_text",'w')
	fj.write(txt)
	fj.close()
	os.system("java -mx400m edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers/all.3class.distsim.crf.ser.gz -textfile ner_text > nout ")
	fo = open("nout")
	txt = fo.read()
	fo.close()
	return txt



def process_ne(match_list):
	e_list = [] 	
	for tup in match_list:
		# processes all the tuples/matches one at a time 
		entity_str = tup[0]
		entity_list = entity_str.split()
		temp_list = []
		for part in entity_list:
			if(part =='O'):
				continue
			#split part by /
			part_list = part.split('/')
			temp_list.append(part_list[0])
		temp_str = ' '.join(temp_list)	
		e_list.append(temp_str)
	print "### ELIST "
	print e_list
	return e_list 

def get_ner_lists(sem_dict):
	
	person_list = []
	org_list = []
	loc_list = [] 
	for k,v in sem_dict.iteritems():

		if(v == "ORGANIZATION"):
			org_list.append(k)
		elif(v == "PERSON"):
			person_list.append(k)
		elif(v == "LOCATION"):
			loc_list.append(k)	
		else:
			print "unknown entity"
	return (org_list,person_list,loc_list)

# returns a dict with key as the np and the value as PERSON/ORG 	
def get_entities(text):

	sem_dict = {}
	m_persons = re.findall(PERSON_NP,text)
#print m_persons
	p_list = process_ne(m_persons)
	# MAKE UNIQUE
	p_list_set = set(p_list)
	print "plist "
	print p_list_set
	if(DEBUG):
		print "set of all the persos =",p_list_set
	temp_list = utility.remove_subsets(list(p_list_set))
	for np in temp_list:
		sem_dict[np] = "PERSON"
	if(DEBUG):	
		print temp_list
	m_organizations = re.findall(ORGANIZATION_NP,text)
	print m_organizations 
#	print m_organizations
	o_list = process_ne(m_organizations)
	o_list_set = set(o_list)
	print "o_list"
	print o_list_set
	temp_list = utility.remove_subsets(list(o_list_set))
	if(DEBUG):
		print temp_list 
	for np in temp_list:
		sem_dict[np] = "ORGANIZATION"
	#print o_list_set 
	return sem_dict 

if __name__=="__main__":
	fd = open(filename)
	text = fd.read()
	get_entities(text)
