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
    speakerName = tmpList[0].strip()
    tmpList2 = tmpList[1].strip().split('|')
    numUtterances = int(tmpList2[0].strip())
    gender = tmpList2[-2].strip()
    genderConfidence = float(tmpList2[-1].strip())

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
   
    charGenders = [speakerInfo[char.firstChild.wholeText][1] for char in spkrs if char.firstChild != None]
 
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

answer_pair=''

for charpair in combinations(femaleChars,2):
    for utterancesList in spkTransition[charpair[0]][charpair[1]][1]:
        cur_utterance = '. '.join(utterancesList[0])
        if not contains_male_reference(cur_utterance):
            answer_pair=(charpair,utterancesList[1])
            break
    if answer_pair!='':
        break

if True:
    if answer_pair == '': 
        print "failed"
    else:
        print "passed"
    #    print "For %s, Bechdel test passed! Character pair: (%s, %s) and diagid: %d" % (filename, answer_pair[0][0], answer_pair[0][1], answer_pair[1])
    #print top_five_chars

print "graph{"
for char in char_list:
    if char == '':
        continue
    if char in top_five_chars:
        peripheries=3
    else:
        peripheries=1
    
    fillcolor='white'

    if speakerInfo[char][1] == 'male':
        shape='ellipse'
    elif speakerInfo[char][1] == 'female':
        shape='box'
        if answer_pair != '' and char in answer_pair[0]:
            fillcolor='green'
        else:
            fillcolor='white'
    else:
        shape='none'
        print char + '[shape=none];' 

    print char + '[shape="%s",peripheries=%d,style=filled,fillcolor="%s"];' % (shape,peripheries,fillcolor)

k=0
for i,j in zip(rows,col):
    print char_list[i],"--",char_list[j],'[weight=%d] ;' %(-data[k])
    k+=1
 
#for i in range(num_chars):
#    for j in range(i,num_chars):
#        print char_list[i],"--",char_list[j],'[weight=%d] ;' %(adj[i][k])

print "}"
