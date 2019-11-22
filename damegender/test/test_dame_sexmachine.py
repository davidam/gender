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

import unittest
import numpy as np
import pickle
import os.path

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import SGDClassifier
from xgboost import XGBClassifier
from sklearn import svm
from app.dame_sexmachine import DameSexmachine


class TddInPythonExample(unittest.TestCase):

    def test_string2array(self):
        array = "muchos    espacios en blanco"
        s = DameSexmachine()
        arr = s.string2array(array)
        self.assertEqual(["muchos", "espacios", "en", "blanco"], arr)

    def test_sexmachine_features(self):
        s = DameSexmachine()
        f = s.features("David")
        self.assertEqual(f['has(a)'], True)
        self.assertEqual(f['count(i)'], 1)
        self.assertEqual(f['count(v)'], 1)
        self.assertEqual(f['last_letter'], 'd')
        self.assertEqual(f['first_letter'], 'd')

    def test_dame_sexmachine_features_int(self):
        s = DameSexmachine()
        f = s.features_int("David")
        self.assertTrue(len(f) > 0)

    def test_dame_sexmachine_guess(self):
        s = DameSexmachine()
        self.assertEqual(s.guess("David"), 'male')
        self.assertEqual(s.guess("David", binary=True, ml="svc"), 1)
        self.assertEqual(s.guess("Laura", binary=True, ml="svc"), 0)
        self.assertEqual(s.guess("Palabra", binary=True, ml="svc"), 1)
        self.assertEqual(s.guess("Laura", binary=True, ml="sgd"), 0)
        self.assertEqual(s.guess("Palabra", binary=True, ml="svc"), 1)
        self.assertEqual(s.guess("David", binary=True, ml="gaussianNB"), 1)
        self.assertEqual(s.guess("David", binary=True, ml="multinomialNB"), 1)
        self.assertEqual(s.guess("David", binary=True, ml="bernoulliNB"), 1)
        self.assertEqual(s.guess("Laura"), 'female')
        # With accents:
        self.assertEqual(s.guess("Inés"), 'female')
        # Without accents:
        self.assertEqual(s.guess("Ines"), 'female')
        self.assertEqual(s.guess("Nodiccionario"), 'male')
        self.assertEqual(s.guess("Nadiccionaria"), 'female')
        self.assertEqual(s.guess("David", binary=True), 1)
        self.assertEqual(s.guess("Laura", binary=True), 0)
        self.assertEqual(s.guess("Nodiccionario", binary=True), 1)
        self.assertEqual(s.guess("Nadiccionaria", binary=True), 0)

    def test_dame_sexmachine_guess_surname(self):
        s = DameSexmachine()
        self.assertTrue(s.guess_surname("Smith"))

    def test_dame_sexmachine_guess_list(self):
        ds = DameSexmachine()
        self.assertEqual(['male', 'male', 'male', 'male', 'male', 'male',
                          'male', 'female', 'male', 'male', 'male',
                          'male', 'male', 'male', 'female', 'male',
                          'male', 'male', 'female', 'male', 'male'],
                         ds.guess_list(path="files/names/partial.csv",
                                       binary=False))
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
                          1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
                         ds.guess_list(path="files/names/partial.csv",
                                       binary=True))
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
                          1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
                         ds.guess_list(path="files/names/partial.csv",
                                       binary=True,
                                       ml="nltk"))
        svc_model = ds.svc_load()
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                          1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                         ds.guess_list(path="files/names/partial.csv",
                                       binary=True,
                                       ml="svc"))

    def test_sexmachine_features_int(self):
        s = DameSexmachine()
        dicc = s.features_int("David")
        self.assertEqual(chr(dicc['last_letter']), 'd')
        self.assertEqual(chr(dicc['first_letter']), 'd')
        self.assertEqual(dicc['count(a)'], 1)
        self.assertEqual(dicc['count(b)'], 0)
        self.assertEqual(dicc['count(c)'], 0)
        self.assertEqual(dicc['count(d)'], 2)
        self.assertEqual(dicc['count(e)'], 0)
        self.assertEqual(dicc['count(f)'], 0)
        self.assertEqual(dicc['count(h)'], 0)
        self.assertEqual(dicc['count(i)'], 1)
        self.assertEqual(dicc['count(v)'], 1)
        self.assertTrue(dicc['count(a)'] > 0)
        self.assertTrue(dicc['vocals'], 2)
        self.assertTrue(dicc['consonants'], 3)
        self.assertEqual(dicc['first_letter_vocal'], 0)
        self.assertEqual(dicc['last_letter_vocal'], 0)
        self.assertTrue(len(dicc.values()) > 30)

    def test_sexmachine_features_list(self):
        s = DameSexmachine()
        fl = s.features_list()
        self.assertTrue(len(fl) > 20)

    def test_sexmachine_features_list_all(self):
        s = DameSexmachine()
        fl = s.features_list(path="files/names/all.csv")
        self.assertTrue(len(fl) > 1000)

    def test_sexmachine_gender_list(self):
        s = DameSexmachine()
        gl = s.gender_list()
        self.assertEqual(gl, [1, 1, 1, 1, 2, 1, 0, 0, 1, 1,
                              2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1])
        self.assertEqual(len(gl), 21)
        self.assertEqual(s.females, 3)
        self.assertEqual(s.males, 16)
        self.assertEqual(s.unknown, 2)

    def test_sexmachine_gender_list_all(self):
        s = DameSexmachine()
        gl = s.gender_list(path="files/names/all.csv")
        self.assertTrue(len(gl) > 1000)

    def test_dame_gender_guess_list(self):
        ds = DameSexmachine()
        self.assertEqual(['male', 'male', 'male', 'male', 'male', 'male',
                          'male', 'female', 'male', 'male', 'male',
                          'male', 'male', 'male', 'female', 'male',
                          'male', 'male', 'female', 'male', 'male'],
                         ds.guess_list(path="files/names/partial.csv",
                                       binary=False))
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1,
                          1, 1, 0, 1, 1, 1, 0, 1, 1],
                         ds.guess_list(path="files/names/partial.csv",
                                       binary=True,
                                       ml="nltk"))
    def test_sexmachine_classifier(self):
        s = DameSexmachine()
        classifier = s.classifier()
        n = s.features("David")
        guess = classifier.classify(n)
        self.assertTrue(1, n)

    def test_sexmachine_accuracy(self):
        s = DameSexmachine()
        self.assertTrue(s.accuracy(path="files/names/partial.csv") > 0.5)

    def test_sexmachine_confusion_matrix(self):
        ds = DameSexmachine()
        cm = ds.confusion_matrix()
        am = np.array([[2, 1, 0],
                       [1, 15, 0],
                       [0, 2, 0]])
        self.assertTrue(np.array_equal(cm, am))

    def test_sexmachine_string2gender(self):
        s = DameSexmachine()
        gender1 = s.string2gender("Arroyo Menéndez, David")
        gender2 = s.string2gender("xxxxx Laura")
        self.assertTrue(gender1, 'male')
        self.assertTrue(gender2, 'female')

    def test_sexmachine_forest(self):
        self.assertTrue(os.path.isfile("files/datamodels/forest_model.sav"))

    def test_sexmachine_forest_load(self):
        s = DameSexmachine()
        m = s.forest_load()
        predicted = m.predict([[0,  0,  1,  0, 21,  0,  0,  0,  0, 34,
                                2,  0,  0,  0,  0,  0, 0,  0,  0,  5,
                                0,  0,  0,  0,  0,  2,  0,  0,  0, 34,
                                1,  0, 1]])
        a = np.array([0.6333333333333334])
        self.assertEqual(predicted[0], a[0])

    def test_sexmachine_sgd_model_exists(self):
        self.assertTrue(os.path.isfile("files/datamodels/sgd_model.sav"))

    def test_sexmachine_sgd_load(self):
        s = DameSexmachine()
        m = s.sgd_load()
        predicted = m.predict([[0,  0,  1,  0, 21,  0,  0,  0,  0, 34,
                                2,  0,  0,  0,  0,  0, 0,  0,  0,  5,
                                0,  0,  0,  0,  0,  2,  0,  0,  0, 34,
                                1,  0, 1]])
        n = np.array([1])
        self.assertEqual(n, predicted)

    def test_sexmachine_svc_load(self):
        s = DameSexmachine()
        m = s.svc_load()
        predicted = m.predict([[0,  0,  1,  0, 21,  0,  0,  0,  0, 34,
                                2,  0,  0,  0,  0,  0, 0,  0,  0,  5,
                                0,  0,  0,  0,  0,  2,  0,  0,  0, 34,
                                1,  0, 1]])
        n = np.array([1])
        self.assertTrue(np.array_equal(predicted, n))

    def test_sexmachine_multinomialNB_load(self):
        s = DameSexmachine()
        m = s.multinomialNB_load()
        array = [[0,  0,  1,  0, 21,  0,  0,  0,  0,
                  34,  2,  0,  0,  0,  0,  0, 0, 0,
                  0,  0,  5,  0,  0,  0,  0,  0,  2,
                  0,  0,  0, 34,  1,  0],
                 [0,  0,  0,  0, 21,  0,  0,  0,  0,
                  34,  0,  0,  0,  0,  0,  1, 0, 0,
                  0,  0,  5,  0,  0,  1,  0,  0,  1,
                  0,  0,  1, 34,  0,  0]]
        predicted = m.predict(array)
        n = np.array([0, 0])
        self.assertTrue(np.array_equal(predicted, n))

    def test_sexmachine_bernoulliNB_load(self):
        s = DameSexmachine()
        m = s.bernoulliNB_load()
        predicted = m.predict(
            [[0,  0,  1,  0, 21,  0,  0,  0,  0, 34,
              2,  0,  0,  0,  0,  0, 0,  0,  0,  5,
              0,  0,  0,  0,  0,  2,  0,  0,  0, 34,
              1,  0, 1]])
        n = np.array([2])
        self.assertTrue(np.array_equal(predicted, n))

    def test_sexmachine_xgboost(self):
        self.assertTrue(os.path.isfile("files/datamodels/xgboost_model.sav"))

    def test_sexmachine_xgboost_load(self):
        s = DameSexmachine()
        m = s.xgboost_load()
        predicted = m.predict(
            [[0,  0,  1,  0, 21,  0,  0,  0,  0, 34,
              2,  0,  0,  0, 0,  0, 0,  0,  0,  5,
              0,  0,  0,  0,  0,  2,  0,  0, 0, 34,
              1,  0, 1]])
        n = np.array([0])
        self.assertTrue(np.array_equal(predicted, n))
