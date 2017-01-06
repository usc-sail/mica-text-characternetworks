import untangle
import sys,json, re
from collections import defaultdict, Counter
import numpy as np
import networkx as nx
import scipy.io 
from funcy import walk_keys 
import string
# from matfile_utils import loadmat
import logging

logging.basicConfig(level = logging.DEBUG)

punct_elim = str.maketrans({key:' ' for key in string.punctuation})

def read(filename, threshold = 2):
	
	with open(filename) as inpt:

		transitions = []
		cur_spkr = ""
		
		for idx, line in enumerate(inpt):
			try:
				char, utt = line.strip().split(" => ")
				
				if char != cur_spkr:
					transitions.append((cur_spkr, char))
					cur_spkr = char 	

			except:
				pass
				# logging.warn("Line:{} in file:{} cannot be read".format(idx, filename) )

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

	return ("", char_list, adj)

def readGenders(filename):
	genders = defaultdict(lambda: 'unknown')
	races = defaultdict(lambda: 'unknown')

	with open(filename) as inpt:

		gender, race = "", ""

		for line in inpt:
			if "=> " in line:
				char, info = line.strip().split("=> ")
				if "|" in info:
					arr_info = info.split("|")
					if len(arr_info) == 3:
						_, gender, _ = arr_info
					elif len(arr_info) == 7:
						_, _, _, _, gender, _, race = arr_info
					else:
						raise Exception('unknown split number')

				gender = gender.strip()
				race = race.strip()

				if len(race) > 0:
					races[char] = race

				genders[char] = gender

	return (genders, races)

############################################################
#
#
#
############################################################
def readGenre(filename):
	genres = []
	with open(filename) as inpt:
		for line in inpt:
			if "Genre: " in line:
				genres = line.strip().split("Genre: ")[1].split(" | ")
				break 

	return genres 


def createGraph(char_list, adj, genders, races = defaultdict(lambda x: None)):
	G = nx.from_numpy_matrix(adj)
	
	node_gender = {i:genders[x] for i, x in enumerate(char_list)}
	node_races = {i:races[x] for i, x in enumerate(char_list)}

	nx.set_node_attributes(G, 'gender', node_gender)
	nx.set_node_attributes(G, 'race', node_races)

	return G

def functionals(arr):
	return (np.min(arr), np.mean(arr), np.median(arr), np.max(arr))