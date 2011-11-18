

remove_list = ["THE","A","IT","HE","SHE","HIS","HER","HIM","THEY","THEM","TODAY","YESTERDAY","THIS","THAT","THERE","WERE","ALSO","VICTIM","CAR"]
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


### ANOTHER FUNCTION IS CHOOSE ONE OR REMOVE REDUNDANT i.e JESUITS / CLERGYMEN
### ALGO IS ONE STR IS A SUBSET OF THE OTHER THEN DONT INCLUDE BOTH	
