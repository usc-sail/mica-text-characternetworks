
import re
from string import punctuation
from funcy import walk_values 
from collections import Counter

class VLIWC(object):
	def __init__(self, dict_file, cat_file = ""):
		self._readDictFile(dict_file, cat_file)

	def _readDictFile(self, dict_file, cat_file):
		if len(dict_file) == 0:
			raise Exception("No dictionary file!")

		if len(cat_file) == 0:
			self._readDictFileWithCategories(open(dict_file, 'r').readlines())
		else:
			self._readDictFileWithCategories(_merge(cat_file, dict_file))

	####################################################################
	# Reads a LIWC dict file (format: % cats % words)
	# It adds missing categories 
	# Returns mapping between indexes and categories
	# 		  mapping between words and categories
	# Saves resulting objects into object
	####################################################################
	def _readDictFileWithCategories(self, file_contents):
		cats = 0
		catDict, wordDict = {}, {}

	
		for line in file_contents:
			line = line.strip()

			if line == "%":
				cats = cats + 1
			elif cats == 1:

				try:
					idx, category = line.split("\t")
					catDict[int(idx)] = category
				except:
					continue

			elif cats == 2:

				try:
					word, categories = line.split("\t", 1)

					# * in LIWC dictionaries is not the same as * in re, replace accordingly
					word = word.replace("*", ".*")

					wordDict[re.compile("\\b{}\\b".format(word), flags = re.IGNORECASE)] = [int(x) for x in categories.split("\t")]
				except:
					print("Error in dict: {}".format(line))
					continue

		# Manually add LEN>6 word category
		catDict[len(catDict) + 1] = "Sixltr"
		wordDict[re.compile("\w{7,}")] = [len(catDict)]

		# Manually add missing categories
		for cat, r in [("AllPct", "[\.,\/#!$%\^&\*;:{}=\-_`~()]"),
					   ("Colon", ":"),
					   ("Comma", ","), 
					   ("Dash", "-"),
					   ("Exclam", "!"), 
					   ("Numerals", "[0-9]+"),
					   ("OtherP", "[\/#$%\^&\*{}=\_`~]"),
					   ("Parenth", "[)()]"),
					   ("Period", "\."),
					   ("QMark", "\?"),
					   ("Quote", "\""),
					   ("SemiC", ";"),
					   ("Apostro", "'")]:
			catDict[len(catDict) + 1] = cat
			wordDict[re.compile(r)] = [len(catDict)]

		self.catDict = catDict
		self.wordDict = wordDict

		return (catDict, wordDict)

	####################################################################
	# This method processes the contents of a filename
	####################################################################
	def processFile(self, filename):
		with open(filename, 'r') as inpt:
			return self.processText(inpt.readlines())


 	####################################################################
	# This method processes a text
	####################################################################
	def processText(self, text):
		(counters, llens, lines) = zip(*map(self._mapper, text.split("\n")))

		# Reduce list of counters to one count
		WC = self._reducer(counters)

		# Total number of words and words per segment
		num_words = sum(llens)
		wps = num_words / 1.0 #TODO: consider segments

		# Convert to percentages
		WC = walk_values(lambda x: "{:.2f}".format(100 * x / float(num_words)), dict(WC))

		#
		WC['num_words'] = num_words
		WC['wps'] = wps 

		return WC

 	####################################################################
 	####################################################################
	@staticmethod
	def _merge(*args):
		res = []
		for f in args:
			with open(f, 'r') as inpt:
				res.extend(inpt.readlines())
		return res

 	####################################################################
 	####################################################################
	def _reducer(self, counters):
		return sum(counters, Counter())

 	####################################################################
 	####################################################################
	def _mapper(self, line):
		words = line.strip().split(" ")
		return (Counter([self.catDict[y] for x in [self.wordDict[_] for t in words
														  		  for _ in self.wordDict.keys()
														  		  if _.match(t)]
									   for y in x]),
				len([t for t in words if t not in punctuation]),
				int(len(line.strip()) > 0))