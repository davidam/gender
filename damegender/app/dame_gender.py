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

from nltk.corpus import names
import nltk
import csv
import unidecode
import unicodedata
import numpy as np
import configparser
import os
import re
import sys
import json
from collections import OrderedDict
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
from damegender.app.dame_utils import DameUtils


csv.field_size_limit(3000000)


class Gender(object):
    # That's the root class in the heritage,
    # apis classes and sexmachine is a gender
    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read('config.cfg')
        self.males = 0
        self.females = 0
        self.unknown = 0
        self.curr_path = os.path.abspath(os.path.dirname(__file__))

    def in_dict(self, name):
        f = os.popen('dict '+name)
        in_dict = False
        for line in f:
            if (re.match(r'[0-9]+ definitions found', line)):
                in_dict = True
        return in_dict

# FEATURES METHODS #

    def features(self, name):
        # features method created to check the nltk classifier
        features = {}
        features["first_letter"] = name[0].lower()
        features["last_letter"] = name[-1].lower()
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features["count({})".format(letter)] = name.lower().count(letter)
            features["has({})".format(letter)] = (letter in name.lower())
        return features

    def features_int(self, name):
        # features method created to check the scikit classifiers
        features_int = {}
        features_int["first_letter"] = ord(name[0].lower())
        features_int["last_letter"] = ord(name[-1].lower())
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            num = name.lower().count(letter)
            features_int["count({})".format(letter)] = num
        features_int["vocals"] = 0
        for letter1 in 'aeiou':
            for letter2 in name:
                if (letter1 == letter2):
                    features_int["vocals"] = features_int["vocals"] + 1
        features_int["consonants"] = 0
        for letter1 in 'bcdfghjklmnpqrstvwxyz':
            for letter2 in name:
                if (letter1 == letter2):
                    features_int["consonants"] = features_int["consonants"] + 1
        # FIRST LETTER
        if (name[0].lower() in 'aeiou'):
            features_int["first_letter_vocal"] = 1
        else:
            features_int["first_letter_vocal"] = 0
        if (name[0].lower() in 'bcdfghjklmnpqrstvwxyz'):
            features_int["first_letter_consonant"] = 1
        else:
            features_int["first_letter_consonant"] = 0
        # LAST LETTER
        if (name[-1].lower() in 'aeiou'):
            features_int["last_letter_vocal"] = 1
        else:
            features_int["last_letter_vocal"] = 0
        if (name[-1].lower() in 'bcdfghjklmnpqrstvwxyz'):
            features_int["last_letter_consonant"] = 1
        else:
            features_int["last_letter_consonant"] = 0
        # h = hyphen.Hyphenator('en_US')
        # features_int["syllables"] = len(h.syllables(name))
        if (name[-1].lower() == "a"):
            features_int["last_letter_a"] = 1
        else:
            features_int["last_letter_a"] = 0
        if (name[-1].lower() == "o"):
            features_int["last_letter_o"] = 1
        else:
            features_int["last_letter_o"] = 0
        return features_int

    # DATASETS METHODS #

    def ukfile(self):
        # create a file with name and prob from uk births
        total = 0
        for i in range(1880, 2018):
            # first we acquire the total of births from 1880 to 2017
            dataset = self.curr_path + "/files/names/uk/yob" + str(i) + ".txt"
            with open(dataset) as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                totali = 0
                for row in sexreader:
                    datasetcount = row[2]
                    totali = totali + int(datasetcount)
            total = total + totali

        # now we are going to start the json file with 1880
        jsonuk = self.curr_path + "/files/names/uk/jsonuk.json"
        file = open(jsonuk, "w")
        dataset = self.curr_path + "/files/names/uk/yob1880.txt"
        with open(dataset) as csvfile:
            sexreader1 = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader1, None)
            cnt = 0
            for row in sexreader1:
                cnt = cnt + 1
        end = cnt
        lines = []
        lines.append('[')
        with open(dataset) as csvfile:
            sexreader2 = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader2, None)
            cnt = 1
            print(cnt)
            print(end)
            for row in sexreader2:
                lines.append('{"name": "' + row[0] + '",')
                lines.append('"gender": "' + row[1] + '",')
                print(end)
                print(cnt)
                if (end == cnt):
                    lines.append('"count": ' + row[2] + '}')
                    print('"count": ' + row[2] + '}')
                else:
                    lines.append('"count": ' + row[2] + '},')
                    print('"count": ' + row[2] + '},')
                cnt = cnt + 1
            lines.append(']')
        fo = open(jsonuk, "w")
        fo.writelines(lines)
        # Cerramos el archivo
        for i in range(1881, 2018):
            dataset = self.curr_path + "/files/names/uk/yob" + str(i) + ".txt"
            with open(dataset) as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                lines = []
                for row in sexreader:
                    print(row)
                #         Cerramos el archivo
        fo.close()
        return 1

    def males_list(self, corpus='engspa'):
        path = self.curr_path + '/files/names/names_es'
        my_corpus = nltk.corpus.PlaintextCorpusReader(path, '.*\.txt')
        if (corpus == 'eng'):
            m = names.words('male.txt')
        elif (corpus == 'spa'):
            m = my_corpus.sents('masculinos.txt')[1]
        elif (corpus == 'engspa'):
            m = names.words('male.txt') + my_corpus.sents('masculinos.txt')[1]
        m = list(OrderedDict.fromkeys(m))
        return m

    def females_list(self, corpus='engspa'):
        path = self.curr_path + '/files/names/names_es'
        my_corpus = nltk.corpus.PlaintextCorpusReader(path, '.*\.txt')
        if (corpus == 'eng'):
            f = names.words('female.txt')
        elif (corpus == 'spa'):
            f = my_corpus.sents('femeninos.txt')[1]
        elif (corpus == 'engspa'):
            f = names.words('female.txt') + my_corpus.sents('femeninos.txt')[1]
        f = list(OrderedDict.fromkeys(f))
        return f

    def csv2names(self, path='files/names/partial.csv'):
        # make a list from a csv file
        csvlist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                csvlist.append(name)
        return csvlist

    def name2gender_in_dataset(self, name, dataset=''):
        guess = 2
        if (dataset == "names_es"):
            with open(dataset+"/"+"femeninos.txt") as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row.title()
                    if (datasetname == name):
                        guess = 0
            with open(dataset+"/"+"masculinos.txt") as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row.title()
                    if (datasetname == name):
                        guess = 1
        if (dataset == "files/names/nam_dict.txt"):
            cmd = 'grep -i "' + name
            cmd = cmd + ' " files/names/nam_dict.txt > files/grep.tmp'
            os.system(cmd)
            results = [i for i in open('files/grep.tmp', 'r').readlines()]
            for row in results:
                datasetname = row[1].title()
                if (datasetname == name):
                    guess = row[0].title()
                    if ((guess == 'F') | (guess == '?F')):
                        guess = 0
                    elif ((guess == 'M') | (guess == '?M')):
                        guess = 1
                    elif (guess == '='):
                        guess = 2
        if (dataset == "files/names/all.csv"):
            with open(dataset) as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row[0].title()
                    if (datasetname == name):
                        guess = row[4]
                        if (guess == 'm'):
                            guess = 1
                        elif (guess == 'f'):
                            guess = 0
                        elif (guess == 'u'):
                            guess = 2
        if (dataset == "files/names/yob2017.txt"):
            with open(dataset) as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row[0].title()
                    if (datasetname == name):
                        guess = row[1]
                        if (guess == 'M'):
                            guess = 1
                        elif (guess == 'F'):
                            guess = 0
        return guess

    def dataset2genderlist(self, dataset=''):
        genderlist = []
        path_all = "files/names/all.csv"
        path_allnoun = "files/names/allnoundefined.csv"
        if ((dataset == path_all) or (dataset == path_allnoun)):
            with open(dataset) as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row[0].title()
                    guess = row[4]
                    guess = guess.replace('\"', '')
                    if (guess == 'm'):
                        guess = 1
                    elif (guess == 'f'):
                        guess = 0
                    elif (guess == 'u'):
                        guess = 2
                    genderlist.append(guess)
        if (dataset == "files/names/yob2017.txt"):
            with open(dataset) as csvfile:
                sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(sexreader, None)
                for row in sexreader:
                    datasetname = row[0].title()
                    guess = row[1]
                    guess = guess.replace('\"', '')
                    if (guess == 'M'):
                        guess = 1
                    elif (guess == 'F'):
                        guess = 0
                    genderlist.append(guess)
        return genderlist

    def name_frec(self, name, dataset='ine'):
        if (dataset == 'ine'):
            du = DameUtils()
            name = du.drop_accents(name)
            path_males = 'files/names/names_es/masculinos_original.csv'
            file_males = open(path_males, 'r')
            readerm = csv.reader(file_males, delimiter=',', quotechar='|')
            males = 0
            for row in readerm:
                if ((len(row) > 1) and (row[1].lower() == name.lower())):
                    males = row[2]
                    males = du.drop_dots(males)
            path_females = 'files/names/names_es/femeninos_original.csv'
            file_females = open(path_females, 'r')
            readerf = csv.reader(file_females, delimiter=',', quotechar='|')
            females = 0
            for row in readerf:
                if ((len(row) > 1) and (row[1].lower() == name.lower())):
                    females = row[2]
                    females = du.drop_dots(females)
            dicc = {"females": females, "males": males}
        elif (dataset == 'uscensus'):
            du = DameUtils()
            usfile = open('files/names/yob2017.txt', 'r')
            usreader = csv.reader(usfile, delimiter=',', quotechar='|')
            males = 0
            females = 0
            for row in usreader:
                if ((len(row) > 1) and (row[0].lower() == name.lower())):
                    if (row[1] == 'F'):
                        females = row[2]
                    elif (row[1] == 'M'):
                        males = row[2]
            dicc = {"females": females, "males": males}
        elif (dataset == 'ukcensus'):
            du = DameUtils()
            name = du.drop_accents(name)
            file_males = open('files/names/2017boysnames-uk.csv', 'r')
            rmales = csv.reader(file_males, delimiter=',', quotechar='|')
            males = 0
            for row in rmales:
                if (len(row) > 1):
                    nowhite = du.drop_white_space(row[1])
                    ukname = du.drop_accents(nowhite).lower()
                    if (ukname == name.lower()):
                        males = row[2]
                        males = du.drop_dots(males)
            file_females = open('files/names/2017girlsnames-uk.csv', 'r')
            rfemales = csv.reader(file_females, delimiter=',', quotechar='|')
            females = 0
            for row in rfemales:
                if (len(row) > 1):
                    nowhite = du.drop_white_space(row[1])
                    ukname = du.drop_accents(nowhite).lower()
                    if (ukname == name.lower()):
                        females = row[2]
                        females = du.drop_dots(females)
            dicc = {"females": females, "males": males}

        return dicc

    def namdict2file(self):
        filepath = 'files/names/nam_dict.txt'
        mylist = []
        with open(filepath) as fp:
            for cnt, line in enumerate(fp):
                # From 3 to 25
                if (cnt > 292):
                    name = ""
                    for i in range(3, 25):
                        name = name + str(line[i])
                    mylist += [name]
        file = open("files/names/nam_dict_list.txt", "w")
        file.writelines(mylist)
        file.close()

    def filenamdict2list(self):
        names = []
        dataset = 'files/names/nam_dict_list.txt'
        with open(dataset, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                names = names + row[0].split()
        return names

# GUESS #

    def guess(self, name, binary=False):
        # guess method to check names dictionary
        guess = ''
        name = unidecode.unidecode(name).title()
        name.replace(name, "")
        m = self.males_list()
        f = self.females_list()
        if (name in m) and (name in f):
            if binary:
                guess = 2
            else:
                guess = 'unknown'
        elif name in m:
            if binary:
                guess = 1
            else:
                guess = 'male'
        elif name in f:
            if binary:
                guess = 0
            else:
                guess = 'female'
        else:
            if binary:
                guess = 2
            else:
                guess = 'unknown'
        return guess

    def guess_list(self, path='files/names/partial.csv', binary=False):
        # guess list method
        slist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                slist.append(self.guess(name, binary))
        return slist

    def gender_list(self, path='files/names/partial.csv'):
        # counting males, females and unknown
        glist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(sexreader, None)
            count_females = 0
            count_males = 0
            count_unknown = 0
            for row in sexreader:
                gender = row[4]
                if (gender == 'f'):
                    g = 0
                    count_females = count_females + 1
                elif (gender == 'm'):
                    g = 1
                    count_males = count_males + 1
                else:
                    g = 2
                    count_unknown = count_unknown + 1
                glist.append(g)
        self.females = count_females
        self.males = count_males
        self.unknown = count_unknown
        return glist

# METHODS ABOUT STATISTICS #

    def count_true2guess(self, truevector, guessvector, true, guess):
        i = 0
        count = 0
        if (len(truevector) >= len(guessvector)):
            maxi = len(guessvector)
        else:
            maxi = len(truevector)
        while (i < maxi):
            if ((truevector[i] == true) and (guessvector[i] == guess)):
                count = count + 1
            i = i + 1
        return count

    def femalefemale(self, truevector, guessvector):
        return self.count_true2guess(truevector, guessvector, 0, 0)

    def femalemale(self, truevector, guessvector):
        return self.count_true2guess(truevector, guessvector, 0, 1)

    def femaleundefined(self, truevector, guessvector):
        return self.count_true2guess(truevector, guessvector, 0, 2)

    def malefemale(self, truevector, guessvector):
        return self.count_true2guess(truevector, guessvector, 1, 0)

    def malemale(self, truevector, guessvector):
        return self.count_true2guess(truevector, guessvector, 1, 1)

    def maleundefined(self, truevector, guessvector):
        return self.count_true2guess(truevector, guessvector, 1, 2)

    def precision(self, truevector, guessvector):
        result = 0
        divider = self.femalefemale(truevector, guessvector)
        divider = divider + self.malemale(truevector, guessvector)
        dividend = self.femalefemale(truevector, guessvector)
        dividend = dividend + self.malemale(truevector, guessvector)
        dividend = dividend + self.malefemale(truevector, guessvector)
        result = divider / dividend
        return result

    def recall(self, truevector, guessvector):
        result = 0
        divider = self.femalefemale(truevector, guessvector)
        divider = divider + self.malemale(truevector, guessvector)
        dividend = self.femalefemale(truevector, guessvector)
        dividend = dividend + self.malemale(truevector, guessvector)
        dividend = dividend + self.malefemale(truevector, guessvector)
        dividend = dividend + self.femaleundefined(truevector, guessvector)
        dividend = dividend + self.maleundefined(truevector, guessvector)
        result = divider / dividend
        return result

    def f1score(self, truevector, guessvector):
        result = 0
        divider = self.precision(truevector, guessvector)
        divider = divider * self.recall(truevector, guessvector)
        dividend = self.precision(truevector, guessvector)
        dividend = dividend + self.recall(truevector, guessvector)
        result = 2 * (divider / dividend)
        return result

    def error_coded(self, truevector, guessvector):
        result = 0
        divider = self.femalemale(truevector, guessvector)
        divider = divider + self.malefemale(truevector, guessvector)
        divider = divider + self.maleundefined(truevector, guessvector)
        divider = divider + self.femaleundefined(truevector, guessvector)
        dividend = self.malemale(truevector, guessvector)
        dividend = dividend + self.femalemale(truevector, guessvector)
        dividend = dividend + self.malefemale(truevector, guessvector)
        dividend = dividend + self.femalefemale(truevector, guessvector)
        dividend = dividend + self.maleundefined(truevector, guessvector)
        dividend = dividend + self.femaleundefined(truevector, guessvector)
        result = divider / dividend
        return result

    def error_coded_without_na(self, truevector, guessvector):
        result = 0
        divider = self.femalemale(truevector, guessvector)
        divider = divider + self.malefemale(truevector, guessvector)
        dividend = self.malemale(truevector, guessvector)
        dividend = dividend + self.femalemale(truevector, guessvector)
        dividend = dividend + self.malefemale(truevector, guessvector)
        dividend = dividend + self.femalefemale(truevector, guessvector)
        result = divider / dividend
        return result

    def na_coded(self, truevector, guessvector):
        result = 0
        divider = self.maleundefined(truevector, guessvector)
        divider = divider + self.femaleundefined(truevector, guessvector)
        dividend = self.malemale(truevector, guessvector)
        dividend = dividend + self.femalemale(truevector, guessvector)
        dividend = dividend + self.malefemale(truevector, guessvector)
        dividend = dividend + self.femalefemale(truevector, guessvector)
        dividend = dividend + self.maleundefined(truevector, guessvector)
        dividend = dividend + self.femaleundefined(truevector, guessvector)
        result = divider / dividend
        return result

    def error_gender_bias(self, truevector, guessvector):
        divider = self.malefemale(truevector, guessvector)
        divider = divider - self.femalemale(truevector, guessvector)
        dividend = self.malemale(truevector, guessvector)
        dividend = dividend + self.femalemale(truevector, guessvector)
        dividend = dividend + self.malefemale(truevector, guessvector)
        dividend = dividend + self.femalefemale(truevector, guessvector)
        result = divider / dividend
        return result

    def weighted_error(self, truevector, guessvector, w):
        divider = self.femalemale(truevector, guessvector)
        divider = divider + self.malefemale(truevector, guessvector)
        dot = self.maleundefined(truevector, guessvector)
        dot = dot + self.femaleundefined(truevector, guessvector)
        divider = divider + w * dot
        dividend = self.malemale(truevector, guessvector)
        dividend = dividend + self.femalemale(truevector, guessvector)
        dividend = dividend + self.malefemale(truevector, guessvector)
        dividend = dividend + self.femalefemale(truevector, guessvector)
        dot = self.maleundefined(truevector, guessvector)
        dot = dot + self.femaleundefined(truevector, guessvector)
        dividend = dividend + w * dot
        result = divider / dividend
        return result

    def accuracy_score_dame(self, v1, v2):
        if (len(v1) == len(v2)):
            success = 0
            fails = 0
            for i in range(0, len(v1)):
                if (v1[i] == v2[i]):
                    success = success + 1
                else:
                    fails = fails + 1
            if (fails == 0):
                accuracy = 1
            else:
                accuracy = success / len(v1)
        else:
            accuracy = 0
            print("Both vectors must have the same length")
        return accuracy

    def accuracy(self, path):
        gl = self.gender_list(path)
        sl = self.guess_list(path, binary=True)
        return self.accuracy_score_dame(gl, sl)

    def confusion_matrix(self, path='files/names/partial.csv'):
        gl = self.gender_list(path)
        sl = self.guess_list(path, binary=True)
        return confusion_matrix(gl, sl)

    def print_confusion_matrix_gender(self, path='', dimensions="2x3"):
        cmd = self.confusion_matrix_gender(path, dimensions)
        print("[[ %s, %s, %s]" % (cmd[0][0], cmd[0][1], cmd[0][2]))
        print(" [ %s, %s, %s]]\n" % (cmd[1][0], cmd[1][1], cmd[1][2]))
        return ""

    def confusion_matrix_gender(self, path='', dimensions="3x2"):
        truevector = self.gender_list(path)
        guessvector = self.guess_list(path, binary=True)
        ff = self.count_true2guess(truevector, guessvector, 0, 0)
        self.femalefemale = ff
        fm = self.count_true2guess(truevector, guessvector, 0, 1)
        self.femalemale = fm
        fu = self.count_true2guess(truevector, guessvector, 0, 2)
        self.femaleundefined = fu
        mf = self.count_true2guess(truevector, guessvector, 1, 0)
        self.malefemale = mf
        mm = self.count_true2guess(truevector, guessvector, 1, 1)
        self.malemale = mm
        mu = self.count_true2guess(truevector, guessvector, 1, 2)
        self.maleundefined = mu
        uf = self.count_true2guess(truevector, guessvector, 1, 0)
        self.undefinedfemale = uf
        um = self.count_true2guess(truevector, guessvector, 1, 1)
        self.undefinedmale = um
        uu = self.count_true2guess(truevector, guessvector, 1, 2)
        self.undefinedundefined = uu

        l = [[self.femalefemale,
              self.femalemale,
              self.femaleundefined],
             [self.malefemale,
              self.malemale,
              self.maleundefined],
             [self.undefinedfemale,
              self.undefinedmale,
              self.undefinedundefined]]

        if (dimensions == "1x1"):
            res = [[l[0][0]]]
        elif (dimensions == "1x2"):
            res = [[l[0][0], l[0][1]]]
        elif (dimensions == "1x3"):
            res = [[l[0][0], l[0][1], l[0][2]]]
        elif (dimensions == "2x1"):
            res = [[l[0][0]], [l[1][0]]]
        elif (dimensions == "2x2"):
            res = [[l[0][0], l[0][1]], [l[1][0], l[1][1]]]
        elif (dimensions == "2x3"):
            res = [[l[0][0], l[0][1], l[0][2]], [l[1][0], l[1][1], l[1][2]]]
        elif (dimensions == "3x1"):
            res = [[l[0][0]], [l[1][0]], [l[2][0]]]
        elif (dimensions == "3x2"):
            res = [[l[0][0],
                    l[0][1]],
                   [l[1][0],
                    l[1][1]],
                   [l[2][0],
                    l[2][1]]]
        elif (dimensions == "3x3"):
            res = [[l[0][0],
                    l[0][1],
                    l[0][2]],
                   [l[1][0],
                    l[1][1],
                    l[1][2]],
                   [l[2][0],
                    l[2][1],
                    l[2][2]]]
        return res

    def features_list(self, path='files/names/partial.csv', sexdataset=''):
        flist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                flist.append(list(self.features_int(name).values()))
        return flist

    def features_list_categorical(self, path='files/names/partial.csv'):
        flist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                l = list([self.features_int(name)["first_letter"],
                          self.features_int(name)["last_letter"],
                          self.features_int(name)["last_letter_a"],
                          self.features_int(name)["first_letter_vocal"],
                          self.features_int(name)["last_letter_vocal"],
                          self.features_int(name)["last_letter_consonant"]])
                flist.append(l)
        return flist

    def features_list_no_categorical(self, path='files/names/partial.csv'):
        flist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                l = list([self.features_int(name)["count(a)"],
                          self.features_int(name)["count(b)"],
                          self.features_int(name)["count(c)"],
                          self.features_int(name)["count(d)"],
                          self.features_int(name)["count(e)"],
                          self.features_int(name)["count(f)"],
                          self.features_int(name)["count(g)"],
                          self.features_int(name)["count(h)"],
                          self.features_int(name)["count(i)"],
                          self.features_int(name)["count(j)"],
                          self.features_int(name)["count(k)"],
                          self.features_int(name)["count(l)"],
                          self.features_int(name)["count(m)"],
                          self.features_int(name)["count(n)"],
                          self.features_int(name)["count(o)"],
                          self.features_int(name)["count(p)"],
                          self.features_int(name)["count(q)"],
                          self.features_int(name)["count(r)"],
                          self.features_int(name)["count(s)"],
                          self.features_int(name)["count(t)"],
                          self.features_int(name)["count(u)"],
                          self.features_int(name)["count(v)"],
                          self.features_int(name)["count(w)"],
                          self.features_int(name)["count(x)"],
                          self.features_int(name)["count(y)"],
                          self.features_int(name)["count(z)"],
                          self.features_int(name)["vocals"],
                          self.features_int(name)["consonants"]])
                flist.append(l)
        return flist

    def features_list_no_letters(self, path='files/names/partial.csv'):
        flist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                l = list([self.features_int(name)["first_letter"],
                          self.features_int(name)["last_letter"],
                          self.features_int(name)["vocals"],
                          self.features_int(name)["consonants"],
                          self.features_int(name)["first_letter_vocal"],
                          self.features_int(name)["last_letter_vocal"],
                          self.features_int(name)["first_letter_consonant"],
                          self.features_int(name)["last_letter_consonant"],
                          self.features_int(name)["last_letter_a"],
                          self.features_int(name)["last_letter_o"]])
                flist.append(l)
        return flist

    def features_list_no_undefined(self, path=''):
        flist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                g = row[4].replace('\"', '')
                if ((g == "m") | (g == "f")):
                    flist.append(list(self.features_int(name).values()))
        return flist

    def features_list2csv(self, path, categorical="both"):
        if (categorical == "categorical"):
            fl = self.features_list_categorical(path)
            first_line = "first_letter, last_letter, last_letter_a, " \
                         "first_letter_vocal, last_letter_vocal, " \
                         "last_letter_consonant"
            f = open('files/features_list_cat.csv', 'w')
        elif (categorical == "nocategorical"):
            fl = self.features_list_no_categorical(path)
            first_line = "a, b, c, d, e, f, g, h, i, j, k, l, m, " \
                         "n, o, p, q, r, s, t, u, v, w, x, y, z, " \
                         "vocals, consonants"
            f = open('files/features_list_no_cat.csv', 'w')
        elif (categorical == "noletters"):
            fl = self.features_list_no_letters(path)
            first_line = "first_letter, last_letter, vocals, " \
                         "consonants, first_letter_vocal," \
                         "last_letter_vocal, first_letter_consonant, " \
                         "last_letter_consonant," \
                         "last_letter_a, last_letter_o"
            f = open('files/features_list_no_letters.csv', 'w')
        elif (categorical == "noundefined"):
            fl = self.features_list_no_undefined(path)
            first_line = "first_letter, last_letter, a, b, c, d, e, " \
                         "f, g, h, i, j, k, l, m, n, o, p, q, r, s, " \
                         "t, u, v, w, x, y, z, vocals, consonants, " \
                         "first_letter_vocal, last_letter_vocal, " \
                         "first_letter_consonant, last_letter_consonant, " \
                         "last_letter_a, last_letter_o"
            f = open('files/features_list_no_undefined.csv', 'w')
        else:
            fl = self.features_list(path)
            first_line = "first_letter, last_letter, a, b, c, d, e, f, " \
                         "g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, " \
                         "v, w, x, y, z, vocals, consonants, " \
                         "first_letter_vocal, last_letter_vocal, " \
                         "first_letter_consonant, last_letter_consonant, " \
                         "last_letter_a, last_letter_o"
            f = open('files/features_list.csv', 'w')
        f.write(first_line+"\n")
        for i in fl:
            line = ""
            count = 0
            while (count < (len(i) - 1)):
                line = line + str(i[count]) + ", "
                count = count + 1
            f.write(line+str(i[count])+"\n")
        f.close()

    def pca(self, path='files/names/partial.csv', n=2):
        X = np.array(self.features_list())
        pca = PCA(n_components=n)
        return pca.fit(X)

    def print_measures(self, gl1, gl2, measure, api_name):
        if (measure == "accuracy"):
            gender_accuracy = self.accuracy_score_dame(gl1, gl2)
            print("%s accuracy: %s" % (api_name, gender_accuracy))

        elif (measure == "precision"):
            gender_precision = self.precision(gl1, gl2)
            print("%s precision: %s" % (api_name, gender_precision))

        elif (measure == "recall"):
            gender_recall = self.recall(gl1, gl1)
            print("%s recall: %s" % (api_name, gender_recall))
        elif (measure == "f1score"):
            gender_f1score = self.f1score(gl1, gl2)
            print("%s f1score: %s" % (api_name, gender_f1score))
