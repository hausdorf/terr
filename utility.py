import re

DEBUG = False
#SENT_SPL1 = '\.(?=")'  # matches '."'
#SENT_SPL2 = '\.(?=\s+)'# matches '. ' 
SENT_SPL = '\.((?=")|(?=\s+))' # matches '." ' '. '
EMPTY_LINE  = "\s*\n\s*$" # checks if a line is empty
COLL_SPACES = "\s+"
SPACES_REPL = " "


# TODO add code to take care of this also change the remove list or add this befor remove list if they both contain the same information
# TODO ADD NER LIST target cannot be a person , victim cannot be an organzation ,
# TODO remove numbers from np ? in perp i only i
# TODO first word for targe
# victims white flags
one_list = ['ONE','EVEN',"URBAN","SECTOR","DAS","PAZ","FEW","CHILEAN","SALVADOR","SEVERAL","VICE","CONFIRMATION","BROADCAST","WATER","U.","S","COLUMN","WEST","WESTERN","EAST","EASTERN","PRIVATE","PUBLIC","NATIONAL","UNIT",'ARMED',"OPERATION","INDUSTRIAL","BERLIN","PANAMA","TOWN","CEIBA","PARTS","PART","SECRET","TOWNS",'DEFENSE','CONFERENCE','PERUVIAN','PERU','HEAD','LEGISLATOR','SOVIET','FOREIGN','FEDERATION','MAGISTRATES','CONNECTION',"INDIVIDUAL","GO",'LISLIQUE','NATIONALIST','CARIBBEAN','JALPATAGUA','QUITO','FREEDOM',"AREAS","LIBERATION",'TWO','THREE','PRESIDENTS','PRESIDENT','MILITARY','FOUR','FIVE','SIX','SEVEN','CORDOBA','EIGHT','NINE',"ON",'TEN',"PENAL","LIMA","CALLAO","THEIR","EARLY","ITALY","FRANCE","SPAIN","ORLANDO","SQUAD",'OFFICIAL','INTELLIGENCE',"BIG",'VENEZUELA',"COLOMBIA","SQUADS","SPOKESMAN","OFF","COLOMBIA","UNION","SANTIAGO","AMERICAN","LEMPA","WAR","POST","INTELLIGENCE","POLICE","MEMBERS",'EDITOR',"ECUADORAN","THOUSAND","THOUSANDS","INVESTIGATIONS","INVESTIGATION","DETAINED","CARIBBEAN","OFFICIAL","DEPUTY","DEVICES","HONDURAN",'EVEN','NEIGHBORHOOD','GROUP','GROUPS','NICARGUA','TEAM','LOCAL','RIVER','BRANCH','BRANCHES','THURSDAY','ZACAMIL',"1ST","LOCAL","SQUAD",'SMALL','ER',"CITY","COMPANY","OIL","COMPANIES","INDUSTRY",'THREE','BASEMENT','WINDOWS','WINDOW',"BACK",'BASEMENT','LIFE',"FRONT",'SALVADORAN','OUR','LONGEST','EUROPEANS',"EUROPEAN",'COLOMBIA','SALVADORANS','SUSPECT','MAZA',"MUNICIPALITY",'MEMBER','DOZEN','DOZENS','EUROPEANS','POLICE','OTHER','A','RECTOR','JUDGES','US','COLOMBIANS','CHIEF','CHIEFS'] # ALSO ANY NUMBER BY ITSELF use isdigit function for string objects add all numbers + isdigit test


