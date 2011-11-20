from __future__ import with_statement
import os, sys

DIR1 = 'developset/test_set/texts/'
DIR2 = 'developset/test_set/answerkeys/'

FI1 = 'AGGREGATE'


def agg_dir(d):
	with open(d + FI1, 'w') as w:

		for path, dirs, fis in os.walk(d):
			for fi in fis:
				to_opn = path + fi
				if to_opn == FI1:
					continue

				with open(path + fi) as f:
					for l in f.readlines():
						w.write(l)
				# TODO: SHOULD THERE BE A DELIMITER HERE? e.g., '******'


if __name__ == '__main__':
	agg_dir(DIR1)
	agg_dir(DIR2)
