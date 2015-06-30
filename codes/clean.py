import os, re
base = 'winston churchill'
'*** START OF THIS PROJECT GUTENBERG'
for d in os.listdir(base):
	try:
		tmp = d.split('.')[0]
		int(tmp)
		doc = ''
		f = open(base+'/'+d)
		flag = False
		ignore = False
		for l in f:
			if l.startswith('Title:'):
				flag = True
			if flag:
				if re.match('\s*\n', l):
					if not ignore:
						ignore = True
						doc += '\n'
				else:
					# print l
					ignore = False
					doc += l.strip() + ' '
		f.close()
		# doc = doc.replace('(\s*\n\s*)+', '\n')
		# doc = doc.replace('\r+', '\r')
		f = open(base+'/c_'+d, 'w')
		f.write(doc)
		f.close()
	except:
		pass

