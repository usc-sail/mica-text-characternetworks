#!/usr/bin/python

import sys,json,os
import numpy as np
import re
from xml.dom import minidom
from collections import defaultdict 
from scipy.sparse.csgraph import minimum_spanning_tree
from itertools import combinations

def contains_male_reference(cur_utterance):
    tokens = alphanum.sub(' ', cur_utterance).lower().split()    
    for tok in tokens:
        if tok in malenouns:
            return True

    return False

def clean_speaker(speaker):
#    speaker=re.sub(' ','_',speaker)
    speaker=re.sub('[^_A-Za-z\. ]','',speaker)

    return speaker

speakerInfoDir = '../../GenderBias_usingText/Data/movies_deliverable/intermediate/speakersWithCharacterInfo/Corrected_Gender_Assignments/'
malenounsfile = '../Data/male_nouns.txt'
with open(malenounsfile) as inptr:
    malenouns=[x.strip() for x in inptr.readlines()]

alphanum = re.compile(r'[^a-zA-Z0-9_ ]+')

th=1
filename=sys.argv[1]
filepath=os.path.join(speakerInfoDir, filename.split('/')[-1].replace('.','_')+'.txt')
if not os.path.exists(filepath):
    filepath = filepath.replace('Corrected_Gender_Assignments/', '')

speakerFilePtr = open(filepath, 'r')

_ = speakerFilePtr.readline()
_ = speakerFilePtr.readline()
_ = speakerFilePtr.readline()
_ = speakerFilePtr.readline()
_ = speakerFilePtr.readline()
_ = speakerFilePtr.readline()

speakerInfo = defaultdict(lambda:'unknown')

for currentLine in speakerFilePtr.readlines():
    currentLine = currentLine.strip()
    tmpList = currentLine.split('=>')
    speakerName = clean_speaker(tmpList[0].strip())
    tmpList2 = tmpList[1].strip().split('|')
    numUtterances = int(tmpList2[0].strip())
    gender = tmpList2[-2].strip()
    genderConfidence = float(tmpList2[-1].strip())

    if speakerName not in speakerInfo.keys():
        speakerInfo[speakerName] = [numUtterances, gender, genderConfidence]

#dlgs_by_speaker=defaultdict(list)
spkTransition=defaultdict(lambda:defaultdict(lambda:[0, []]))

tree=minidom.parse(filename)
mov=tree.getElementsByTagName('movie')[0]

movietitle=mov.getAttribute('title')
dlgs=mov.getElementsByTagName('dialogue')

for d in dlgs:
    cur_diagid=int(d.getAttribute('id'))
    lastSpeaker=''
    utts=[utt.firstChild.data for utt in d.getElementsByTagName('utterance') if utt.firstChild != None]
    utts.extend([context.firstChild.data for context in d.getElementsByTagName('context') if context.firstChild != None])
    spkrs=d.getElementsByTagName('speaker')
   
    charGenders = [speakerInfo[clean_speaker(char.firstChild.wholeText)][1] for char in spkrs if char.firstChild != None]
 
    for s in spkrs:
        if s.firstChild:
            #dlgs_by_speaker[s.firstChild.data].append(u.firstChild.data)
            thisSpeaker=s.firstChild.data

            if len(thisSpeaker.split())>2:
                continue

            if len(lastSpeaker)>0:
                lastSpeaker=clean_speaker(lastSpeaker)
                thisSpeaker=clean_speaker(thisSpeaker)
                spkTransition[lastSpeaker][thisSpeaker][0]+=1
                spkTransition[thisSpeaker][lastSpeaker][0]+=1

                if 'male' not in charGenders and 'unknown' not in charGenders:
                    spkTransition[lastSpeaker][thisSpeaker][1].append((utts, cur_diagid))
                    spkTransition[thisSpeaker][lastSpeaker][1].append((utts, cur_diagid))

            lastSpeaker=thisSpeaker


for sp1 in spkTransition:
    for sp2 in spkTransition[sp1]:
        #make the graph more symmetric
        if sp1<sp2:
            spkTransition[sp1][sp2][0]+=spkTransition[sp2][sp1][0]
            spkTransition[sp2][sp1][0]=spkTransition[sp1][sp2][0]/2
            spkTransition[sp1][sp2][0]=spkTransition[sp1][sp2][0]/2


#Print movie characters sorted by transition probabilities
#for sp1 in spkTransition:
#    if len(sp1)==0:
#        continue
#    print sp1,':',
#    sorted_sp=sorted(spkTransition[sp1].keys(), key = lambda a: spkTransition[sp1][a],reverse=True)
#    for sp2 in sorted_sp:
#        print sp2,spkTransition[sp1][sp2],
#    print

#char_list=np.array(spkTransition.keys())
char_list=np.array(list(set(spkTransition.keys()).intersection(set(speakerInfo.keys()))))
char_list=np.array([char for char in char_list if char != ''])

N=len(char_list)
adj=np.zeros((N,N))

for i,ch1 in enumerate(char_list):
    for j,ch2 in enumerate(char_list):
        adj[i][j]=-spkTransition[ch1][ch2][0]


#Filter the graph for characters who have very few dialogs
adj[range(len(char_list)), range(len(char_list))]=0
total_dlgs=np.sum(-adj,axis=1)
idx=np.array(np.where(total_dlgs>=th)[0])
adj=adj[idx,:]
adj=adj[:,idx]
char_list=char_list[idx]
#char_list=list(set(char_list).intersection(set(speakerInfo.keys())))
num_chars = len(char_list)

connection_matrix=np.zeros(adj.shape)
connection_matrix[np.where(adj<0)]=1
degrees_list=np.sum(connection_matrix,axis=1)
top_five_chars=[char_list[id] for id in np.argsort(-degrees_list)[:5]]

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

maleChars = [char for char in char_list if speakerInfo[char][1] == 'male']
femaleChars = [char for char in char_list if speakerInfo[char][1] == 'female' \
    and speakerInfo[char][0] > 2 and speakerInfo[char][2] > 0.25]

bechdel_pair=''

for charpair in combinations(femaleChars,2):
    for utterancesList in spkTransition[charpair[0]][charpair[1]][1]:
        cur_utterance = '. '.join(utterancesList[0])
        if not contains_male_reference(cur_utterance):
            bechdel_pair=(charpair,utterancesList[1])
            break
    if bechdel_pair!='':
        break

char_nodes_list = []
edge_nodes_list = []

counter=1
for char in char_list:
    if bechdel_pair != '' and char in bechdel_pair[0]:
        bechdel_node=1
    else:
        bechdel_node=0
    char_nodes_list.append({"name": char, "sno": counter, "count": speakerInfo[char][0], "gender": speakerInfo[char][1], "bechdel": bechdel_node})
    counter = counter + 1

counter=1
for char_pair in zip(list(np.where(connection_matrix==1)[0]), list(np.where(connection_matrix==1)[1])):
    num_mutual_dialogs=-adj[char_pair[0], char_pair[1]]
    if True:
        if num_mutual_dialogs<1:
            if set(bechdel_pair) != set(char_pair):
                continue

    edge_nodes_list.append({"source": char_pair[0], "target": char_pair[1], "strength": num_mutual_dialogs});

print (json.dumps({"nodes": char_nodes_list, "edges": edge_nodes_list}))