# flag words for victims 
flag_victims = ["GUERRILLAS","HEADQUARTERS","HEADQUARTER","ROAD","RIVER","PROVINCE","BASE","TOWN","VILLAGE","NEWSPAPER","UNITED STATES","VALLE DEL CAUCA","INSTITUTE","INSTITUTES","CALI CARTEL","NEIGHBORHOOD"]
# flag word for perp and targets 
flag_perp   = ["POLICE","ARMY","GOVERNMENT","JESUITS","JESUIT","PRIEST","PRIESTS","DEPARTMENT","NATIONAL FRONT","VILLAGE","BASE","POLICEMEN","POLICEMAN","TOWN","PROVINCE","JOURNALIST","RIVER","JOURNALISTS","BATTALION","CHIEFS","UNION","VEHICLE","MUNICIPALITY","PEASANTS","INDUSTRIAL","GROUP",'LEGISLATOR',"SALVADORAN",'PRESIDENT',"REPORTER","COLONEL","LAWYER","AMBASSADOR","MAJOR","SENATOR","COMMANDER","PORT"]
flag_target = ["JESUITS","TOWNS","CLERGYMEN","PROVINCE","JESUIT","PERSON","ATTORNEY","DEPARTMENT","HUANTA","EL MOSOTO SUNPUL","BATTALION","SOLDIERS","SOLDIER","CITY","NEIGHBORHOOD","PERSONS","ELN","RIVER","PRIESTS","JUDGES","JUDGE","PRESIDENTS","PRIEST","PEOPLE","PRESIDENT","MAJOR","REPORTER","COLONEL","'EL MOSOTO SUNPUL","OCOTAPAYO","CIVILIAN","CIVILIANS"]


# just remove the first word # DONT ADD JUDGE HERE I REMOVE ALL OF THESE IF THEY ARE ALONE
first_word_victim = ['SALVADORAN','REPORTER','LOCAL','COLONEL','LAWYER','DIRECTOR',"ATTORNEY","SENATOR","MAJOR","OTHER"]

