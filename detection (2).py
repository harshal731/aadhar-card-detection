# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 21:20:50 2020

@author: 91998
"""


import os
import os.path
import json
import sys
import pytesseract
import re
import csv
import dateutil.parser as dparser
from PIL import Image


img = Image.open(r'C:\Users\91998\Desktop\ClassX\Capture.png')
img = img.convert('RGBA')
pix = img.load()

for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
            pix[x, y] = (0, 0, 0, 255)
        else:
            pix[x, y] = (255, 255, 255, 255)

img.save('temp.png')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(Image.open('Capture.png'))

# Initializing data variable
name = None
gender = None
ayear = None
vid = None
yearline = []
genline = []
nameline = []
text1 = []
text2 = []
genderStr = '(Female|Male|emale|male|ale|FEMALE|MALE|EMALE)$'


# Searching for Year of Birth
lines = text
# print (lines)
for wordlist in lines.split('\n'):
    xx = wordlist.split()
    if [w for w in xx if re.search('(DOB:)$', w)]:
        
        break
   # else:
      #  text1.append(wordlist)
try:
    text2 = text.split(yearline, 1)[1]
except Exception:
    pass

try:
    yearline = re.split('DOB:', yearline)[1:]
    yearline = ''.join(str(e) for e in yearline)
    if yearline:
        ayear = dparser.parse(yearline, fuzzy=True).year
except Exception:
    pass

# Searching for Gender
try:
    for wordlist in lines.split('\n'):
        xx = wordlist.split()
        if [w for w in xx if re.search(genderStr, w)]:
            genline = wordlist
            break

    if 'Female' in genline or 'FEMALE' in genline:
        gender = "Female"
    if 'Male' in genline or 'MALE' in genline:
        gender = "Male"

    text2 = text.split(genline, 1)[1]
except Exception:
    pass

# Read Database

with open('namedb1.csv', 'r') as f:
    reader = csv.reader(f)
    newlist = list(reader)
newlist = sum(newlist, [])

# Searching for Name and finding exact name in database
try:
    text1 = filter(None, text1)
    for x in text1:
        for y in x.split():
            if y.upper() in newlist:
                nameline.append(x)
                break
    name = ' '.join(str(e) for e in nameline)
except Exception:
    pass

'''
# Searching for UID
vid = set()
try:
    newlist = []
    for xx in text2.split('\n'):
        newlist.append(xx)
    newlist = list(filter(lambda x: len(x) > 12, newlist))
    for no in newlist:
        print(no)
        if re.match("^[VID : 0-9 ]+$", no):
            vid.add(no)

except Exception:
    pass

#Making tuples of data
data = {}
#data['Name'] = name
data['Gender'] = gender
data['Birth year'] = ayear

if len(list(vid)) > 1:
    data['vid'] = list(vid)[0]
else:
    data['vid'] = None

print(data)










# Writing data into JSON
fName = '../result/' + os.path.basename(sys.argv[1]).split('.')[0] + '.json'
with open(fName, 'w') as fp:
    json.dump(data, fp)

# Removing dummy files
os.remove('temp.png')

# Reading data back JSON
with open(fName, 'r') as f:
    ndata = json.load(f)

print("+++++++++++++++++++++++++++++++")
print(ndata['Name'])
print("-------------------------------")
print(ndata['Gender'])
print("-------------------------------")
print(ndata['Birth year'])
print("-------------------------------")
print(ndata['Uid'])
print("-------------------------------")