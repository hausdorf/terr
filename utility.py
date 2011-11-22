import re

DEBUG = False
#SENT_SPL1 = '\.(?=")'  # matches '."'
#SENT_SPL2 = '\.(?=\s+)'# matches '. ' 
SENT_SPL = '\.((?=")|(?=\s+))' # matches '." ' '. '
EMPTY_LINE  = "\s*\n\s*$" # checks if a line is empty
COLL_SPACES = "\s+"
SPACES_REPL = " "


# TODO add code to take care of this also change the remove list or add this befor remove list if they both contain the same information
# TODO ADD NER LIST i
# TODO remove numbers from np ? in perp i only 
# victims white flags 
not_victims = ["GUERRILLAS"]
not_perp   = ["POLICE","ARMY","GOVERNMENT"]
not_target = ["JESUITS","CLERGYMEN","JESUIT"]
# Remove everything befor president
# for organization the jesuit community cant be a perp . perp cant be jesuit  
# RED FLAG VICTIMS/organization perpatrators = [organization,military,infantry,]
# PERPETRATORS ARE UNIDENTIFIED PERSON / MEN or contains this
# BY is a NP not sure abt general
remove_list = ["MAIN","AUTHORITIES","AT","SAN","WELL","WORLD","GOVERNMENTS","RELEASE","TOTAL","CLARIFIACATION","PARTICULARLY","VICENTE","LOCATED","CLASHES","STRONG","VOLCANO","CHICHONTEPEC","0945","SOME","COULD","PARTICIPATED","IMMEDIATE","IDENTIKITS","AIRPORT","BOARD","FLIGHT","BETWEEN","HEADING","REPORTED","0630","0700","WOULD","ENTRANCE","COUNTRY","CENTRAL","GUATEMALA","REPORTS","COMPANION","ASSISTANT","SECRETARY","DEFENSE","MINISTER","CASE","COLD","BLOOD","ANOTHER","WE","TOTALLY","BEEN","BRUTALLY","VIOLENTLY","SHOTS","DAMAGED","DAMAGE","DURING","NO","OR","FROM","RESULTED","CASUALTIES","SUBSTANTIALLY","BOMB","THE","THESE","OPERATIONS","KILLING","A","BEFORE","AFTER","DAY","SHOCKED","NATION","BOTH","MEMBER","PARTY","SOCIAL","DEMOCRATIC","CRIME","IT","HE","SHE","HIS","HER","HIM","THEY","THEM","TODAY","YESTERDAY","THIS","THAT","THERE","THEIR","WERE","ALSO","VICTIM","CAR","WHILE","FORMER","SAME","NIGHT","BY","AS","QUALIFICATIONS","WHO","KILLED","ALSO","HAVE","HAD","RECEIVED","RECEIVE","LEARNED","WE","SAME","PLACE","IN","MORNING","MURDERED","MASSACRED","MASSACRE","MURDER","OUTSTANDING","GENERAL","LAST","TO","CONTINUE","HONEST"]
victim_remove_list = ["ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE","TEN","MNR","LA","AURORA","GROUP","OF"]
target_remove_list = ["SAN","SALVADOR","JESUITS","CLERGYMEN","JESUIT","REBEL","POSITIONS","COLCANO","GROUP","OF"]
perp_indiv_remove_list = ["POLICE","GOVERNMENT","PEOPLE","LA","AURORA","PART"]
# REGEXES 
SEARCH_NP = "\[(.*?)\]\/NP" 
# NP cleaner 
# given a [(NP (DT a) (NN bomb) (NN plot))] output "bomb plot"
# there will be two versions of this one this one and the other is for when we want to put the answer into the template
def np_cleaner(np):
	
	clean_list = [] 
	spl = np.split()
	lspl = len(spl)

	if lspl < 2:
		return ''

	wrds = []

	i = 1
	curr = spl[0]
	while i < lspl:
		if curr[0][0] == '(' and spl[i][-1] == ')':
			s1 = curr.strip('(')
			s2 = spl[i].strip(')')
			s2.strip()
			# S1 is tag S2 is word 
			wrds.append(s2)

		curr = spl[i]
		i += 1
	new_wrds = []	
	for wrd in wrds:
		wrd = wrd.upper()
		# if there is a comma then everything after the comma can be thrown ## this is imp !!
		# if wrd is not a word just punctuation dont add it # this i am not sure abt 
		if wrd in remove_list: 
			continue
		else:
			new_wrds.append(wrd)

	clean_str = ' '.join(new_wrds)
	return clean_str

def np_cleaner_str(np):

	np = np.strip()
	np_words = np.split()
	if (len(np_words) == 1):
		return np
	new_words = []
	for word in np_words :
		word = word.upper()	
		if word in remove_list:
			continue 
		else:
			new_words.append(word)
	new_np = ' '.join(new_words)
	return new_np
# take a bunch of words from a line and a list of stop words and removes the stop words in the word list 
def word_cleaner(line_wrds_list,v_list):
	new_wrds = []	
	for wrd in line_wrds_list:

		wrd = wrd.strip()
		if wrd:
			wrd = wrd.upper()
			# if there is a comma then everything after the comma can be thrown ## this is imp !!
			# if wrd is not a word just punctuation dont add it # this i am not sure abt 
			if wrd in v_list: 
				continue
			else:
				new_wrds.append(wrd)

	clean_str = ' '.join(new_wrds)
	# check if empty line
	clean_str = clean_str.strip()
	if(clean_str):
		return clean_str
	else:	
		return ""

