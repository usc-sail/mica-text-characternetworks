import untangle
import sys,json, re
from collections import defaultdict, Counter
import numpy as np
import networkx as nx
import scipy.io 
from funcy import walk_keys 
import string
from matfile_utils import loadmat

punct_elim = str.maketrans({key:' ' for key in string.punctuation})

def read(filename, threshold = 2):
	
	doc = untangle.parse(filename)
	movie_name = doc.movie['title']

	transitions = []
	for diag in doc.movie.dialogue:
		speaker = diag.speaker[0].cdata 

		for spk in diag.speaker[1:]:
			transitions.append((speaker, spk.cdata))
			speaker = spk.cdata 

	# Filter empty speakers and same speaker
	transitions = list(filter(lambda x: x[0]!=x[1], transitions))
	transitions = list(filter(lambda x: len(x[0])>0 and len(x[1])>0, transitions))

	# 
	weights = Counter(transitions)
	char_list = np.array(sorted(list(set([y for x in map(lambda x: [x[0], x[1]], weights.keys())
				   						    for y in x]))))

	# Create adj matrix
	adj = np.zeros((len(char_list), len(char_list)))
	for i in range(len(char_list)):
		for j in range(len(char_list)):
			adj[i, j] = weights[(char_list[i], char_list[j])] > 0

	# Filter those chars without many dialogs
	total_dlgs = np.sum(adj, axis = 1)
	idx = np.array(np.where(total_dlgs > threshold)[0])
	adj = adj[idx, :][:, idx]
	char_list = char_list[idx]

	# Make it binary
	adj = (adj > 0).astype(int)

	return (movie_name, char_list, adj)

def readGenders(filename):
	genders = defaultdict(lambda: 'unknown')
	with open(filename) as inpt:
		for line in inpt:
			if "=>" in line:
				CNAME, info = line.strip().split("=>")
				try:
					cid, char_name, actor_name, _, gender, _ = info.split(" | ")
				except:
					cid, gender, _ = info.split(" | ")

				genders[CNAME] = gender
	return genders

############################################################
# Override is a filename with a mapping from k -> k'
# Overwriting the keys of the dict
# So that it coincides with movies titles 
############################################################
def readGenre(filename, override = None, remove_punct = True):
	mat = loadmat(filename)

	if override:
		with open(override) as inpt:
			over = eval(inpt.read())
	else:
		over = {}

	def aux(key):
		newk = re.sub('\s+', ' ', key.translate(punct_elim).strip())
		return over.get(newk, newk)

	return walk_keys(aux, mat)

def createGraph(char_list, adj, genders):
	G = nx.from_numpy_matrix(adj)
	node_gender = {i:genders[x] for i, x in enumerate(char_list)}
	nx.set_node_attributes(G, 'gender', node_gender)
	
	return G

def functionals(arr):
	return (np.min(arr), np.mean(arr), np.median(arr), np.max(arr))