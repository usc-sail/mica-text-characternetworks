from xml.dom import minidom
import sys,json, re
from collections import defaultdict 
import numpy as np
import networkx as nx

def read(filename, threshold = 2):
    spkTransition=defaultdict(lambda:defaultdict(int))


    tree=minidom.parse(filename)
    mov=tree.getElementsByTagName('movie')[0]

    # movietitle=mov.getAttribute('title')
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

    char_list=np.array(sorted(list(spkTransition.keys()))) #Python 3
    N=len(char_list)
    adj=np.zeros((N,N))

    for i, ch1 in enumerate(char_list):
        for j, ch2 in enumerate(char_list):
            if ch2 in spkTransition[ch1]:
                adj[i][j] = spkTransition[ch1][ch2]

    # Make it symmetric
    adj = (adj.transpose() + adj) / 2.0


    # Filter those without many dialogs
    total_dlgs = np.sum(adj, axis = 1)
    idx = np.array(np.where(total_dlgs > threshold)[0])
    adj = adj[idx, :][:, idx]
    char_list = char_list[idx]

    # Make it binary
    adj = (adj > 0).astype(int)

    return (char_list, adj)

def genders(filename):
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

def createGraph(char_list, adj, genders):
    G = nx.from_numpy_matrix(adj)
    node_gender = {i:genders[x] for i, x in enumerate(char_list)}
    nx.set_node_attributes(G, 'gender', node_gender)
    
    return G

def functionals(arr):
    return (np.min(arr), np.mean(arr), np.median(arr), np.max(arr))