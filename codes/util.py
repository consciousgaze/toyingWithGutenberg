from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import os, re, scipy
from scipy.spatial import distance
modelDir = 'glove_ModelFiles/'

authors = ['honore_de_balzac', 
		   'mark_twain', 
		   'samuel_pepys', 
		   'ww_jacobs', 
		   'winston_churchill']
delim = '*** START OF THIS PROJECT GUTENBERG'

def loadRowNames():
	f = open(modelDir+'vocabulary.txt')
	rownames = []
	for l in f:
		rownames.append(l.split()[0])
	f.close()
	return rownames

def tokenize():
	voc = CountVectorizer(decode_error = 'replace')
	data = []
	for author in authors:
		for fname in os.listdir(author):
			if fname.startswith('c_'):
				doc = open(author+'/'+fname).read()
				data.append(doc)
	voc.fit(data)
	return voc

def prepGloVe():
	for author in authors:
		doc = ''
		for fname in os.listdir(author):
			if fname.startswith('c_'):
				doc += open(author+'/'+fname).read().replace('\s+', ' ')
		tmp = open(author+'.txt', 'w')
		tmp.write(doc)
		tmp.close()


def gathterDocs(authors, outputFileName):
	doc = ''
	for author in authors:
		for fname in os.listdir(author):
			if fname.startswith('c_'):
				f = open(author+'/'+fname)
				flag = False
				for l in f:
					if flag:
						doc += l
					else:
						if l.startswith(delim):
							flag = True
				f.close()
	f = open(outputFileName, 'w')
	f.write(doc)
	f.close()



# functions from cs224u
def cosine(u, v):
    # Use scipy's method:
    return distance.cosine(u, v)
    # Or define it yourself:
    # return 1.0 - (np.dot(u, v) / (vector_length(u) * vector_length(v)))

def so_seed_matrix(seeds, mat, rownames):
    indices = [rownames.index(word) for word in seeds if word in rownames]
    if not indices:
        raise ValueError('The matrix contains no members of the seed set: %s' % ",".join(seeds))
    return mat[np.array(indices)]

def so_row_func(row, sm1, sm2, distfunc = cosine):
    val1 = np.sum([distfunc(row, srow) for srow in sm1])
    val2 = np.sum([distfunc(row, srow) for srow in sm2])
    return val1 - val2  
