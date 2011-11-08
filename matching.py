from aslog import groups

PATT_WEAP = ['%s exploded']
PATT_PIND = ['%s kidnapped']
PATT_PORG = []
PATT_TARG = ['%s exploded', 'attack on %s', 'exploded in %s', 'occurred on',
		'destroyed %s', 'exploded on %s']
PATT_VICT = ['murder of %s', 'assassination of %s', '%s was killed',
		'%s was kidnapped', 'attack on %s', '%s was injured',
		'death of %s', 'claimed %s', '%s was wounded', 'destroyed %s',
		'%s was murdered', '%s died']


def fmt(l):
	grp = list(groups(l, key=lambda x:x.split('/')[1]))
	nplst = [e.split('/')[0] for e in grp[-1]]
	return ' '.join(nplst)

def find_thing(prsed, patterns):
	for patt in patterns:
		pattspl = patt.split()
		lpattspl = len(pattspl)

		prsedspl = prsed.split()
		lprsedspl = len(prsedspl)

		i = 0
		j = 0
		while i < lprsedspl and j < lpattspl:
			curr = prsedspl[i].split('/')[0]
			if pattspl[j] == '%s' or curr == pattspl[j]:
				j += 1
			else:
				i -= j
				j = 0

			if j == lpattspl:
				yield fmt(prsedspl[:i])
			i += 1

def find_weapon(prsed):
	found = list(find_thing(prsed, PATT_WEAP))[0]
	if len(found) == 0:
		return '-'
	return found

def find_perp_indiv(prsed):
	found = list(find_thing(prsed, PATT_PIND))[0]
	if len(found) == 0:
		return '-'
	return found

def find_perp_org(prsed):
	found = list(find_thing(prsed, PATT_PORG))[0]
	if len(found) == 0:
		return '-'
	return found

def find_target(prsed):
	found = list(find_thing(prsed, PATT_TARG))[0]
	if len(found) == 0:
		return '-'
	return found

def find_victim(prsed):
	found = list(find_thing(prsed, PATT_VICT))[0]
	if len(found) == 0:
		return '-'
	return found


def match(prsed):
	result = {'INCIDENT': '-', 'WEAPON': '-', 'PERP INDIV': '-',
			'PERP ORG': '-', 'TARGET': '-', 'VICTIM': '-'}

	result['WEAPON'] = find_weapon(prsed)
	result['PERP INDIV'] = find_perp_indiv(prsed)
	result['PERP ORG'] = find_perp_org(prsed)
	result['TARGET'] = find_target(prsed)
	result['VICTIM'] = find_victim(prsed)

	return result

if __name__ == '__main__':
	s = 'my/NNS cow/NNS exploded/VBD cow/NNS'
	p = ['%s cow is cow']

	print find_weapon(s)
	#for e in find_thing(s, p):
		#print e
