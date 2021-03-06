#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez (davidam@gmail.com)
# This file is part of Damegender.

# You can share, copy and modify this software if you are a woman or you
# are David Arroyo Menéndez and you include this note.


from __future__ import print_function
from operator import itemgetter, attrgetter
from app.dame_gender import Gender
from app.dame_utils import DameUtils

import sys
import os
import re
import argparse
import csv
import subprocess, tempfile


parser = argparse.ArgumentParser()
parser.add_argument("country", default="usa", choices=['at', 'au', 'be', 'ca', 'dk', 'de', 'es', 'fi', 'gb', 'ie', 'ine', 'inter', 'is', 'nz', 'mx', 'pt', 'si', 'uy', 'uk', 'us', 'usa'], help="Countries with 2 letter, example, es is Spain")
# More about iso codes on https://www.iso.org/obp/ui/
parser.add_argument('--number', default=10)
parser.add_argument('--sex', default="female", choices=["male", "female", "all"])
parser.add_argument('--reverse', default=False, action="store_true")
parser.add_argument('--less', default=False, action="store_true")
parser.add_argument('--position', default=False, action="store_true")
parser.add_argument('--version', action='version', version='0.3')
args = parser.parse_args()

results = []

g = Gender()
du = DameUtils()

# PAGINATION STUFF

#page = True  # For tests

# Definition of a printc() function that prints to the correct output
if args.less:
    tmp_file = open(tempfile.mkstemp()[1], 'w')  # No need to store the name in a specific variable
    def printc(*largs, **kwargs):
        if 'file' not in kwargs:  # The code can still use the usual file argument of print()
            kwargs['file'] = tmp_file  # Forces the output to go to the temp file
        print(*largs, **kwargs)
else:
    printc = print  # Regular print




# MALES
def c2l(csvpath):
    l = []
    with open(csvpath) as csvfile:
        sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in sexreader:
            l.append([row[0], int(row[1])])
    return l

#c2l = c2l("files/names/names_au/baby-names-1944-2013/aumales.csv")

def getKey0str(item):
    return item[0]

def getKey1(item):
    return int(item[1])

du = DameUtils()
dicc_dataset_males = du.dicc_dataset("male")

if (args.country == "at"):
    c2lmales = du.csv2list(dicc_dataset_males["au"])
elif (args.country == "au"):
    c2lmales = du.csv2list(dicc_dataset_males["au"])
elif (args.country == "be"):
    c2lmales = du.csv2list(dicc_dataset_males["be"])
elif (args.country == "ca"):
    c2lmales = du.csv2list(dicc_dataset_males["ca"])
elif (args.country == "dk"):
    c2lmales = du.csv2list(dicc_dataset_males["dk"])
elif ((args.country == "es") | (args.country == "ine")):
    c2lmales = du.csv2list(dicc_dataset_males["es"])
elif (args.country == "fi"):
    c2lmales = du.csv2list(dicc_dataset_males["fi"])
elif (args.country == "ie"):
    c2lmales = du.csv2list(dicc_dataset_males["ie"])
elif (args.country == "inter"):
    c2lmales = du.csv2list(dicc_dataset_males["inter"])
elif (args.country == "is"):
    c2lmales = du.csv2list(dicc_dataset_males["is"])
elif (args.country == "nz"):
    c2lmales = du.csv2list(dicc_dataset_males["nz"])
elif (args.country == "mx"):
    c2lmales = du.csv2list(dicc_dataset_males["mx"])
elif (args.country == "pt"):
    c2lmales = du.csv2list(dicc_dataset_males["pt"])
elif (args.country == "si"):
    c2lmales = du.csv2list(dicc_dataset_males["si"])
elif (args.country == "uy"):
    c2lmales = du.csv2list(dicc_dataset_males["uy"])
elif ((args.country == "uk") or (args.country == "gb")):
    c2lmales = du.csv2list(dicc_dataset_males["gb"])
elif ((args.country == "usa") | (args.country == "us")):
    c2lmales = du.csv2list(dicc_dataset_males["us"])

if (args.reverse):
    c2lmales = sorted(c2lmales, key=getKey1)
else:
    c2lmales = sorted(c2lmales, key=getKey1, reverse=True)

