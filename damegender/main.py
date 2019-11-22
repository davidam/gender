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

from app.dame_sexmachine import DameSexmachine
import sys
import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name", help="display the gender")
parser.add_argument('--ml', choices=['nltk', 'svc', 'sgd', 'gaussianNB', 'multinomialNB', 'bernoulliNB', 'forest', 'xgboost'])
parser.add_argument('--total', default="ine", choices=['ine', 'genderguesser'])
parser.add_argument('--version', action='version', version='0.1')
args = parser.parse_args()


if (args.total == "genderguesser"):
        name = args.name.capitalize()
        cmd = 'grep -i "' + name + '" files/names/nam_dict.txt > logs/grep.tmp'
        print(cmd)
        os.system(cmd)
        results = [i for i in open('files/grep.tmp', 'r').readlines()]
        for i in results:
            regex = "(M|F|=|\?|1)( |M|F)?( )(" + name + ")"
            r = re.match(regex, i)
            prob = r.group(1) + r.group(2)
            if (('F' == prob) or ('F ' == prob)):
                print("female")
                print("prob: fully female")
            elif (prob == '?F'):
                print("female")
                print("prob: mostly female")
            elif (prob == '1F'):
                print("female")
                print("prob: female name, if first part of name; mostly female name")
            elif (('M' == prob) or ('M ' == prob)):
                print("male")
                print("prob: fully male")
            elif (prob == '?M'):
                print("male")
                print("prob: mostly male")
            elif (prob == '1M'):
                print("male")
                print("prob: male name, if first part of name; mostly male name")
            elif (prob == '? '):
                print("unknow")
                print("you can try predict with --ml")
else:
    s = DameSexmachine()
    num_males = s.name_frec(args.name, dataset=args.total)['males']
    num_females = s.name_frec(args.name, dataset=args.total)['females']
    if (int(num_males) > int(num_females)):
        print("%s's gender is male" % (str(args.name)))
        prob = int(num_males) / (int(num_males) + int(num_females))
        print("probability: %s" % str(prob))
    elif (int(num_males) < int(num_females)):
        print("%s's gender is female" % (str(args.name)))
        prob = int(num_females) / (int(num_females) + int(num_males))
        print("probability: %s" % str(prob))
    elif ((int(num_males) == 0) and (int(num_females) == 0)):
        args.ml = 'nltk'

    if (args.ml):
        if (args.ml == "nltk"):
            guess = s.guess(args.name, binary=True, ml="nltk")
        if (args.ml == "sgd"):
            guess = s.guess(args.name, binary=True, ml="sgd")
        elif (args.ml == "svc"):
            guess = s.guess(args.name, binary=True, ml="svc")
        elif (args.ml == "gaussianNB"):
            guess = s.guess(args.name, binary=True, ml="gaussianNB")
        elif (args.ml == "multinomialNB"):
            guess = s.guess(args.name, binary=True, ml="multinomialNB")
        elif (args.ml == "bernoulliNB"):
            guess = s.guess(args.name, binary=True, ml="bernoulliNB")
        elif (args.ml == "forest"):
            guess = s.guess(args.name, binary=True, ml="forest")
        elif (args.ml == "xgboost"):
            guess = s.guess(args.name, binary=True, ml="xgboost")
        if (guess == 1):
            sex = "male"
        elif (guess == 0):
            sex = "female"
        elif (guess == 2):
            sex = "unknown"
        print("%s gender predicted is %s" % (str(args.name), sex))

    if (args.total == "ine"):
        print("%s males for %s from INE.es" % (num_males, args.name))
        print("%s females for %s from INE.es" % (num_females, args.name))
#