# if these flag words are present as first words ignore the whole np
first_word_flag_victim= ['SUSPECT','SUSPECTS','SUSPECTED']
first_word_flag_target = ["LAWYER","DIRECTOR","ATTORNEY","SENATOR","COUNCILMAN","PRESIDENT","ROAD","BUSINESSMAN",'DOCTOR','WESTERN'] 
first_word_flag_perp = ["LAWYER","DIRECTOR","ATTORNEY","SENATOR","COUNCILMAN","PRESIDENT","ROAD","BUSINESSMAN","NEWSMAN",'DOCTOR',"LIBERAL"] 
# Remove everything befor president
# for organization the jesuit community cant be a perp . perp cant be jesuit  
# RED FLAG VICTIMS/organization perpatrators = [organization,military,infantry,]
# PERPETRATORS ARE UNIDENTIFIED PERSON / MEN or contains this
# BY is a NP not sure abt general
remove_list = ["GMT","APPROXIMATELY","OPERATING","''","RIVER","TOROLA","CONFIRMATION","PERPETRATED",'COORDINATOR',"INCIDENT","CAUSED","AGREEMENT","CHANNEL","INTO","CONSIDERATION","0300","RAIDED","DETERMINED","REASON","REASONS","RAID","AGREEMENTS","ESCALATION","ESPECIALLY","MEANS","FIGHTING","RAGED","SUPPORT","INCIDENTS","NORTHWESTERN","FRUSTRATED","NORTHEAST","CHARGES",'OPERATION','ENEMY',"BE","INFLUENTIAL","TELEPHONE","CALLS","CALL","OLIGARCHY","DECLARE","ROCKET",'REPRESENTATION',"AFFAIRS","IRRESPONSIBLE","PLANTED","CONCERNING","CHARGES","COMMISSION","DEFEAT","DEFEATED","ASSASSINATION","ALLEGED","LAUNCHER","RULING","ALLIANCE","REPUBLICAN","LAW","OUTLAW","GUNNED","SELF-STYLED","GO","DOWN","MEASURE","MEASURES",'PESETAS','RANSOM','RESIGNATIONS',"TENDERED",'STATEMENT','EARLY',"SATURDAY","PERSECUTED","SUNDAY","JANUARY","CALI","MONDAY","PROCESS","ACKNOWLEDGED","OFFICIALLY","SERVER","CARTEL","THURSDAY","COMMISSIONED","PATRIOT","US","RELEASED","RELEASE","FOUND","BECAUSE","ILLEGAL","ACTIVITY","ACTIVITIES","EXTRADITING","BUSINESS","LEFT","POSTS","DEVELOPMENT",'SECURITY',"WITHOUT","FULFILLING","SUSPEND","PROCEED","PROCEEDING","PROCEEDINGS","FUNERAL","TASK","COMMISIONED","ANY","INCLUDED","SET","INVESTIGATIONS","INVESTIGATION","PASSED","MATTER","MATTERS","SET","REMOTE","NOVEMBER","MACHINEGUN","BACKPACKS","DAWN","ADMITTED","MATERIEL","POINTED","RECREATIONAL","SLIGHTLY","SLIGHT","STATED","LEG","VISIT","WOUND","CAPITAL","QUICKLY","TREATED","ALLEGATION","WAR","UNOFFICIAL","FRUSTATED","PLAN","LINKED","MADE","INTERIOR","WEDNESDAY","ASSASINATION","SERVICES","AID","OCTOBER","TUESDAY","SHORTLY","SCENE","ISOLATED","NOTE","THROUGH","SENTENCES","LABEL","NEWS","CONDEMN","ACT","LABELED","COVERING","YES","SAY","THEN","SUFFICIENT","DETERMINE","WHETHER","ONLY","RECORD","EXPLOSION","IS","LEGAL","RESCUED","VIDEO","FOOTAGE","RESCUED","MEDIUM_SIZED","DICTATORSHIP","COWARDLY","RECORDS","APPROXIMATE","BOGOTA","WEAPON","WEAPONS","OVER","OUR","FORCES","FORCE","CATAPULTS","CATAPULT","DEVICES","DESCRIBED","EXPLOSIVE","EXPLOSIVES","PROJECTILES","ASSASINATION","PROJECTILE","KM","FINANCIAL","38-YEAR","UNDER","OLD","FREQUENT","ALL","CONTROL","DISTRICT","PERCENT","HAS","HAD","ACCEPTED","DOORS","DOOR",'STRAFFED',"WHOM","JUST","HONORARY","BEGAN","SHOUTING","SLOGANS","SLOGAN","FACT","LATELY",",","CARRIES","MONTH","MONTHS","SECTIONS",'TRADITIONAL',"SECTION","BEGUN","$","BILLION","BILLIONS","INCREASE","MULALO","YUMBO","WOUNDED","FOLLOWING","WHICH","JUNE","REPRESSION","ADMINISTRATIVE","INFANTRY","MINUTES","DEATH","NOON","DEACTIVATED","DEFEAT","AGAINST","UNLEASHED","HALTED","TEMPORARILY","GENOCIDE","SHOCK","BANKING","WALL","TOP","ANTIDRUG","CAUSING","BUT","MORTAR","TONIGHT","FIRE","MASS","SO","DECADES",'MONSIGNOR',"A","REPORTERS","MOUTH","ROUNDUPS","BEING","``","FIND","DETACHMENT","3D","MAGNATE","TELEVISION","WHICH","APPARENTLY","HOPEFUL","INCIDENT","KIDNAPPED","CAN","35-YEAR-OLD","ANTI-TERRORIST","NOT","LED","NICARAGUA","MISSING","MANY","DUE","INDISCRIMINATE","VENEZUELAN","ARE","SINCE","BLAME","BLAMED","BURIED","DECREES","DECREE","ISSUED","55-YEAR-OLD","PUNISHED","THOSE","RUMORS","MORE","GUARDING","SOURCES","POSITION","VACANT","SOURCE","ACCORDING","GIVEN","NATIONALIZATION","RESPITE","FEARS","AUGUST","DECADE","DECADED","BELIEVED","AWAKENING","VIOLENCE","PREVALENT","SEIZED","RIFLE","BEGINNING","REGIMES","TARGET","MR","UNDETERMINED","LARGE","PROPERTY","LOSSES","NEW","ACTIVITY","INSISTENT","IDENTIFIED","BOMBINGS","INCREASING","MURDERS","WAVE","KIDNAPPINGS","DRUG","TRAFFICKING","VERY","HOWEVER","ADMITS","ADMIT","FOUGHT","YOUNG","MECHANICS","SIMILAR","PRELIMINARY","LATER","MUCH","INVOLVED","LATE","MAY","DYNAMITE","ATTACK","AN","CARRIED","OUT","CONSIDERING","ENOUGH","EVIDENCE","PROVE","MISTREATED","FIRST","BRIBED","STILL","MASSACRES","AMAZED","JUSTICE","MAGISTRATE","CANDIDATE","PAST","YEARS","PREVIOUS","ATTACKS","SERIOUSLY","NONE","CLAIMED","ME","TOOK","ACTION","ESCAPED","CLOSE","ATTENTION","REPORT","INCLUDE","MARCH","TAKEN","WAS","WARNING","INDICATE","NEAR","VICTIMS","POLITICAL","FRIDAY","WAY","POLITICAL","MAIN","AUTHORITIES","AT","SAN","WELL","WORLD","GOVERNMENTS","RELEASE","TOTAL","CLARIFIACATION","PARTICULARLY","PARTICULAR","VICENTE","LOCATED","CLASHES","STRONG","VOLCANO","CHICHONTEPEC","0945","SOME","COULD","PARTICIPATED","IMMEDIATE","IDENTIKITS","AIRPORT","BOARD","FLIGHT","BETWEEN","HEADING","REPORTED","0630","0700","WOULD","ENTRANCE","COUNTRY","GUATEMALA","REPORTS","COMPANION","ASSISTANT","SECRETARY","MINISTER","MINISTRY","CASE","COLD","BLOOD","ANOTHER","WE","TOTALLY","BEEN","BRUTALLY","VIOLENTLY","SHOTS","DAMAGED","DAMAGE","DURING","NO","OR","FROM","RESULTED","RESULT","CASUALTIES","SUBSTANTIALLY","BOMB","THE","THESE","OPERATIONS","KILLING","BEFORE","AFTER","DAY","SHOCKED","NATION","BOTH","MEMBER","PARTY","SOCIAL","DEMOCRATIC","CRIME","IT","HE","SHE","HIS","HER","HIM","THEY","THEM","TODAY","YESTERDAY","THIS","THAT","THERE","WERE","ALSO","VICTIM","WHILE","FORMER","SAME","NIGHT","BY","AS","QUALIFICATIONS","WHO","KILLED","ALSO","HAVE","HAD","RECEIVED","RECEIVE","LEARNED","WE","SAME","PLACE","IN","MORNING","MURDERED","MASSACRED","'S","MASSACRE","MURDER","OUTSTANDING","GENERAL","LAST","TO","CONTINUE","HONEST"]