# FEMALES

dicc_dataset_females = du.dicc_dataset("female")

if (args.country == "at"):
    c2lfemales = du.csv2list(dicc_dataset_females["at"])
elif (args.country == "au"):
    c2lfemales = du.csv2list(dicc_dataset_females["au"])
elif (args.country == "be"):
    c2lfemales = du.csv2list(dicc_dataset_females["be"])
elif (args.country == "ca"):
    c2lfemales = du.csv2list(dicc_dataset_females["ca"])
elif (args.country == "dk"):
    c2lfemales = du.csv2list(dicc_dataset_females["dk"])
elif ((args.country == "es") | (args.country == "ine")):
    c2lfemales = du.csv2list(dicc_dataset_females["es"])
elif (args.country == "fi"):
    c2lfemales = du.csv2list(dicc_dataset_females["fi"])
elif ((args.country == "gb") or (args.country == "uk")):
    c2lfemales = du.csv2list(dicc_dataset_females["gb"])
elif (args.country == "ie"):
    c2lfemales = du.csv2list(dicc_dataset_females["ie"])
elif (args.country == "inter"):
    c2lfemales = du.csv2list(dicc_dataset_females["inter"])
elif (args.country == "is"):
    c2lfemales = du.csv2list(dicc_dataset_females["is"])
elif (args.country == "nz"):
    c2lfemales = du.csv2list(dicc_dataset_females["nz"])
elif (args.country == "mx"):
    c2lfemales = du.csv2list(dicc_dataset_females["mx"])
elif (args.country == "pt"):
    c2lfemales = du.csv2list(dicc_dataset_females["pt"])
elif (args.country == "si"):
    c2lfemales = du.csv2list(dicc_dataset_females["si"])
elif (args.country == "uy"):
    c2lfemales = du.csv2list(dicc_dataset_females["uy"])
elif ((args.country == "usa") | (args.country == "us")):
    c2lfemales = du.csv2list(dicc_dataset_females["us"])

if (args.reverse):
    c2lfemales = sorted(c2lfemales, key=getKey1)
else:
    c2lfemales = sorted(c2lfemales, key=getKey1, reverse=True)

n = int(args.number)

if (args.less and (args.sex=='female')):
    n = len(c2lfemales)
elif (args.less and (args.sex=='male')):
    n = len(c2lmales)
elif (args.less and (args.sex=='all')):
    n = len(c2lmales) + len(c2lfemales)

if (args.sex == "male"):
    position = 1
    for i in c2lmales[0:n]:
        if args.less:
            if args.position:
                printc(str(position) + ") " + i[0] + ": " + i[1], sep='/')
            else:
                printc(i[0] + ": " + i[1], sep='/')
        else:
            if args.position:
                print(str(position) + ") " + i[0] + ": " + i[1])
            else:
                print(i[0] + ": " + i[1])
        position = position + 1

elif (args.sex == "female"):
    position = 1
    for i in c2lfemales[0:n]:
        if args.less:
            if args.position:
                printc(str(position) + ") " + i[0] + ": " + i[1], sep='/')
            else:
                printc(i[0] + ": " + i[1], sep='/')
        else:
            if args.position:
                print(str(position) + ") " + i[0] + ": " + i[1])
            else:
                print(i[0] + ": " + i[1])
        position = position + 1

elif (args.sex == "all"):

    c2l = c2lfemales + c2lmales
    if (args.reverse):
        c2l = sorted(c2l, key=getKey1)
    else:
        c2l = sorted(c2l, key=getKey1, reverse=True)

    position = 1
    for i in c2l[0:n]:
        if args.less:
            if args.position:
                printc(str(position) + ") " + i[0] + ": " + i[1], sep='/')
            else:
                printc(i[0] + ": " + i[1], sep='/')
        else:
            if args.position:
                print(str(position) + ") " + i[0] + ": " + i[1])
            else:
                print(i[0] + ": " + i[1])
        position = position + 1

# Paging of the current contents of the temp file:
if args.less:
    tmp_file.flush()  # No need to close the file: you can keep printing to it
    subprocess.call(['less', tmp_file.name])  # Simpler than a full Popen()
