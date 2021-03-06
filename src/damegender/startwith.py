#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez (davidam@gmail.com)
# This file is part of Damegender.

#  Author: David Arroyo Menéndez <davidam@gmail.com>
#  Maintainer: David Arroyo Menéndez <davidam@gmail.com>
#  This file is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3, or (at your option)
#  any later version.
#
#  This file is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with damegender; see the file GPL.txt.  If not, write to
#  the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301 USA,

from app.dame_gender import Gender
from app.dame_utils import DameUtils
import sys
import os
import re
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("chars", help="display the gender")
#parser.add_argument('--ml', choices=['nltk', 'svc', 'sgd', 'gaussianNB', 'multinomialNB', 'bernoulliNB', 'forest', 'tree', 'mlp'])
parser.add_argument('--total', default="us", choices=['at', 'au', 'be', 'ca', 'de', 'es', 'fi', 'ie', 'ine', 'is', 'nz', 'mx', 'pt', 'si', 'uy', 'uk', 'us'])
parser.add_argument('--gender', default="female", choices=['male', 'female'])
parser.add_argument('--surname', default=False, action="store_true")
parser.add_argument('--version', action='version', version='0.3')
args = parser.parse_args()

g = Gender()

print(args.surname)
if (args.surname):
    if ((args.total == "es") or (args.total == "us")):
        print(args.total)
else:
    du = DameUtils()
    dicc = du.dicc_dataset(args.gender)

    path = dicc[args.total]

with open(path) as csvfile:
    sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in sexreader:
#        print(row[0].upper())
        regex = "^" + args.chars.upper()
        match = re.search(regex, row[0].upper())
        if match:
            print(row[0])
