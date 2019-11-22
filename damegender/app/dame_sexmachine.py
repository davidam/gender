#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: David Arroyo Menéndez.
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

from pprint import pprint
from nltk.corpus import names
import csv
import nltk
import re
import unidecode
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from xgboost import XGBClassifier
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import pickle
from damegender.app.dame_gender import Gender


class DameSexmachine(Gender):
    def __init__(self):
        self.males = 0
        self.females = 0
        self.unknown = 0

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
            n = name.lower().count(letter)
            features_int["count({})".format(letter)] = n
        features_int["vocals"] = 0
        for letter in 'aeiou':
            features_int["vocals"] = features_int["vocals"] + 1
        features_int["consonants"] = 0
        for letter in 'bcdfghjklmnpqrstvwxyz':
            features_int["consonants"] = features_int["consonants"] + 1
        if (chr(features_int["first_letter"]) in 'aeiou'):
            features_int["first_letter_vocal"] = 1
        else:
            features_int["first_letter_vocal"] = 0
        if (chr(features_int["last_letter"]) in 'aeiou'):
            features_int["last_letter_vocal"] = 1
        else:
            features_int["last_letter_vocal"] = 0
        # h = hyphen.Hyphenator('en_US')
        # features_int["syllables"] = len(h.syllables(name))
        if (ord(name[-1].lower()) == "a"):
            features_int["last_letter_a"] = 1
        else:
            features_int["last_letter_a"] = 0
        return features_int

    def classifier(self):
        # NLTK bayesian classifier

        labeled_names = []
        for name in names.words('male.txt'):
            elem = [(name, 'male')]
            labeled_names = labeled_names + elem

        for name in names.words('female.txt'):
            elem = [(name, 'female')]
            labeled_names = labeled_names + elem

        featuresets = [(self.features(n), gender) for (n, gender) in
                       labeled_names]
        train_set, test_set = featuresets[500:], featuresets[:500]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        return classifier

    def svc(self):
        # Scikit svc classifier
        X = np.array(self.features_list(path="files/names/all.csv"))
        y = self.gender_list(path="files/names/all.csv")
        clf = svm.SVC()
        clf.fit(X, y)
        filename = 'files/datamodels/svc_model.sav'
        pickle.dump(clf, open(filename, 'wb'))
        return clf

    def svc_load(self):
        pkl_file = open('files/datamodels/svc_model.sav', 'rb')
        clf = pickle.load(pkl_file)
        pkl_file.close()
        return clf

    def sgd(self):
        # Scikit classifier
        X = np.array(self.features_list(path="files/names/all.csv"))
        y = self.gender_list("files/names/all.csv")
        clf = SGDClassifier(loss="log").fit(X, y)
        filename = 'files/datamodels/sgd_model.sav'
        pickle.dump(clf, open(filename, 'wb'))
        return clf

    def sgd_load(self):
        pkl_file = open('files/datamodels/sgd_model.sav', 'rb')
        clf = pickle.load(pkl_file)
        pkl_file.close()
        return clf

    def gaussianNB(self):
        # Scikit bayesian classifier
        x = np.array(self.features_list(path="files/names/all.csv"))
        y = np.array(self.gender_list(path="files/names/all.csv"))
        # Create a Gaussian Classifier
        model = GaussianNB()
        # Train the model using the training sets
        model.fit(x, y)
        filename = 'files/datamodels/gaussianNB_model.sav'
        pickle.dump(model, open(filename, 'wb'))
        return model

    def gaussianNB_load(self):
        pkl_file = open('files/datamodels/gaussianNB_model.sav', 'rb')
        clf = pickle.load(pkl_file)
        pkl_file.close()
        return clf

    def multinomialNB(self):
        # Scikit bayesian classifier
        X = np.array(self.features_list(path="files/names/all.csv"))
        y = np.array(self.gender_list(path="files/names/all.csv"))
        model = MultinomialNB()
        model.fit(X, y)
        filename = 'files/datamodels/multinomialNB_model.sav'
        pickle.dump(model, open(filename, 'wb'))
        return model

    def multinomialNB_load(self):
        pkl_file = open('files/datamodels/multinomialNB_model.sav', 'rb')
        clf = pickle.load(pkl_file)
        pkl_file.close()
        return clf

    def bernoulliNB(self):
        # Scikit bayesian classifier
        X = np.array(self.features_list(path="files/names/all.csv"))
        y = np.array(self.gender_list(path="files/names/all.csv"))
        model = BernoulliNB()
        model.fit(X, y)
        filename = 'files/datamodels/bernoulliNB_model.sav'
        pickle.dump(model, open(filename, 'wb'))
        return model

    def bernoulliNB_load(self):
        pkl_file = open('files/datamodels/bernoulliNB_model.sav', 'rb')
        clf = pickle.load(pkl_file)
        pkl_file.close()
        return clf

    def forest(self):
        # Scikit forest classifier
        X = np.array(self.features_list(path="files/names/all.csv"))
        y = np.array(self.gender_list(path="files/names/all.csv"))
        X, y = make_classification(n_samples=7000,
                                   n_features=33,
                                   n_informative=33,
                                   n_redundant=0,
                                   random_state=0,
                                   shuffle=False)
        rf = RandomForestRegressor(n_estimators=20, random_state=0)
        rf.fit(X, y)
        filename = 'files/datamodels/forest_model.sav'
        pickle.dump(rf, open(filename, 'wb'))
        return rf

    def forest_load(self):
        pkl_file = open('files/datamodels/forest_model.sav', 'rb')
        clf = pickle.load(pkl_file)
        pkl_file.close()
        return clf

    def xgboost(self):
        # Scikit xgboost classifier
        X = np.array(self.features_list(path="files/names/all.csv"))
        y = np.array(self.gender_list(path="files/names/all.csv"))
        model = XGBClassifier()
        model.fit(X, y)
        filename = 'files/datamodels/xgboost_model.sav'
        pickle.dump(model, open(filename, 'wb'))
        return model

    def xgboost_load(self):
        pkl_file = open('files/datamodels/xgboost_model.sav', 'rb')
        clf = pickle.load(pkl_file)
        pkl_file.close()
        return clf

    def string2array(self, string):
        res = ""
        string = unidecode.unidecode(string)
        if re.search(r' ', string):
            res = re.sub(r' +', ' ', string)
        array = res.split(' ')
        return array

    def guess_surname(self, string):
        # A first version without ML
        path = 'files/names/surnames.csv'
        boolean = False
        with open(path) as csvfile:
            surnamereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(surnamereader, None)
            for row in surnamereader:
                surname = row[0]
                if (surname.lower() == string.lower()):
                    boolean = True
        return boolean

    def string2gender(self, string):
        # TODO: take care with trash strings before the name
        arr = self.string2array(string)
        name = ""
        i = 0
        features_int = self.features_int(string)
        while ((name == "") and (len(arr) > i)):
            if (not(self.guess_surname(arr[i])) and (len(string) > 0)):
                name = arr[i]
            i = i + 1
        return self.guess(name)

    def guess(self, name, binary=False, ml="nltk"):
        # guess method to check names dictionary and nltk classifier
        guess = 2
        guess = super().guess(name, binary)
        vector = self.features_int(name)
        if ((guess == 'unknown') | (guess == 2)):
            classifier = self.classifier()
            s = DameSexmachine()
            vector = list(s.features_int(name).values())
            if (ml == "nltk"):
                guess = classifier.classify(self.features(name))
            elif (ml == "svc"):
                m = s.svc_load()
                predicted = m.predict([vector])
                guess = predicted[0]
            elif (ml == "sgd"):
                m = s.sgd_load()
                predicted = m.predict([vector])
                guess = predicted[0]
            elif (ml == "gaussianNB"):
                m = s.gaussianNB_load()
                predicted = m.predict([vector])
                guess = predicted[0]
            elif (ml == "multinomialNB"):
                m = s.multinomialNB_load()
                predicted = m.predict([vector])
                guess = predicted[0]
            elif (ml == "bernoulliNB"):
                m = s.bernoulliNB_load()
                predicted = m.predict([vector])
                guess = predicted[0]
            elif (ml == "forest"):
                m = s.forest_load()
                predicted = m.predict([vector])
                guess = predicted[0]
            elif (ml == "xgboost"):
                m = s.xgboost_load()
                predicted = m.predict([vector])
                guess = predicted[0]
            if binary:
                if (guess == 'female'):
                    guess = 0
                elif (guess == 'male'):
                    guess = 1
                elif (guess == 'unkwnon'):
                    guess = 2
            else:
                if (guess == 0):
                    guess = 'female'
                elif (guess == 1):
                    guess = 'male'
                elif (guess == 2):
                    guess = 'unknown'
        return guess

    def guess_list(self, path='files/names/partial.csv',
                   binary=False, ml="nltk"):
        # guess list method
        slist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                slist.append(self.guess(name, binary, ml=ml))
        return slist

    def confusion_matrix_gender(self, path='', dimensions="3x2", ml='nltk'):
        truevector = self.gender_list(path)
        guessvector = self.guess_list(path,
                                      binary=True,
                                      ml=ml)
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

    def print_confusion_matrix_gender(self, path='files/names/partial.csv', dimensions="3x2", ml="nltk"):
        cmd = self.confusion_matrix_gender(path, dimensions, ml=ml)
        print("[[ %s, %s, %s]" % (cmd[0][0], cmd[0][1], cmd[0][2]))
        print(" [ %s, %s, %s]]\n" % (cmd[1][0], cmd[1][1], cmd[1][2]))
        return ""

    def num_females(self, url, directory):
        # Extracting females with perceval
        gg = GenderGit()
        r = gg.repo("https://github.com/grimoirelab/perceval.git",
                    "/tmp/clonedir")
        count = 0
        for user in r.fetch():
            name = gg.removeMail(user['data']['Author'])
            sm = self.guess(name)
            if (sm == 'female'):
                count = count + 1
        return count

    def num_males(self, url, directory):
        # Extracting males with perceval
        gg = GenderGit()
        r = gg.repo("https://github.com/grimoirelab/perceval.git",
                    "/tmp/clonedir")
        count = 0
        for user in r.fetch():
            name = gg.removeMail(user['data']['Author'])
            sm = self.guess(name)
            if (sm == 'male'):
                count = count + 1
        return count
