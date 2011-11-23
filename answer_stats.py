from __future__ import division, with_statement
import os, sys, collections, re


ANSWR = 'answerkeys/'
ALLWD = set(['INCIDENT', 'WEAPON', 'PERP INDIV', 'PERP ORG', 'TARGET', 'VICTIM'])


def fiter():
	for pth, dirs, files in os.walk(ANSWR):
		for file in files:
			r = open(pth + '/' + file)
			yield r
			r.close()

def liter_all_f():
	for f in fiter():
		for l in f.readlines():
			yield l

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

def get_weapon(text, stats):
	patts = []
	for entry in stats['WEAPON']:
		if entry == '-':
			continue

		patts.append(entry)

	rslts = []
	for e in patts:
		res = re.search(e, text)
		if res:
			rslts.append((e, stats['WEAPON'][e]))

	rslts.sort(key=lambda(x,y):y, reverse=True)
	if len(rslts) > 0:
		return rslts[0][0]
	else:
		return '-'

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
