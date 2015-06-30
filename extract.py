from zipfile import ZipFile as zf
from os import listdir, path, makedirs
from re import match
from collections import Counter
import pickle, shutil

base = 'www.gutenberg.lib.md.us'
root = '/Users/Ted/Downloads/tmp'
authorDocs = Counter()
authors = [ 'honore de balzac',
			'samuel pepys',
			'anonymous 139',
			'u.s. copyright office',
			'mark twain (samuel clemens)',
			'w.w. jacobs',
			'various 1967',
			'winston churchill'
		   ]

def extract(p):
	for f in listdir(p):
		try:
			if path.isdir(p+'/'+f):
				extract(p+'/'+f)
			if match('.*zip', f):
				zipFile = zf(p+'/'+f)
				for i in zipFile.infolist():
					# print i.filename
					if match(".*txt", i.filename):
						zipFile.extract(i, p)
				zipFile.close()
		except:
			print p + '/'+f

def count(p):
	for f in listdir(p):
		try:
			if path.isdir(p+'/'+f):
				count(p+'/'+f)
			if match('.*txt', f):
				txt = open(p+'/'+f)
				for l in txt:
					if l.startswith("Author:"):
						author = l.split('Author:')[1].strip().lower()
						authorDocs[author] += 1
						break
		except:
			print p + '/'+f


def pick(p):
	for f in listdir(p):
		try:
			# print p, f
			if path.isdir(p+'/'+f):
				pick(p+'/'+f)
			if match('.*txt', f):
				txt = open(p+'/'+f)
				cnt = 0 
				for l in txt:
					cnt += 1
					if cnt > 100:
						# print
						break
					# print l
					if l.startswith("Author:"):
						author = l.split('Author:')[1].strip().lower()
						# print author, authors
						if author in authors:
							# move file to right folder
							if not path.exists(root+'/'+author):
   								makedirs(root + '/' + author)
   							shutil.copy2(p+'/'+f, root+'/'+author+'/'+f)
						break
				txt.close()
		except:
			print p + '/'+f

pick(base)