victim_remove_list = ["SUNPUL","ONE","PERQUIN","MOSOTO","PATRIOTIC","AIR","WHERE","UNIVERSITY","PANAMA","NATIONAL","BROADCAST","OCOTAPAYO",'ASONAL',"PRISONER","PRISONERS","HEAVILY","MINE","MINES","FREEDOM","VEHICLE","TECUN","UMAN","HOUSES","HOUSE","FMLN","FOURTH","PORT","RIVER","SOCIALIST","MIR","8","PEACE",'DEPUTY',"INTERNATIONAL","MUNICIPAL",'35','52','55',"12TH","CLINIC","HOTEL","EMBASSY","TEMPLE","100,000","70,000","PENAL","COURT","REVOLUTIONARY","MOVEMENT","12","LATIN","AMERICA","CAMP","DIRECTOR","WEEKEND","ARCE",'BATTALION','PAZ',"CRIMINAL","COURT","ETC","DOWNTOWN","COMPANY","KIDNAPPERS","KIDNAPPER","INFANTRY","CONCHAGUA","BATTALION","TOWN","MRTA","UCA","HUANTA","PALMEROLA","LEGISLATOR","UP","PRESIDENT","STREET","DOWNTOWN","STREETS","SEVERAL","STREET","1210","PLANE","HOME","ARMY","ALL","GANGS","NEWSMEN","POLITICIANS","BASE","PALMORA","BROTHER","LOCAL",",","0030","CHRISTIAN","BUSINESSMAN","SPANISH","ELECTRIC","POWER","SUBSTATION","EUROPEAN","UNDER","9","HEAD","SUSPECTS","2","DEPARTMENT","FIRE","MAN","NATIONAL","GUERRILLAS","LIBERAL","MILITARY","BANKER","COLUMBIANS","GOVERNMENT","CANDIDATE","MAFIA","COLOMBIAN","3","FIVE","FOUR","TWO","THREE","FIVE","SIX","SEVEN","EIGHT","NINE","TEN","MINISTRY","MEDIA","ITS","JUSTICE","ARMED","FORCES","DR","RESIDENCE","65","UNIVERSITY","RELIGIOUS","17","ORGANIZATION","TERRORIST","CAMERAMAN","POLICEMAN","ATTORNEY","CHILEAN","U.","S","HOSPITAL","18","BOMBS","ROSALES","37","OIL","PIPELINE","PACIFIC","ELN","10","MARKET","TASS","MISSION","PERSON","VALUABLE","FOUND","BODY","BODIES","EL","SAN","SALVADOR","BORDER","GUATEMALAN","MSGR","11","DAYS","AGO","10","LABOR","MEDELLIN","BE","LEADERS","LEADER","LEFTIST","MNR","LA","AURORA","GROUP","GROUPS","OF","ON","AN","AREA","BOGOTA","1","CAR","RURAL","PRESIDENTIAL","NEARBY","CENTRAL","PRESIDENCY"]

