from __future__ import with_statement


def find_communique(data):
	ldata = len(data)
	rslt = []

	for i in range(ldata):
		if data[i][:12] == '[COMMUNIQUE]':
			rslt.append(data[i][12:])
			while i+1 < ldata:
				curr = data[i+1]
				rslt.append(curr)
				if curr.count(']') > 0:
					return ' '.join(rslt)
				i += 1

	return None

def proc_meta(data):
	sp = data.split()

	return find_communique(sp)


if __name__ == '__main__':
	with open('sample-textfile.txt') as f:
		proc_meta(f.read())
