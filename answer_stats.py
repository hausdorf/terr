from __future__ import division, with_statement
import os, sys, collections, re, string
from ctx_hist import CTX_HIST
from nltk import sent_tokenize, word_tokenize, pos_tag, RegexpParser, ne_chunk


TST = {'BOMB SET IN AN ICE CREAM CART': 1, 'POWERFUL BOMB': 2, 'BOMB': 29, 'ROCKET': 2, 'TNT': 1, 'MACHINEGUNS IN TRIPODS': 1, 'THE BOMB': 1, 'CARBOMB': 1, 'TRUCK': 1, 'DYNAMITE CHARGE': 3, 'TERRORIST BOMBS': 1, 'EXPLOSIVES': 5, 'CAR BOMB': 5, 'SEVERAL DYNAMITE ATTACKS': 1, 'A BOMB': 2, '9-MM WEAPONS': 1, '-': 318, 'HELICOPTER GUNSHIP': 1, 'INCENDIARY BOMB': 1, 'AK-47S': 1, 'VEHICLE LOADED WITH EXPLOSIVES': 1, 'HELICOPTER GUNSHIPS': 1, 'PACKAGES OF DYNAMITE': 1, 'SUBMACHINEGUN': 1, 'EXPLOSIVE DEVICE': 2, 'MACHINEGUN': 2, 'ROCKETS': 3, 'EIGHT BOMBS': 1, 'MINE': 1, 'EXPLOSIVE CHARGES': 1, 'BOMB BLAST': 1, 'GRENADES': 2, 'BOMBS': 12, 'DYNAMITE STICKS': 2, 'GRENADE': 2, 'HEAVY CALIBER WEAPONS': 1, 'BULLET': 1, '.22 CALIBER GUN': 1, 'MORTAR': 2, 'FOUR BOMBS': 1, 'MACHINE-GUN': 1, 'EXPLOSIVE DEVICES': 5, 'BULLETS': 1, 'CHARGE OF DYNAMITE': 1, 'AT LEAST SIX BOMBS': 1, 'DYNAMITE': 10, 'MACHINEGUNS': 2, 'DYNAMITE ATTACKS': 1}

