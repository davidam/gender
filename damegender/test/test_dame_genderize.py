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
from app.dame_genderize import DameGenderize


class TddInPythonExample(unittest.TestCase):

    def test_dame_genderize_guess(self):
        dg = DameGenderize()
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            self.assertEqual(dg.guess("David"), "male")
            self.assertEqual(dg.guess("David", binary=True), 1)

    def test_dame_genderize_prob(self):
        dg = DameGenderize()
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            self.assertEqual(dg.prob("David", binary=True), 1.0)

    def test_dame_genderize_guess_file(self):
        dg = DameGenderize()
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            self.assertEqual(dg.guess("David", binary=True), 1)

    def test_dame_genderize_gender_list(self):
        dg = DameGenderize()
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            gl = dg.gender_list()
            self.assertEqual(gl, [1, 1, 1, 1, 2, 1, 0, 0, 1, 1,
                                  2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1])
            self.assertEqual(len(gl), 21)
            self.assertEqual(dg.females, 3)
            self.assertEqual(dg.males, 16)
            self.assertEqual(dg.unknown, 2)

    def test_dame_genderize_guess_list(self):
        dg = DameGenderize()
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            self.assertEqual(['male', 'male', 'male', 'male', 'unknown',
                              'male', 'female', 'female', 'male', 'male'],
                             dg.guess_list(path="files/names/partial.csv",
                                           binary=False)[0:10])
            self.assertEqual([1, 1, 1, 1, 2, 1, 0, 0, 1, 1],
                             dg.guess_list(path="files/names/partial.csv",
                                           binary=True)[0:10])

    def test_dame_genderize_guess_list(self):
        dg = DameGenderize()
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            self.assertEqual(['male', 'male', 'male', 'male', 'unknown',
                              'male', 'female', 'female', 'male', 'male'],
                             dg.guess_list(path="files/names/partial.csv",
                                           binary=False)[0:10])
            self.assertEqual([1, 1, 1, 1, 2, 1, 0, 0, 1, 1],
                             dg.guess_list(path="files/names/partial.csv",
                                           binary=True)[0:10])
