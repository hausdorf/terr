from __future__ import division, with_statement
import os, sys, collections, re, string
from ctx_hist import CTX_HIST
from nltk import sent_tokenize, word_tokenize, pos_tag, RegexpParser, ne_chunk


TST = {'BOMB SET IN AN ICE CREAM CART': 1, 'POWERFUL BOMB': 2, 'BOMB': 29, 'ROCKET': 2, 'TNT': 1, 'MACHINEGUNS IN TRIPODS': 1, 'THE BOMB': 1, 'CARBOMB': 1, 'TRUCK': 1, 'DYNAMITE CHARGE': 3, 'TERRORIST BOMBS': 1, 'EXPLOSIVES': 5, 'CAR BOMB': 5, 'SEVERAL DYNAMITE ATTACKS': 1, 'A BOMB': 2, '9-MM WEAPONS': 1, '-': 318, 'HELICOPTER GUNSHIP': 1, 'INCENDIARY BOMB': 1, 'AK-47S': 1, 'VEHICLE LOADED WITH EXPLOSIVES': 1, 'HELICOPTER GUNSHIPS': 1, 'PACKAGES OF DYNAMITE': 1, 'SUBMACHINEGUN': 1, 'EXPLOSIVE DEVICE': 2, 'MACHINEGUN': 2, 'ROCKETS': 3, 'EIGHT BOMBS': 1, 'MINE': 1, 'EXPLOSIVE CHARGES': 1, 'BOMB BLAST': 1, 'GRENADES': 2, 'BOMBS': 12, 'DYNAMITE STICKS': 2, 'GRENADE': 2, 'HEAVY CALIBER WEAPONS': 1, 'BULLET': 1, '.22 CALIBER GUN': 1, 'MORTAR': 2, 'FOUR BOMBS': 1, 'MACHINE-GUN': 1, 'EXPLOSIVE DEVICES': 5, 'BULLETS': 1, 'CHARGE OF DYNAMITE': 1, 'AT LEAST SIX BOMBS': 1, 'DYNAMITE': 10, 'MACHINEGUNS': 2, 'DYNAMITE ATTACKS': 1}


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

def liter_(i):
	if i == 1 or i == 3:
		for f in fiter(ANSWR1):
			for l in f.readlines():
				yield l

	if i == 2 or i == 3:
		for f in fiter(ANSWR2):
			for l in f.readlines():
				yield l

def liter_all_f():
	for f in fiter(ANSWR1):
		for l in f.readlines():
			yield l

	for f in fiter(ANSWR2):
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

def results(thing, patts, stats, text):
	rslts = []
	rslt = collections.defaultdict(lambda:0)
	"""
	for e in patts:
		res = re.search(' ([a-zA-Z]+-)?' + e + '(S)? ', text)
		if res:
			#print res.group(0)
			rslts.append((res.group(0).strip(), stats[thing][e]))

	rslts = filter(lambda(x,y): y > 1, rslts)
	rslts.sort(key=lambda(x,y):y, reverse=True)
	"""

	for e in patts:
		res = re.search(' ([a-zA-Z]+-)?' + e + '(S)? ', text)
		if res:
			sents = [s for s in sent_tokenize(text)]
			for s in sents:
				if not re.search(' ([a-zA-Z]+-)?' + e + '(S)? ', s):
					continue
				pos = pos_tag(word_tokenize(s.lower()))
				scr = score_w_hist(pos, CTX_HIST)
			#sents = map(pos_tag, map(word_tokenize,
			#	[s for s in sent_tokenize(text.lower())]))
				if thing == 'WEAPON':
					rslts.append((res.group(0).strip(), TST.get(e,0)))
					continue

				if scr > 0:
					print scr, e
					rslts.append((res.group(0).strip(), stats[thing][e]))
					rslt[res.group(0).strip()] += scr

	print rslts


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