TST_TARG = {'pintuco paint factory': 1, 'santa elena church': 1, 'stores': 1, 'office': 2, 'power pylons': 1, "headquarters of colombia's secret security police": 1, "el espectador's offices": 1, 'facilities': 2, 'lempa river hydroelectric executive commission ministation': 1, 'headquarters of the salvadoran workers national union federation': 1, 'state department hercules c-123 cargo plane': 1, "newspaper el siglo's facilities": 1, 'transformer': 1, 'hondutel office': 1, 'embassy facilities': 1, 'a camp of salvadoran refugees who had been in honduras': 1, 'main oil pipeline in colombia': 1, "colombia's federal investigations police": 1, 'grocery store': 1, 'royal hotel': 1, 'fenastras building': 1, 'hercules c-123 cargo plane': 1, 'strategic targets': 1, 'old shack': 1, 'c-123 hercules plane': 1, 'the banco cuscatlan': 1, 'building with coffee harvesters': 1, 'homes': 1, 'das': 4, 'precinct': 1, 'bank': 2, 'the university of chile': 1, 'posts of the electric system': 1, 'tank trucks': 1, 'police instruction center': 1, 'pole': 1, 'cargo train': 1, 'embassy': 1, 'offices': 1, 'colpatria bank branch': 1, 'cargo plane': 1, 'political party headquarters': 1, 'hondutel': 1, 'a settlement of repatriates': 1, 'offices of the national housing enterprise': 1, 'administrative department of security': 5, 'private homes': 1, 'chilean-u.s. cultural institute': 2, "president cristiani's residence": 1, 'cathedral': 1, "avianca's boeing 727": 1, 'bathroom of the chilean-u.s. cultural institute': 1, 'peruvian embassy': 2, 'settlement of repatriates': 1, 'radio station': 1, 'power lines': 1, 'camp': 1, 'zacamil neighborhood': 1, 'cultural institute': 1, 'liberal unity headquarters': 1, 'cetipol': 1, 'embassy building': 1, 'mining centers': 1, 'transportation': 1, 'the electric system': 1, 'electric system': 1, 'houses': 3, 'ecuadoran consulate': 1, 'fishing boat': 2, 'movie theater': 1, 'cano limon-covenas oil pipeline': 1, 'velox bank': 1, 'cano - limon - covena oil pipeline': 1, 'home of retired colonel carlos humberto figueroa': 1, '110,000-volt primary lines': 1, 'cel ministation': 1, 'plane': 2, 'central american jose simeon canas university': 1, "avianca's boeing 727 that exploded in midair in a sparsely populated region near bogota": 1, 'steel factory': 2, 'a pole': 1, 'camp of salvadoran refugees who had been in honduras': 1, 'a bank': 1, 'fenastras headquarters': 2, 'teca - vasconia oil pipeline': 1, 'uca': 1, 'salvadoran embassy': 1, 'fenastras': 8, 'honduran telecommunications enterprise': 2, 'union': 1, 'fensatras building': 1, 'telephone exchange of the bocagrande tourist and residential district': 1, 'unidentified office in the agriculture and livestock ministry building': 1, 'vehicle': 2, 'oil installations': 1, 'peasant home': 1, 'store': 1, 'its ambulances': 1, 'the electric service system': 1, 'el salvadoran embassy': 1, 'the diplomatic premises': 1, 'oil pipeline': 1, 'bus': 5, 'hotel': 1, 'attack on the homes of important government officials': 1, 'headquarters of the department of administrative security': 1, 'consulate': 1, 'sheraton hotel': 1, 'salvadoran workers national labor federation': 1, 'hilton hotel': 1, 'telephone booth': 1, 'salvadoran workers national union federation': 3, 'a camp of salvadoran refugees': 1, 'gasoline truck': 1, 'a pole that they use for electrical distribution': 1, 'shopping centers': 1, 'c-123 cargo plane': 1, 'the residence of salvadoran president alfredo cristiani': 1, 'offices of radio mineria': 1, 'electric poles': 1, 'camp of salvadoran refugees': 1, 'san jorge warehouse': 1, 'police precinct': 1, 'home of the deputy minister': 1, 'headquarters of a labor union': 1, '-': 281, 'bank branch': 1, 'congress building': 1, 'installations of the das': 2, 'labor union headquarters': 1, 'telephone exchange': 2, 'headquarters of the opposition salvadoran workers national union federation': 1, 'power grid': 1, 'banco cuscatlan': 1, 'u.s. state department hercules c-123 cargo plane': 1, 'telephone office': 2, 'unidentified office of the agriculture and livestock ministry': 1, 'the hilton hotel': 1, 'police patrol car': 3, 'das facilities': 1, 'power tower': 1, 'union offices': 1, 'building': 2, 'the gate of the university of chile': 1, 'a camp': 1, 'vehicles': 1, 'headquarters': 1, 'red cross ambulances': 1, 'the u.s. consulate': 1, 'the department of administrative security': 1, 'the das': 1}