target_remove_list = ["DEMONSTRATORS","DEMONSTRATOR",'SPOKESMAN',"DEFENSE","PARKED","FECMAFAM","MILLION","PEACE","LEMPA","INTERNATIONAL","LISLIQUE","MINERS","NEWSMEN","MINER","1830","POLITICIANS","PEASANT","PATROLS","NEWSMEN","COLOMBIAN","ENTERPRISE","BOMBS","CAMERAMAN","PEOPLE",'CONSUL',"PALO","QUEMAO","ETC","20","NEIGHBORING","JESUITS","UNITED","STATES","FMLN","SALVADORANS","POLICE","CLERGYMEN","JESUIT","MEMBERS","UNION","OTHERS","COPREFA","REBEL","COMMAND","POSITIONS","COLCANO","GROUP","OF","OFFICIAL","SEVERAL","ON","STUDENT","U.","S"]

perp_indiv_remove_list = ["PRESIDENCY","''","PANAMA","FARABUNDO","UNIVERSITY","NATIONAL","POLICE","LA","AIR","FARC","SAN","BOMBS","LEAST","ON","BROADCAST","ONE","MAOIST","SHINING","SOVIET","PATH","'","MILLION","XXII",'MNR',"THOUSAND","MRTA","TWO","MINES","MINE","PRIVATE","FMLN","EASTERN","DEPARTMENT","DEPARTMENTS","100,000","PERQUIN","CUNDINAMARCA","FSLN","AMBASSADOR","PEASANT","PEASANTS","EXECUTIVE","LEADER","LEADERS","GOVERNMENT","EMPLOYEES","CITIZEN","LIBERATION","CITIZENS","PEOPLE","LA","AURORA","PART","TRUCK","COURT","AREA","RURAL","DEVICES","EMBASSY","NEWSMEN","EMPLOYEES","EXPLOSIVE","U.","S","EXPLOSIVES","CRISTIANI","PEDESTRIAN","PLANE","PEDESTRIANS","BOGOTA","DOWNTOWN","STREET","MARKET","DEPARTMENT","BODIES","EL","SALVADOR","BORDER","PRESIDENTIAL","NEARBY","CENTRAL"]
# REGEXES 
SEARCH_NP = "\[(.*?)\]\/NP" 
# NP cleaner 
# given a [(NP (DT a) (NN bomb) (NN plot))] output "bomb plot"
# there will be two versions of this one this one and the other is for when we want to put the answer into the templatei


def rmv_flagged_np(np_l,meta):

	new_list = []
	if (meta =='victim'):
		l  = flag_victims
	elif(meta == 'target'):
		l = flag_target
	elif(meta == 'perp'):
		l = flag_perp
	else:
		print "incorrect meta value for method rmv flagged np meta ==",meta
		return 
	for np in np_l:

		np = np.strip()
		flag = 0
		for flag_wrd in l :
		 	flag_wrd = '\\b'+flag_wrd+'\\b'
			m = re.search(flag_wrd,np)
			if m:
				# this np is flagged 
				flag = 1
		if(flag == 0):
			new_list.append(np)

	return new_list	

# this is only for victims 
def first_word_rmv(np_l):
	new_list = []
	for np in np_l:
		np = np.strip()
		# split the np into all its words 
		np_arr = np.split()
		np_arr_len = len(np_arr)
		if np_arr_len == 0 :
			continue
		np_first_word = np_arr[0]
		# go over first_word_flag_target
		flag = 0 
		for wrd in first_word_victim:
			if(np_first_word == wrd):
					flag = 1
					if np_arr_len == 1:
							#temp = ' '.join(np_arr)
							#new_list.append(temp)
							# will break from innermost loop	
							break
					else:
						# copy everything except the first word 
						temp = np_arr[1:]
						str_temp = ' '.join(temp)
						new_list.append(str_temp)
		if(flag == 0):
			# add to new_list
			temp = ' '.join(np_arr)
			new_list.append(temp)

	return new_list
