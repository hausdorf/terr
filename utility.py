import re

DEBUG = False
# victims white flags 
not_victims = ["GUERRILLAS,"]
not_perp   = ["POLICE","ARMY","GOVERNMENT"]
# Remove everything befor president
# for organization the jesuit community cant be a perp . perp cant be jesuit  
# RED FLAG VICTIMS/organization perpatrators = [organization,military,infantry,]
# PERPETRATORS ARE UNIDENTIFIED PERSON / MEN or contains this
# BY is a NP not sure abt general
remove_list = ["COMPANION","ASSISTANT","SECRETARY","DEFENSE","MINISTER","CASE","COLD","BLOOD","AND","ANOTHER","WE","TOTALLY","BEEN","BRUTALLY","VIOLENTLY","SHOTS","DAMAGED","DAMAGE","DURING","NO","OR","FROM","RESULTED","CASUALTIES","SUBSTANTIALLY","BOMB","THE","A","IT","HE","SHE","HIS","HER","HIM","THEY","THEM","TODAY","YESTERDAY","THIS","THAT","THERE","THEIR","WERE","ALSO","VICTIM","CAR","WHILE","FORMER","SAME","NIGHT","BY","AS","QUALIFICATIONS","WHO","KILLED","ALSO","HAVE","HAD","RECEIVED","RECEIVE","LEARNED","WE","SAME","PLACE","IN","MORNING","MURDERED","MASSACRED","MASSACRE","MURDER","OUTSTANDING","GENERAL","LAST","TO","CONTINUE","HONEST"]
victim_remove_list = ["ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE","TEN","MNR"]
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
### ANOTHER FUNCTION IS CHOOSE ONE OR REMOVE REDUNDANT SYNONYMSi.e JESUITS / CLERGYMENi




### TAKES CARE OF NP overlapping .. selects the smallest NP . i.e if we have Bill clinton  and clinton ..this will return clinton

def remove_subsets(np_l):

	# clean the list of any redundant words 
	np_list = []
	for np in np_l:
		np = np.upper()
		np = np_cleaner_str(np)
		if np:
			np_list.append(np)

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
		for j in range(i+1,n):
				if( np_list_bin[j] == 1):
					continue
				source_np = np_list[j] 
				m = re.search(pattern,source_np,re.IGNORECASE)
				if m:
					if (DEBUG):
						if(DEBUG):
							print "one is a subset of another ",pattern,source_np
					np_list_bin[j] = 1
		np_list_bin[i]	= 1		
		np_list_new.append(patt)
	return np_list_new

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
	test_list = ["aa","aaaaaaa asdfs","aa sg asgasg","ia asgs aa"]
	if(DEBUG):
		print "original list",test_list
	l = remove_subsets(test_list)
	if(DEBUG):
		print l