def common_cleaner(in_list):

	out_list = [] 
	for line in in_list:
		line = line.strip()
		wrd_list = line.split()
		clean_line = word_cleaner(wrd_list,remove_list)
		if clean_line:
			out_list.append(clean_line)
	return out_list	

def perpi_cleaner(in_list):
	out_list = [] 
	for line in in_list:
		line = line.strip()
		wrd_list = line.split()
		clean_line = word_cleaner(wrd_list,perp_indiv_remove_list)
		if clean_line:
			out_list.append(clean_line)
	return out_list

def target_cleaner(in_list):

	out_list = [] 
	for line in in_list:
		line = line.strip()
		wrd_list = line.split()
		clean_line = word_cleaner(wrd_list,target_remove_list)
		if clean_line:
			out_list.append(clean_line)
	return out_list	

def victim_cleaner(in_list):

	out_list = [] 
	for line in in_list:
		line = line.strip()
		wrd_list = line.split()
		clean_line = word_cleaner(wrd_list,victim_remove_list)
		if clean_line:
			out_list.append(clean_line)
	return out_list		
	

### ANOTHER FUNCTION IS CHOOSE ONE OR REMOVE REDUNDANT SYNONYMSi.e JESUITS / CLERGYMENi
syn_list = [('JESUITS','CLERGYMEN','JESUIT')]	
def remove_syn(np_l):
	
	np_str = ' # '.join(np_l)
	np_str = np_str.strip()
	# remove consecutive white space
	np_str = re.sub(COLL_SPACES,SPACES_REPL,np_str)
	for tup in syn_list:
		# choose the first one as the main one 
		main_wrd = tup[0]
		temp_str = np_str 
		for sub in xrange(1,len(tup)):
			# replace all occurence of others to main tuple 
			sub_wrd = '\\b'+tup[sub]+'\\b'
			temp_str = re.sub(sub_wrd,main_wrd,temp_str)
	# make the temp_str into list
	temp_list = temp_str.split('#')
	new_set = set([])
	for np in temp_list:
		np = np.strip()
		new_set.add(np)

	return list(new_set)
		
### TAKES CARE OF NP overlapping .. selects the smallest NP . i.e if we have Bill clinton  and clinton ..this will return clinton

def remove_subsets(np_list):

	# clean the list of any redundant words 
	#np_list = []
	#for np in np_l:
	#	np = np.upper()
		#np = np_cleaner_str(np)
	#	if np:
	#		np_list.append(np)

	if(DEBUG):
		print "np_list",np_list
	# sort list 
	np_list.sort(key=lambda(x):len(x))
	# create a binary list of same len as np list and set all elements to 0 , ( 0, not added to new list ,1 = added to new list ) 
	np_list_bin = [0 for i in xrange(len(np_list))]
	# Algorithm go from smallest to largest 
	n = len(np_list)
	np_list_new = [] 
	for i in range(n):
		if(np_list_bin[i] == 1 ):
			continue
		patt = np_list[i]
		patt = patt.strip()
		pattern = '\\b'+patt+'\\b' # add word boundary regex meta character  
		flag = 0 
		for j in range(i+1,n):
				if( np_list_bin[j] == 1):
					continue
				source_np = np_list[j] 
				m = re.search(pattern,source_np,re.IGNORECASE)
				if m:
					if(DEBUG):
						print "one is a subset of another ",pattern,source_np
					np_list_bin[j] = 1
					if(not flag): 
						np_list_new.append(source_np)
						np_list_bin[i]=1
						flag = 1
		if(not np_list_bin[i]):				
			np_list_new.append(patt)
		np_list_bin[i]	= 1		
	return np_list_new


# checks if a line is empty i.e \s*\n
def isEmpty(line):	
	m = re.match(EMPTY_LINE,line)
	if(m):
		return True
	return False
# splits sentences 
def sent_splitter(line):

	out_list = []
	line_list = re.split(SENT_SPL,line)	
	if len(line_list) > 1:
		for l in line_list:
			l = l.strip()	
			if isEmpty(l):
				continue
			elif l:
				# remove any " quotations in the list 
				l_new = re.sub('"','',l)
				out_list.append(l)
		return out_list	
		
	else:
		out_list.append(line)
		return out_list
		



def f_read(filename):

	fd = open(filename)
	text = fd.read()
	fd.close()
	return text

# converts a pos tagged sentence to a untagged plain sentence 	
def pos_to_plain(sent):	
	out_list = [] 
	words = sent.split()
	for wrd in words:
		wrd_list = wrd.split('/')
		new_wrd = wrd_list[0]
		if (new_wrd):
			out_list.append(new_wrd)
	return ' '.join(out_list)


if __name__ =="__main__":
	test_list = ["AA","AAAAAA ASDFS","AA SG ASGASG","IA ASGS AA"]
	test_list1 = ["JESUITS","CLERGYMEN","CLERGYMEN","JESUIT"]
	test_list2 = ['OQUELI', 'GILDA FLORES', 'HECTOR OQUELI']
	test_list3 = ['HECTOR OQUELI']
	if(DEBUG):
		print "original list",test_list
	l = remove_subsets(test_list3)
	l1 = remove_syn(test_list1)	
	print l
	if(DEBUG):
		print l1
