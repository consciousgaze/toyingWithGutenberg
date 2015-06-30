from nltk.corpus import brown
from nltk.model.ngram import NgramModel as NM
from nltk.probability import LidstoneProbDist, WittenBellProbDist
import pickle, util, os
from collections import Counter()
from random import rand()

trainedWeight = None

def buildNgramModels():
	outputFile = 'out.txt'
	for author in [util.authors[0]]:
		print util.authors[:1]
		estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
		util.gathterDocs([author], outputFile)
		f = open(outputFile)
		train = f.read()#.split()
		f.close()
		ngrammodel = NM(5, train, estimator = estimator)
		pickle.dump(ngrammodel, open(author+'_ngram.model', 'w'))
		os.remove(outputFile)
	# estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
	# lm = NM(3, brown.words(categories='news'), estimator=estimator)

def loadModels(author):
	return pickle.load(open('%s_ngram.model'))

def classify(text, weight = lambda x:1.):
	'''
		classifies a text
	'''
	authors = dict()
	authorHits = Counter()
	for author in util.authors
		authors[author] = loadModels(author)
	words = text.split()
	if len(words) < 5:
		raise Exception('Input Too Short!')

	for i in range(len(words -5)):
		grams = words[i:i+4]
		word = words[i+5]
		for author in util.authors:
			authorHits[author] += authors[author].prob(word, grams)*weight(word)

	mx = float('-inf')
	rlt = None
	for author in authorHits:
		if authorHits[author] > mx:
			mx = authorHits[author]
			rlt = author

	return rlt

def gloVeWeight(word, author, alph = 600000.):
	'''
		return the word weight base on the word distnace
		between the author GloVe model and the GloVe model
		trianed with whole text

		word is the input word
		author is the pretrained word distance dict
		aurthor[word] = abs(author_sematic[word] - common_semantic[word])
	'''
	return author[word]/alph

def getTrainedWeight(word, author, rownames):
	'''
		trained weight with certain rules
		both author and word are strings
	'''
	try:
		return trainedWeight[word]
	except:
		trainedWeight = pickle.load(open('trainedWeight.p'%author))
		return trainedWeight[author][word]

def trainWeight(train, trainY, maxIter = 100, alpha = .1):
	rownames = util.loadRowNames()
	trainedWeight = dict()
	for author in util.authors:
		trainedWeight[aurthor] = dict()
		for word in rownames:
			trainedWeight[author][word] = rand()

	for i in range(maxIter):
		for idx in range(len(train)):
			text = train[idx]
			rlt = classify(text, wetight = getTrainedWeight)
			for word in text.split():
				if rlt == trainY[idx]:
					trainedWeight[rlt][word] += 0.1
				else:
					trainedWeight[rlt][word] -= 0.1

	pickle.dump(trainedWeight, open('trainedWeight.p', 'wb'))



