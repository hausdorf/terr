from aslog import groups
import collections

PATT_WEAP = ['<np> exploded']
PATT_PIND = ['<np> kidnapped']
PATT_PORG = []
PATT_TARG = ['<np> exploded', 'attack on <np>', 'exploded in <np>',
		'occurred on', 'destroyed <np>', 'exploded on <np>']
PATT_VICT = ['murder of <np>', 'assassination of <np>', '<np> was killed',
		'<np> was kidnapped', 'attack on <np>', '<np> was injured',
		'death of <np>', 'claimed <np>', '<np> was wounded',
		'destroyed <np>', '<np> was murdered', '<np> died']


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
			if pattspl[j] == '<NP>' or curr == pattspl[j]:
				j += 1
			else:
				i -= j
				j = 0

			if j == lpattspl:
				yield fmt_prev(prsedspl[:i]), patt
				j = 0
				i -= 1
			i += 1

def agg_weapon(prsed):
	found = list(find_thing(prsed, PATT_WEAP))
	if len(found) == 0:
		return '-'
	return found

def agg_perp_indiv(prsed):
	found = list(find_thing(prsed, PATT_PIND))
	if len(found) == 0:
		return '-'
	return found

def agg_perp_org(prsed):
	found = list(find_thing(prsed, PATT_PORG))
	if len(found) == 0:
		return '-'
	return found

def agg_target(prsed):
	found = list(find_thing(prsed, PATT_TARG))
	if len(found) == 0:
		return '-'
	return found

def agg_victim(prsed):
	found = list(find_thing(prsed, PATT_VICT))
	if len(found) == 0:
		return '-'
	return found

def tally_rslts(d, rslts, slot):
	if rslts == '-':
		return

	for chnk, rslt in rslts:
		d[slot][rslt] += 1

def aggregate(prsed):
	
	result = {
		'INCIDENT': collections.defaultdict(lambda:0),
		'WEAPON': collections.defaultdict(lambda:0),
		'PERP INDIV': collections.defaultdict(lambda:0),
		'PERP ORG': collections.defaultdict(lambda:0),
		'TARGET': collections.defaultdict(lambda:0),
		'VICTIM': collections.defaultdict(lambda:0)
		}

	tally_rslts(result, agg_weapon(prsed), 'WEAPON')
	tally_rslts(result, agg_perp_indiv(prsed), 'PERP INDIV')
	tally_rslts(result, agg_perp_org(prsed), 'PERP ORG')
	tally_rslts(result, agg_target(prsed), 'TARGET')
	tally_rslts(result, agg_victim(prsed), 'VICTIM')

	return result

def p(d):
	for slot,d1 in d.items():
		for patt,cnt in d1.items():
			print slot, patt, cnt


if __name__ == '__main__':
	s = 'my/NNS neat/NNS cow/NNS exploded/VBD cow/NNS exploded/VBD cow/NNS cow/NNS cow/NNS exploded/VBD'

	p(aggregate(s))
	#for e in find_thing(s, p):
		#print e