TST_VICT = {'john marck jones': 1, 'two women': 1, 'luis sales': 1, 'trade union members': 1, 'guillermo rojas': 1, 'coronel largow': 1, 'ana isabel casanova': 1, 'julio rodriguez': 1, 'coffee harvesters': 1, 'jose ovidio gomez': 1, 'disfigured bodies of the victims': 1, 'children': 3, 'several mayors': 1, 'u.s. mormon missionaries': 1, 'dolores isabel casanova porras': 1, 'workers': 1, 'justiniano sagastume rodriguez': 1, 'hipolito hincapie': 1, 'brenda hoovarit': 1, 'jose maria martinez': 2, 'hector oqueli': 5, 'victims': 2, 'jose ernesto vasquez': 1, 'civilian': 1, 'gustavo alvarez martinez': 2, 'lopez grimaldo': 1, 'armando caycedo camargo': 1, 'ernesto': 1, 'ignacio ellacuria': 13, "disfigured bodies of the victims of avianca's boeing 727": 1, 'francisco guerrero': 1, 'spanish jesuits': 1, 'one of them': 1, 'alumni, of cetipol': 2, 'carlos pizarro leon-gomez': 1, 'two officials from the electoral registry': 1, 'carlos pizarro leongomez': 5, 'police instruction center': 2, 'colombian': 1, 'patricia echavarria': 1, 'jose gonzalo rodriguez gacha': 1, 'soviet seamen': 1, 'labor leaders': 2, 'federico estrada velez': 4, 'two people': 1, 'ricardo bohorquez': 1, 'people': 14, "jesuit priests'": 1, 'estrada velez': 1, 'dead': 1, 'embassy officials': 1, 'fabio roa': 1, 'marilin ramirez': 1, 'miguel maza marquez': 1, 'enrique lopez albujar': 2, 'other person': 1, 'febe elizabeth velasquez': 2, 'galan': 1, 'one of the u.s. citizens who was kidnapped in medellin today': 1, 'maria elena diaz': 2, 'member of carabineros': 1, 'pedro luis osorio': 1, 'uca priests': 1, 'company of policemen': 1, 'father ignacio ellacuria': 1, 'demonstrators': 1, 'hector oqueli colindres': 6, 'jaime roldos aguilera': 2, 'elmer machado': 1, 'salvadorans': 2, 'jaramillo ossa': 1, 'jesuits': 28, 'hector delgado parker': 2, 'luis carlos galan': 17, 'abelardo daza': 1, 'danilo barillas': 1, 'sorto milla': 1, 'bodyguards': 1, 'pizarro': 1, 'eulogio flores': 1, 'many civilians': 1, 'members': 1, 'civilians': 6, 'passengers': 2, 'oscar arnulfo romero': 2, 'antonio roldan betancur': 1, 'persons': 4, 'peasants': 1, 'jesuit priests': 35, 'francisco jose guerrero': 2, "baena soares' personal bodyguards": 1, 'congressman': 1, 'residents': 1, 'luis carlos galan sarmiento': 4, 'disfigured bodies': 1, 'alvaro diego montoya escobar': 1, 'ernesto samper': 1, 'carlos humberto figueroa': 1, 'jesuits and two employees of the central american university': 1, 'members, rather the alumni, of cetipol': 2, 'diego morales': 1, 'carlos marcelo': 1, 'bernardo jaramillo ossa': 6, 'a police detachment': 1, 'valdemar franklin quintero': 2, 'manuel vallejo uribe': 1, 'one of the u.s. citizens': 1, 'gonzalo rodriguez gacha': 2, 'two civilians': 1, 'david blundy': 1, "disfigured bodies of the victims of avianca's boeing 727 that exploded in midair in a sparsely populated region near bogota": 1, 'tourists': 1, 'wife of a university leader': 1, 'jaramillo': 1, 'bernardo jaramillo': 2, 'jose antonio rodriguez porth': 2, 'journalists': 1, 'members of the mpsc': 2, 'otto sorto milla': 2, 'clergymen': 1, 'passersby': 1, 'carlos pizarro': 6, 'jorge adolfo vargas': 1, 'david leslie kent': 1, 'women': 2, 'elizabeth velazquez': 2, 'alvaro diego montoya': 1, 'policemen': 3, 'mayors': 1, 'norberto rodriguez rodriguez': 1, 'vargas gonzalez': 1, 'edgardo lopez grimaldo': 2, 'fishermen': 1, 'gustavo guerra': 1, 'union leaders': 2, 'peruvian diplomats': 1, 'guillermo payes': 1, 'the governor of antioquia': 1, 'priests': 7, 'billy murphy': 1, 'francisco antonio amico ferrari': 1, 'rodriguez': 1, 'augusto carneiro moreira junior': 1, 'businessman naim isaias': 1, 'armansio quispe': 1, 'rodriguez rodriguez': 1, 'orlando letelier': 1, 'dr ignacio ellacuria': 1, 'mauricio gutierrez castro': 1, 'a presidential candidate': 1, 'edgar chacon': 1, 'drivers': 1, 'ellacuria': 2, '-': 79, 'antonio rodriguez porth': 4, 'marco tulio montenegro': 1, 'nedina elkaches': 1, 'injured': 1, 'ruben zamora': 1, 'students': 2, 'baena soares': 1, 'mormon missionaries': 1, 'seamen': 1, '15-year-old daughter': 1, 'six jesuit priests': 2, 'luis carlos carlos galan': 1, 'juan carlos mir': 1, 'officials from the electoral registry': 1, 'barroso': 1, 'national guard units': 1, 'alfredo cristiani': 2, 'jamus arthur donelly': 1, 'person': 2, 'university students': 1, 'mary stanislaus makeil': 1, 'intellectuals': 1, 'pablo li ormeno': 1, 'civilian population': 1, "social christian people's movement": 1, 'carlos valencia garcia': 5, 'gustavo leigh guzman': 1, 'members of the local red cross': 1}

ANSWR1 = 'developset/answers/'
ANSWR2 = 'answerkeys/'
ALLWD = set(['INCIDENT', 'WEAPON', 'PERP INDIV', 'PERP ORG', 'TARGET', 'VICTIM'])
V_TAGS = set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])


def fiter(p):
	for pth, dirs, files in os.walk(p):
		for file in files:
			r = open(pth + '/' + file)
			yield r
			r.close()

def liter(p):
	for f in fiter(p):
		for l in f.readlines():
			yield l

