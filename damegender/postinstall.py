#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2018  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Damegender; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from app.dame_gender import Gender
from app.dame_sexmachine import DameSexmachine
from app.dame_utils import DameUtils
import csv
from pprint import pprint
import re


g = Gender()

print("You don't need execute this script in normal conditions. We are going to create some data files, in normal conditions you've downloaded these files cloning the repository. But perhaps you need regenerate these files.")

yesornot = input("Do you want continue? (Yes/Not) ")

#print(yesornot)

if ((yesornot == "Yes") | (yesornot == "yes") | (yesornot == "Y") | (yesornot == "y")):
    print("We are creating files/names/nam_dict_list.txt")
    g.namdict2file()
    print("We are creating .sav files data models in files/datamodels")
    print("This process take a long time, you can rest.")
    s = DameSexmachine()
    s.gaussianNB()
    s.svc()
    s.sgd()
    s.multinomialNB()
    s.bernoulliNB()
    print("This process has finished. You have the models in files/datamodels/*.sav")

    du = DameUtils()

    print("Creating the file files/names/allnoundefined.csv from files/names/all.csv")
    with open('files/names/all.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        filenou = open('files/names/allnoundefined.csv','w+')
        for row in reader:
            g = du.drop_quotes(row[4])
            if ((g == "m") | (g == "f")):
                filenou.write(row[0]+','+row[1]+','+row[2]+','+row[3]+','+row[4]+','+row[5]+'\n')
        filenou.close()
