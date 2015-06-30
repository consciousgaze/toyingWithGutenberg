from operator import itemgetter
import numpy as np
import os, subprocess, util, pickle

def main():
	buildSematicOrder()
	print findCharacterWords(util.authors[0], util.authors[2])


def mostDistinct(word1, word2, rownames, k, dumpName = None):
	differ = []
	for word in rownames:
		dist = word1.index(word) - word2.index(word)
		if dist < 0:
			dist = -dist
		differ.append((word, dist))
	tmp = sorted(differ, key=itemgetter(1), reverse=True)
	if dumpName != None:
		pickle.dump(tmp, open(util.modelDir+dumpName, 'wb'))
	return tmp[:k]

def loadGloVe(author):
	f = open(util.modelDir+author+'.txt')
	rownames = []
	glove = []
	for l in f:
		l = l.split(' ')
		rownames.append(l[0])
		values = []
		for v in l[1:]:
			values.append(float(v))
		glove.append(values)
	glove = np.array(glove)
	return glove, rownames

def buildGloVe(author, vocabulary = 'vocabulary.txt', rebuild = False):
	'''
		build GloVe model. Fine tune the model paramter here
	'''
	if rebuild or not os.path.exists('%s%s.txt'%(util.modelDir, author)):
		print 'Building GloVe model for %s -----------' % author
		docFname = 'corpus'
		util.gathterDocs([author], docFname)
		# build occurance file
		# ../glove/cooccur -memory 4.0 -vocab-file vocabulary -verbose 2 -window-size 15 < docFname > coocur.bin
		cmd = '../glove/cooccur'
		param = '-memory 4.0 -vocab-file %s -verbose 2 -window-size 15 < %s > coocur.bin' % (util.modelDir+vocabulary, docFname)
		os.system(cmd+' '+param)
		# shuffle occurance file
		# ../glove/shuffle -memory 4.0 -verbose 2 < coocur.bin > shuffle.bin
		cmd = '../glove/shuffle'
		param = '-memory 4.0 -verbose 2 < coocur.bin > shuffle.bin'
		os.system(cmd+' '+param)
		# build glove
		# ../glove/glove -save-file glove_+$author -threads 4 -input-file shuffle.bin -x-max 10 -iter 50 -vector-size 50 -binary 2 -vocab-file vocabulary -verbose 2
		cmd = '../glove/glove'
		param = '-save-file glove_%s -threads 4 -input-file shuffle.bin -x-max 10 -iter 50 -vector-size 50 -binary 2 -vocab-file %s -verbose 2' % ("ModelFiles/"+author, util.modelDir+vocabulary)
		os.system(cmd+' '+param)

		os.remove(docFname)
		os.remove('shuffle.bin')
		os.remove('coocur.bin')

def buildVocabulary(rebuild = False):
	# check if the vocabulary is there and if rebuild
	if rebuild or not os.path.exists(util.modelDir+'vocabulary.txt'):
		vocFileName = 'voc.txt'
		util.gathterDocs(util.authors, vocFileName)
		print 'voc.txt done'
		# execute ../glove/vocab_count -min-count 5 -verbose 2 < vocFileName > vocabulary.txt
		cmd = '../glove/vocab_count'
		param = '-min-count 5 -verbose 2 < %s > %svocabulary.txt' % (vocFileName, util.modelDir)

		os.system(cmd+' '+param)
		os.remove(vocFileName)

def buildSematicOrder(rebuild = False):
	# build voc file with all docs
	buildVocabulary()

	# for each author build glove model
	for author in util.authors:
		buildGloVe(author)

	# build sematic orientation for each author
	seed_pos = ['good', 'nice', 'excellent', 'positive', 'fortunate', 'correct', 'superior']
	seed_neg = ['bad', 'nasty', 'poor', 'negative', 'unfortunate', 'wrong', 'inferior']

	for author in util.authors:
		if rebuild or not os.path.exists(util.modelDir+'%s_sematic.p'%author):
		    print 'Processing %s --------------------' % author
		    mat, rownames = loadGloVe(author)
		    sm1 = util.so_seed_matrix(seed_neg, mat, rownames)
		    sm2 = util.so_seed_matrix(seed_pos, mat, rownames)
		    # scores = dict()
		    # for i in xrange(len(rownames)):
		    # 	scores[rownames[i]] = so_row_func(mat[i], sm1, sm2)
		    scores = [[rownames[i], util.so_row_func(mat[i], sm1, sm2)] for i in xrange(len(mat))]
		    wordOrder = [word for word, score in sorted(scores, key=itemgetter(1), reverse=False)]
		    pickle.dump(wordOrder, open(util.modelDir+author+'_sematic.p', 'wb'))


def findCharacterWords(author1, author2):
	rownames = util.loadRowNames()
	print 'Row name loaded'
	# find the most distinct words
	return mostDistinct(pickle.load(open(util.modelDir+author1+'_sematic.p')), 
				 		pickle.load(open(util.modelDir+author2+'_sematic.p')), 
				 		rownames, 5, dumpName = 'example.p')


if __name__ == '__main__':
	main()
