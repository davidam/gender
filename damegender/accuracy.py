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
from app.dame_namsor import DameNamsor
from app.dame_genderize import DameGenderize
from app.dame_genderguesser import DameGenderGuesser
from app.dame_genderapi import DameGenderApi
from app.dame_nameapi import DameNameapi
from app.dame_customsearch import DameCustomsearch

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--csv', default="files/names/min.csv", help='input file for names')
parser.add_argument('--json', help='if you have downloaded the results from an api in a json file, you can try this argument')
parser.add_argument('--measure', default="accuracy", choices=['accuracy', 'precision', 'recall', 'f1score'])
parser.add_argument('--api', default="damegender", choices=['customsearch', 'namsor', 'genderize', 'genderguesser', 'damegender', 'genderapi', 'nameapi', 'all'])
parser.add_argument('--ml', default="nltk", choices=['nltk', 'svc', 'sgd', 'gaussianNB', 'multinomialNB', 'bernoulliNB', 'forest', 'xgboost'])
args = parser.parse_args()

if (args.api == "all"):
    dg = Gender()

    if (dg.config['DEFAULT']['namsor'] == 'yes'):
        dn = DameNamsor()
        print("################### Namsor!!")
        gl = dn.gender_list(path=args.csv)
        print("Gender list: " + str(gl))
        sl = dn.guess_list(path=args.csv, binary=True)
        print("Guess list:  " +str(sl))
        dg.print_measures(gl, sl, args.measure, "Namsor")

    if (dg.config['DEFAULT']['genderize'] == 'yes'):
        dg = DameGenderize()
        print("################### Genderize!!")
        gl = dg.gender_list(path=args.csv)
        print("Gender list: " + str(gl))
        sl = dg.guess_list(path=args.csv, binary=True)
        print("Guess list:  " +str(gl))
        dg.print_measures(gl, sl, args.measure, "Genderize")

    dgg = DameGenderGuesser()
    print("################### GenderGuesser!!")
    gl = dgg.gender_list(path=args.csv)
    print("Gender list: " + str(gl))
    sl = dgg.guess_list(path=args.csv, binary=True)
    print("Guess list:  " +str(sl))
    dgg.print_measures(gl, sl, args.measure, "GenderGuesser")


    ds = DameSexmachine()
    print("################### Dame Gender!!")
    gl = ds.gender_list(path=args.csv)
    print("Gender list: " + str(gl))
    sl = ds.guess_list(path=args.csv, binary=True)
    print("Guess list:  " +str(sl))
    ds.print_measures(gl, sl, args.measure, "Dame Gender")



    if (dg.config['DEFAULT']['genderapi'] == 'yes'):
        dga = DameGenderApi()
        print("################### GenderApi!!")
        gl = dga.gender_list(path=args.csv)
        print("Gender list: " + str(gl))
        sl = dga.guess_list(path=args.csv, binary=True)
        print("Guess list:  " +str(sl))
        dga.print_measures(gl, sl, args.measure, "Genderapi")

    if (dg.config['DEFAULT']['nameapi'] == 'yes'):
        dna = DameNameapi()
        print("################### Nameapi!!")
        gl = dna.gender_list(path=args.csv)
        print("Gender list: " + str(gl))
        sl = dna.guess_list(path=args.csv, binary=True)
        print("Guess list:  " +str(sl))
        dna.print_measures(gl, sl, args.measure, "Nameapi")

elif (args.api == "namsor"):
    dn = DameNamsor()
    print("################### Namsor!!")
    gl = dn.gender_list(path=args.csv)
    print("Gender list: " + str(gl))
    sl = dn.guess_list(path=args.csv, binary=True)
    print("Guess list:  " +str(sl))
    dn.print_measures(gl, sl, args.measure, "Namsor")


elif (args.api == "genderize"):
    dg = DameGenderize()
    print("################### Genderize!!")
    gl = dg.gender_list(path=args.csv)

    print("Gender list: " + str(gl))
    sl = dg.guess_list(path=args.csv, binary=True)
    print("Guess list:  " +str(gl))
    dg.print_measures(gl, sl, args.measure, "Genderize")

elif (args.api == "genderguesser"):
    dgg = DameGenderGuesser()
    print("################### GenderGuesser!!")
    gl = dgg.gender_list(path=args.csv)
    print("Gender list: " + str(gl))
    sl = dgg.guess_list(path=args.csv, binary=True)
    print("Guess list:  " +str(sl))
    dgg.print_measures(gl, sl, args.measure, "GenderGuesser")


