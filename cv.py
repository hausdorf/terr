from __future__ import division
import re
from answer_stats import answr_dict_, results



def test_txt(fn):
	f = open(fn)

	doc = []
	for l in f.readlines():
		if re.search('-MUC', l):
			if len(doc) > 0:
				yield name, ''.join(doc)
				doc = []

			name = l.strip().split()[0]
		else:
			doc.append(l)

def ans_txt(fn, thing):
	f = open(fn)

	d = {}
	for l in f.readlines():
		if re.search('-MUC', l):
			name = l.strip().split()[1]

		if re.search(thing, l):
			t = l.split(':')[1].strip()
			d[name] = t

	f.close()
	return d

def learn_weights(train, key):
	tst = {}
	retr = 0
	for name,text in test_txt('developset/texts/AGGREGATE'):
		r = results('WEAPON', train.keys(), {'WEAPON': train}, text)
		if r != '-':
			tst[name] = key[name].split('/').count(r[0][0]) == 1
			retr += 1

	for k,v in tst.items():
		if tst[k]:
			for a in key[k].split('/'):
				print train[a]
				train[a] += 1
		else:
			for a in key[k].split('/'):
				print train[a]
				train[a] -= 1

	ans = len(filter(lambda (k,v): v != '-', key.items()))
	corr = len(filter(lambda (k,v): v, tst.items()))
	prec = corr / retr
	reca = corr / ans
	print train
	return ((prec * reca) / (prec + reca)) * 2

def cv_boost(thing):
	print "Buildin' dictionary..."
	f = answr_dict_(1)[thing]

	print "Building' key..."
	k = ans_txt('developset/answers/AGGREGATE', 'WEAPON')

	print "Learnin' weights..."
	lst_scr = learn_weights(f, k)
	print lst_scr
	while lst_scr < 0.60:
		lst_scr = learn_weights(f, k)
		print lst_scr


if __name__ == '__main__':
	cv_boost('WEAPON')