### USED FOR TESTING, NOT TRAINING
def liter_(i):
	if i == 1 or i == 3:
		for f in fiter(ANSWR1):
			for l in f.readlines():
				yield l

	if i == 2 or i == 3:
		for f in fiter(ANSWR2):
			for l in f.readlines():
				yield l
### USED FOR TESTING, NOT TRAINING;

def liter_all_f():
	for f in fiter(ANSWR1):
		for l in f.readlines():
			yield l

def answr_dict_(i):
	stats = collections.defaultdict(
			lambda: collections.defaultdict(lambda: 0))

	for l in liter_(i):
		spl = l.strip().split(':')
		if len(spl) < 2 or spl[0] not in ALLWD:
			continue

		#stats[spl[0]][spl[1].strip()] += 1
		for s in spl[1].split('/'):
			s = s.strip()
			stats[spl[0]][s] += 1

	return stats

def answr_dict():
	stats = collections.defaultdict(
			lambda: collections.defaultdict(lambda: 0))

	for l in liter_all_f():
		spl = l.strip().split(':')
		if len(spl) < 2 or spl[0] not in ALLWD:
			continue

		#stats[spl[0]][spl[1].strip()] += 1
		for s in spl[1].split('/'):
			s = s.strip()
			stats[spl[0]][s] += 1

	return stats

def prior_patts(thing, stats):
	patts = []
	for entry in stats[thing]:
		if entry == '-':
			continue

		patts.append(entry)

	return patts

def score_w_hist(sent, d):
	lst = []
	for w in sent:
		if w[1] in V_TAGS:
			lst.append(w[0])
	return len(lst)

def score_w_targlist(sent):
	if sent in TST_TARG:
		return sent
	return None

def score_w_victlist(sent):
	if sent in TST_VICT:
		return sent
	return None

def results(thing, patts, stats, text):
	rslts = []
	rslt = collections.defaultdict(lambda:0)

	for e in patts:
		res = re.search(' ([a-zA-Z]+-)?' + e + '(S)? ', text)
		if res:
			sents = [s for s in sent_tokenize(text)]
			for s in sents:
				if not re.search(' ([a-zA-Z]+-)?' + e + '(S)? ', s):
					continue
				pos = pos_tag(word_tokenize(s.lower()))
				scr = score_w_hist(pos, CTX_HIST)

				"""
				if thing == 'TARGET':
					o = score_w_targlist(res.group(0).strip().lower())
					if o:
						rslts.append((res.group(0).strip(),TST_TARG[e.lower()]))
						rslt[res.group(0).strip()] += scr
						continue

				if thing == 'VICTIM':
					o = score_w_victlist(res.group(0).strip().lower())
					print o
					if o:
						rslts.append((res.group(0).strip(),TST_VICT[e.lower()]))
						rslt[res.group(0).strip()] += scr
						continue
				"""

				if scr > 0:
					rslts.append((res.group(0).strip(), stats[thing][e]))
					rslt[res.group(0).strip()] += scr

	rslts = filter(lambda(x,y): y > 1, rslts)
	rslts.sort(key=lambda(x,y):y, reverse=True)

	rslt = filter(lambda(x,y): y > 1, [(k,v) for k,v in rslt.items()])
	rslt.sort(key=lambda(x,y):y, reverse=True)

	if len(rslts) > 0:
		#return rslt
		return rslts
	else:
		return '-'

def get_weapon(text, stats):
	patts = prior_patts('WEAPON', stats)
	return results('WEAPON', patts, stats, text)

def get_perp_indiv(text, stats):
	patts = prior_patts('PERP INDIV', stats)
	return results('PERP INDIV', patts, stats, text)

def get_perp_org(text, stats):
	patts = prior_patts('PERP ORG', stats)
	return results('PERP ORG', patts, stats, text)

def get_target(text, stats):
	patts = prior_patts('TARGET', stats)
	return results('TARGET', patts, stats, text)

def get_victim(text, stats):
	patts = prior_patts('VICTIM', stats)
	return results('VICTIM', patts, stats, text)

def pstats(stats):
	lst = []
	for slot,slot_d in stats.items():
		for entry,cnt in slot_d.items():
			#print '%s\t%s\t%s' % (slot, entry, cnt)
			lst.append((slot,entry,cnt))

	lst.sort(key=lambda (x,y,z): z)
	for e in lst:
		if e[0] == 'WEAPON':
			print e


if __name__ == '__main__':
	get_weapon('lsdkjf sd', answr_dict())
