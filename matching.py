from __future__ import division
from aslog import groups
import collections, math


def fmt_prev(l):
	grp = list(groups(l, key=lambda x:x.split('/')[1]))
	nplst = [e.split('/')[0] for e in grp[-1]]
	return ' '.join(nplst)

# find_thing : prsed_string -> patterns -> list_of_words, pattern
def find_thing(prsed, patterns):
	for patt in patterns:
		pattspl = patt.upper().split()
		lpattspl = len(pattspl)

		prsedspl = prsed.upper().split()
		lprsedspl = len(prsedspl)

		i = 0
		j = 0
		while i < lprsedspl and j < lpattspl:
			curr = prsedspl[i].split('/')[0]
			if pattspl[j] == '<VICTIM>' or curr == pattspl[j]:
				j += 1
			else:
				i -= j
				j = 0

			if j == lpattspl:
				#yield fmt_prev(prsedspl[:i]), patt
				yield patt
				j = 0
				i -= 1
			i += 1

def cmp(irr, rel):
	irr_dict = collections.defaultdict(lambda:0)
	for i in irr:
			irr_dict[i.split(':')[-1]] += 1

	rel_set = collections.defaultdict(lambda:[])
	for r in rel:
			r_spl = r.split(':')
			#rel_set[r.split(':')[-1]].append(r)
			rel_set[r_spl[-1].strip()].append(r_spl[:-1])

	rel_dict = collections.defaultdict(lambda:0)
	for r in rel:
			rel_dict[r.split(':')[-1]] += 1

	res = []
	for patt,cnt in rel_dict.items():
			tot = cnt + irr_dict[patt]
			scr = (cnt/tot) * math.log(tot,2)
			#print scr
			if scr > 0.5:
					res.append((patt,scr,rel_set[patt]))

	res.sort(key=lambda(x,y,z):y,reverse=True)

	return res

def aggregate(prsed, patts):
	cnts = collections.defaultdict(lambda: 0)
	for l in prsed:
		for t in find_thing(l, patts):
			cnts[t] += 1

	return cnts

def p(d):
	for slot,d1 in d.items():
		for patt,cnt in d1.items():
			print slot, patt, cnt


if __name__ == '__main__':
	s = 'my/NNS neat/NNS cow/NNS exploded/VBD cow/NNS exploded/VBD cow/NNS cow/NNS cow/NNS exploded/VBD'

	p(aggregate(s))
	#for e in find_thing(s, p):
		#print e