elif (args.api == "customsearch"):
    dc = DameCustomsearch()
    print("################### Google Custom Search!!")
    gl = dc.gender_list(path=args.csv)
    print("Gender list: " + str(gl))
    sl = dc.guess_list(path=args.csv, binary=True)
    print("Guess list:  " +str(sl))
    customsearch_accuracy = dc.accuracy_score_dame(gl,sl)
    print("Google Custom Search: %s" % customsearch_accuracy)


elif (args.api == "damegender"):

    if (args.ml == "nltk"):
        ds = DameSexmachine()
        print("################### NLTK!!")
        gl1 = ds.gender_list(path=args.csv)
        print("Gender list: " + str(gl1))
        gl2 = ds.guess_list(path=args.csv, binary=True)
        print("Guess list:  " +str(gl2))
        ds.print_measures(gl1, gl2, args.measure, "Dame Gender")

    elif (args.ml == "svc"):
        ds = DameSexmachine()
        print("################### Support Vector Machines!!")
        gl1 = ds.gender_list(path=args.csv)
        print("Gender list: " + str(gl1))
        gl2 = ds.guess_list(path=args.csv, binary=True, ml="svc")
        print("Guess list:  " +str(gl2))
        ds.print_measures(gl1, gl2, args.measure, "Dame Gender")


    elif (args.ml == "sgd"):
        ds = DameSexmachine()
        print("################### Stochastic Gradient Descent!!")
        gl1 = ds.gender_list(path=args.csv)
        print("Gender list: " + str(gl1))
        gl2 = ds.guess_list(path=args.csv, binary=True, ml="sgd")
        print("Guess list:  " +str(gl2))
        ds.print_measures(gl1, gl2, args.measure, "Dame Gender")

    elif (args.ml == "gaussianNB"):
        ds = DameSexmachine()
        print("################### Gaussian Naive Bayes!!")
        gl1 = ds.gender_list(path=args.csv)
        print("Gender list: " + str(gl1))
        gl2 = ds.guess_list(path=args.csv, binary=True, ml="gaussianNB")
        print("Guess list:  " +str(gl2))
        ds.print_measures(gl1, gl2, args.measure, "Dame Gender")

    elif (args.ml == "multinomialNB"):
        ds = DameSexmachine()
        print("################### Multinomial Naive Bayes!!")
        gl1 = ds.gender_list(path=args.csv)
        print("Gender list: " + str(gl1))
        gl2 = ds.guess_list(path=args.csv, binary=True, ml="multinomialNB")
        print("Guess list:  " +str(gl2))
        ds.print_measures(gl1, gl2, args.measure, "Dame Gender")

    elif (args.ml == "bernoulliNB"):
        ds = DameSexmachine()
        print("################### Bernoulli Naive Bayes!!")
        gl1 = ds.gender_list(path=args.csv)
        print("Gender list: " + str(gl1))
        gl2 = ds.guess_list(path=args.csv, binary=True, ml="bernoulliNB")
        print("Guess list:  " +str(gl2))
        ds.print_measures(gl1, gl2, args.measure, "Dame Gender")

    elif (args.ml == "forest"):
        ds = DameSexmachine()
        print("################### Random Forest!!")
        gl1 = ds.gender_list(path=args.csv)
        print("Gender list: " + str(gl1))
        gl2 = ds.guess_list(path=args.csv, binary=True, ml="forest")
        print("Guess list:  " +str(gl2))
        ds.print_measures(gl1, gl2, args.measure, "Dame Gender")

    elif (args.ml == "xgboost"):
        ds = DameSexmachine()
        print("################### Xgboost!!")
        gl1 = ds.gender_list(path=args.csv)
        print("Gender list: " + str(gl1))
        gl2 = ds.guess_list(path=args.csv, binary=True, ml="xgboost")
        print("Guess list:  " +str(gl2))
        ds.print_measures(gl1, gl2, args.measure, "Dame Gender")


elif (args.api == "genderapi"):
    dga = DameGenderApi()
    print("################### GenderApi!!")
    gl = dga.gender_list(path=args.csv)
    print("Gender list: " + str(gl))
    if (args.json is None):
        sl = dga.guess_list(path=args.csv, binary=True)
    else:
        sl = dga.json2guess_list(jsonf=args.json, binary=True)
    print("Guess list:  " +str(sl))
    dga.print_measures(gl, sl, args.measure, "Genderapi")


elif (args.api == "nameapi"):
    dna = DameNameapi()
    print("################### Nameapi!!")
    gl = dna.gender_list(path=args.csv)
    print("Gender list: " + str(gl))
    sl = dna.guess_list(path=args.csv, binary=True)
    print("Guess list:  " +str(sl))
    dna.print_measures(gl, sl, args.measure, "Nameapi")
