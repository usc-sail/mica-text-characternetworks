#!/usr/bin/python

import os

fileList = os.listdir('.')

for file in fileList:
    if file.endswith('_xml.txt'):
        inPtr = open(file, 'r')

        _ = inPtr.readline()

        tmpLine = inPtr.readline()

        tmpList = tmpLine.strip().split(': ')

        print file + ': ' + ': '.join(tmpList[1:])

        inPtr.close()

