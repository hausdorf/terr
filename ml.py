import re, collections
from answer_stats import fiter
from nltk import sent_tokenize, word_tokenize, pos_tag, RegexpParser, ne_chunk


DEV_KEY = 'developset/answers/'
DEV_TXT = 'developset/texts/'
V_TAGS = set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])


def fmt_ln(line):
	spl = line.split(':')

	if len(spl) < 2:
		return

	terms = [t.strip() for t in re.split('/|\[|\]', spl[1].strip())]

	return spl[0], terms

def iter_weapons_key():
	lastid = ''
	for f in fiter(DEV_KEY):
		for l in f.readlines():
			l = fmt_ln(l)

			if l and l[0] == 'ID':
				lastid = l[1][0]

			if l and l[0] == 'WEAPON':
				yield lastid, l[1]

def iter_weapons_txt():
	lastid = ''
	for f in fiter(DEV_TXT):
		id = f.readline().strip()
		txt = f.read()
		yield id.split()[0], txt

def ctxt(sent, lim, i, ln):
	if i - ln - lim + 1 < 0:
		left = 0
	else:
		left = i - ln - lim + 1

	if i + lim > len(sent):
		right = len(sent)
	else:
		right = i + lim + 1

	return sent[left : i - ln + 1], sent[i + ln : right]

def update_features(ans, ctx, d):
	for c in ctx:
		if c[1] in V_TAGS:
			d[c[0]] += 1

def match(ans, sent):
	ans_words = word_tokenize(ans)
	nawords = len(ans_words)
	nswords = len(sent)
	wdw_len = 5

	i = 0
	j = 0
	while i < nswords:

		curr = sent[i][0].upper()
		if curr == ans_words[j]:
			j += 1
		elif j > 0:
			i -= j
			j = 0

		if j == nawords:
			l,r = ctxt(sent, wdw_len, i, len(ans_words))
			yield l, r
			i = i - j + 1
			j = 0

		i += 1

def iter_ctxts(ans, sents, d):
	for a in ans:
		for s in sents:
			for l,r in match(a, s):
				update_features(a, s, d)

def weapons_answers():
	ans = dict((id, weapon) for id,weapon in iter_weapons_key())
	return ans

def weapons_text():
	txt = dict((id,txt) for id,txt in iter_weapons_txt())
	return txt

def train_weapons():
	print "Buildin' answer dictionary..."
	wa = weapons_answers()

	print "Buildin' text dictionary..."
	wt = weapons_text()

	print "Cyclin' through text and trainin'"
	d = collections.defaultdict(lambda:0)
	for k,txt in weapons_text().items():
		ans = wa[k]
		if ans[0] == '-':
			continue

		sents = map(pos_tag, map(word_tokenize,
			[s for s in sent_tokenize(txt.lower())]))

		iter_ctxts(ans, sents, d)

	print d

	# TODO: AGGREGATE STATISTICS HERE! WE'RE LOOKING FOR PATTERNS THAT
	# INDICATE CERTAIN WEAPONS.


if __name__ == '__main__':
	train_weapons()
