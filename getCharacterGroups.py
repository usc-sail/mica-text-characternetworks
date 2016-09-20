from xml.dom import minidom
import sys,json
from collections import defaultdict 
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
import re

th=2
filename=sys.argv[1]
#dlgs_by_speaker=defaultdict(list)
spkTransition=defaultdict(lambda:defaultdict(int))


tree=minidom.parse(filename)
mov=tree.getElementsByTagName('movie')[0]

movietitle=mov.getAttribute('title')
dlgs=mov.getElementsByTagName('dialogue')
lastSpeaker=''

for d in dlgs:
	utts=d.getElementsByTagName('utterance')
	spkrs=d.getElementsByTagName('speaker')
	
	for s in spkrs:
		if s.firstChild:
			#dlgs_by_speaker[s.firstChild.data].append(u.firstChild.data)
			thisSpeaker=s.firstChild.data

			if len(thisSpeaker.split())>2:
				continue

			if len(lastSpeaker)>0:
				lastSpeaker=re.sub(' ','_',lastSpeaker)
				thisSpeaker=re.sub(' ','_',thisSpeaker)
				lastSpeaker=re.sub('[^_A-Za-z]','',lastSpeaker)
				thisSpeaker=re.sub('[^_A-Za-z]','',thisSpeaker)
				spkTransition[lastSpeaker][thisSpeaker]+=1

			lastSpeaker=thisSpeaker


for sp1 in spkTransition:
	for sp2 in spkTransition[sp1]:
		#make the graph more symmetric
		if sp1<sp2:
			spkTransition[sp1][sp2]+=spkTransition[sp2][sp1]
			spkTransition[sp2][sp1]=spkTransition[sp1][sp2]/2
			spkTransition[sp1][sp2]=spkTransition[sp1][sp2]/2


#Print movie characters sorted by transition probabilities
#for sp1 in spkTransition:
#	if len(sp1)==0:
#		continue
#	print sp1,':',
#	sorted_sp=sorted(spkTransition[sp1].keys(), key = lambda a: spkTransition[sp1][a],reverse=True)
#	for sp2 in sorted_sp:
#		print sp2,spkTransition[sp1][sp2],
#	print

char_list=np.array(sorted(list(spkTransition.keys()))) #Python 3
N=len(char_list)
adj=np.zeros((N,N))

for i,ch1 in enumerate(char_list):
	for j,ch2 in enumerate(char_list):
		adj[i][j]=-spkTransition[ch1][ch2]


#Filter the graph for characters who have very few dialogs
total_dlgs=np.sum(-adj,axis=1)
idx=np.array(np.where(total_dlgs>th)[0])
adj=adj[idx,:]
adj=adj[:,idx]
char_list=char_list[idx]

#Find a minimum spanning tree
skel=minimum_spanning_tree(adj)
col=skel.indices
data=skel.data

rows=np.zeros(col.shape).astype('int')
for k in skel.indptr:
	if k>=len(col):
		break
	rows[k]+=1
rows=np.cumsum(rows)
rows=rows-1


print "graph{"
k=0
for i,j in zip(rows,col):
	print char_list[i],"--",char_list[j],'[weight=%d] ;' %(-data[k])
	k+=1
print "}"