# removes np if its first word is in list
def first_word_flag(np_l,meta):

	new_list = []
	for np in np_l:
		np = np.strip()
		# split the np into all its words 
		np_arr = np.split()
		np_arr_len = len(np_arr)
		if np_arr_len == 0 :
			continue
		np_first_word = np_arr[0]
		flag = 0
		if (meta == 'victim'):
			for wrd in first_word_flag_victim:
				if(np_first_word == wrd):
						flag = 1
			if(flag == 0):
				temp = ' '.join(np_arr)
				new_list.append(temp)


		elif(meta =='target'):
			# go over first_word_flag_target 
			for wrd in first_word_flag_target:
				if(np_first_word == wrd):
						flag = 1
			if(flag == 0):
				temp = ' '.join(np_arr)
				new_list.append(temp)
							
		elif(meta =='perp'):
			# go over first_word_flag_perp 
			for wrd in first_word_flag_perp:
				if(np_first_word == wrd):
						flag = 1
			if(flag == 0):				
				temp = ' '.join(np_arr)
				new_list.append(temp)

	return new_list 	

def one_word_cleaner(np_l):
	new_list = []
	for np in np_l:
		np = np.strip()
		np_arr = np.split()
		if(len(np_arr) == 1):
			temp = np_arr[0]
			#check if its a digit 
			if( temp.isdigit()):
				continue
			elif(temp in one_list):
				continue
			else:
				new_list.append(temp)

		else:
			new_list.append(np)
	return new_list

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
syn_list = [('JESUITS','CLERGYMEN'),('WIFE','LADY')]	
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

## Victim hacks 

def victim_hacks(np_l):
	
	new_set = set([]) 
	for np in np_l:
		np = np.strip()
		if(np == "POLICE COLONEL"):
			np = "A "+ np
		elif(np == "JUDGE"):	
			np = "A "+ np
		elif(np =="CITIZEN"):	
			np = "A "+ np
		elif(np == "JESUIT FATHERS"):
			np = "JESUIT PRIESTS"
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
	test_list4 = ['ONE','EVEN','TWO','0030','67','1',"ONLY THIS"]
	test_list3 = ['LAWYER HECTOR OQUELI','LAWYER','DIRECTOR',"ATTORNEY HECTOR","DOCTORE","SUSPECT ABC DEF"]
	flag_v = ['The ALCON HEADQUARTERS ','THE ABC HEADQUARTER','SCJIANG PROVINCE',"LONG ROAD","ONLY THIS :)","0030"]
	flag_p = ['The POLICE HEADQUARTERS ','THE ARMY HEADQUARTER','GOVERNMENT',"ONLY GOVERNMENT","ONLY THIS :)","0030"]
	flag_t = ['The JESUIT HEADQUARTERS ','THE JESUITS HEADQUARTER','CLERGYMEN',"CATHOLIC PRIESTS","ONLY THIS :)","PEOPLE"]
	print "input v",flag_v
	out_v = rmv_flagged_np(flag_v,'victim')
	print out_v
	print "input p",flag_p
	out_p = rmv_flagged_np(flag_p,'perp')
	print out_p
	print "input t",flag_t
	out_t = rmv_flagged_np(flag_t,'target')
	print out_t
	out_test  = one_word_cleaner(test_list4)
	print "one word cleaner"
	print out_test
	tst = ["CITIZEN","JUDGE","POLICE COLONEL","POLICE","JESUIT FATHER","JESUIT FATHERS"]
	print tst 
	new_tst = victim_hacks(tst)
	print new_tst
	if(DEBUG):
		print "original list",test_list
#	l = remove_subsets(test_list3)
#	l1 = remove_syn(test_list1)
#	l2 = first_word_flag(test_list3,'target')
#	l3 = first_word_flag(test_list3,'perp')
#	l5 = first_word_flag(test_list3,'victim')
#l4 = first_word_rmv(test_list3)
#print l5
	if(DEBUG):
		print l1
