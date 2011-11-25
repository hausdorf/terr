from __future__ import division, with_statement
import os, sys, collections, re, string


ANSWR1 = 'developset/answers/'
ANSWR2 = 'answerkeys/'
ALLWD = set(['INCIDENT', 'WEAPON', 'PERP INDIV', 'PERP ORG', 'TARGET', 'VICTIM'])

def fiter(p):
	for pth, dirs, files in os.walk(p):
		for file in files:
			r = open(pth + '/' + file)
			yield r
			r.close()

def liter_all_f():
	for f in fiter(ANSWR1):
		for l in f.readlines():
			yield l

	"""
	for f in fiter(ANSWR2):
		for l in f.readlines():
			yield l
	"""

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

def results(thing, patts, stats, text):
	rslts = []
	for e in patts:
		res = re.search('([a-zA-Z]+-)?' + e + '(S|ING)* ', text)
		if res:
			#print res.group(0)
			rslts.append((res.group(0).strip(), stats[thing][e]))

	rslts.sort(key=lambda(x,y):y, reverse=True)
	if len(rslts) > 0:
		#print rslts
		return rslts[0][0]
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
