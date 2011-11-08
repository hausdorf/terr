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
		pattspl = patt.upper().split()
		lpattspl = len(pattspl)

		prsedspl = prsed.upper().split()
		lprsedspl = len(prsedspl)

		i = 0
		j = 0
		while i < lprsedspl and j < lpattspl:
			curr = prsedspl[i].split('/')[0]
			if curr == 'EXPLODE':
				print 'M', pattspl[j], curr
			if pattspl[j] == '%S' or curr == pattspl[j]:
				j += 1
			else:
				i -= j
				j = 0

			if j == lpattspl:
				yield fmt(prsedspl[:i])
			i += 1

def find_weapon(prsed):
	found = list(find_thing(prsed, PATT_WEAP))
	if len(found) == 0:
		return '-'
	return found[0]

def find_perp_indiv(prsed):
	found = list(find_thing(prsed, PATT_PIND))
	if len(found) == 0:
		return '-'
	return found[0]

def find_perp_org(prsed):
	found = list(find_thing(prsed, PATT_PORG))
	if len(found) == 0:
		return '-'
	return found[0]

def find_target(prsed):
	found = list(find_thing(prsed, PATT_TARG))
	if len(found) == 0:
		return '-'
	return found[0]

def find_victim(prsed):
	found = list(find_thing(prsed, PATT_VICT))
	if len(found) == 0:
		return '-'
	return found[0]


def first_line(prsed):
	spl = prsed.split('\n')[0]
	if len(spl) > 0:
		return spl
	else:
		return prsed.split('\n')[0]


def match(prsed):
	result = {'INCIDENT': '-', 'WEAPON': '-', 'PERP INDIV': '-',
			'PERP ORG': '-', 'TARGET': '-', 'VICTIM': '-'}

	line = first_line(prsed)

	result['WEAPON'] = find_weapon(line)
	result['PERP INDIV'] = find_perp_indiv(line)
	result['PERP ORG'] = find_perp_org(line)
	result['TARGET'] = find_target(line)
	result['VICTIM'] = find_victim(line)

	return result

if __name__ == '__main__':
	s = 'my/NNS cow/NNS exploded/VBD cow/NNS'
	p = ['%s cow is cow']

	print find_weapon(s)
	#for e in find_thing(s, p):
		#print e
