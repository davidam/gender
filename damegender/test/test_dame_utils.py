#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

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
import os
from app.dame_utils import DameUtils
from os.path import expanduser


class TddInPythonExample(unittest.TestCase):

    def test_is_not_blank(self):
        du = DameUtils()
        self.assertEqual(du.is_not_blank("  "), False)
        self.assertEqual(du.is_not_blank("ok"), True)

    def test_various_words_p(self):
        du = DameUtils()
        self.assertEqual(du.various_words_p("david arroyo"), True)
        self.assertEqual(du.various_words_p("Abdul+Ahad"), True)
        self.assertEqual(du.various_words_p(" david arroyo "), True)

    def test_path2file(self):
        du = DameUtils()
        self.assertEqual(du.path2file("files/images/lalla.csv"),
                         "files_images_lalla.csv")

    def test_represents_int(self):
        du = DameUtils()
        self.assertEqual(du.represents_int("23"), True)
        self.assertEqual(du.represents_int("ok"), False)

    def test_split(self):
        u = DameUtils()
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        sp = u.split(x, 5)
        self.assertEqual(sp, [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13]])
        y = list(range(1, 100))
        ysp = u.split(y, 10)
        self.assertEqual(ysp[0:2],
                         [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]])

    def test_drop_dots(self):
        u = DameUtils()
        self.assertEqual(1212, int(u.drop_dots(12.12)))

    def test_drop_accents(self):
        u = DameUtils()
        self.assertEqual("Ines", u.drop_accents("Inés"))

    def test_drop_white_space(self):
        u = DameUtils()
        self.assertEqual("In",
                         u.drop_white_space("In "))
        self.assertEqual("Ines",
                         u.drop_accents(u.drop_white_space("Inés ")))
        self.assertEqual("JuanCarlosI",
                         u.drop_accents(u.drop_white_space("Juan Carlos I ")))

    def test_drop_white_space_around(self):
        u = DameUtils()
        self.assertEqual("In",
                         u.drop_white_space_around(" In"))
        self.assertEqual("Juan Carlos I",
                         u.drop_white_space_around(" Juan Carlos I"))
        self.assertEqual("Juan Carlos I",
                         u.drop_white_space_around(" Juan Carlos I  "))
        self.assertEqual("Juan Carlos I",
                         u.drop_white_space_around(" Juan Carlos I "))
        self.assertEqual("Jose Maria",
                         u.drop_white_space_around(
                             u.drop_accents(" José María ")))
        self.assertEqual("Ines",
                         u.drop_white_space_around(
                             u.drop_accents("Inés ")))
        self.assertEqual("Ana", u.drop_white_space_around(" Ana"))

    def test_drop_white_space_around(self):
        u = DameUtils()
        self.assertEqual(
            "Maria+Jose",
            u.white_space_inside_by(
                u.drop_accents(" María José "),
                "+"))

    def test_drop_quotes(self):
        u = DameUtils()
        self.assertEqual('Hola Mexico', u.drop_quotes('Hola "Mexico'))
        self.assertEqual("Hola Mexico", u.drop_quotes("Hola' 'Mexico"))

    def test_dame_utils_delete_duplicated(self):
        du = DameUtils()
        self.assertEqual(du.delete_duplicated([1, 2, 2, 1, 3]), [1, 2, 3])

    def test_dame_utils_clean_list(self):
        du = DameUtils()
        self.assertEqual(
            du.clean_list(
                ['',
                 'H. Peter Anvin',
                 'hiranotaka@zng.info',
                 'Ram Yalamanchili',
                 'Ferenc Wagner']),
            ['H. Peter Anvin',
             'Ram Yalamanchili',
             'Ferenc Wagner'])

    def test_dame_utils_files_one_level(self):
        du = DameUtils()
        cwd = os.getcwd()
        self.assertTrue(len(du.files_one_level(cwd + '/files/')) > 10)

    def test_dame_utils_files_one_level_drop_pwd(self):
        du = DameUtils()
        cwd = os.getcwd()
        self.assertEqual(
            sorted(du.files_one_level_drop_pwd(cwd+"/files/datamodels")),
            ['files/datamodels/bernoulliNB_model.sav',
             'files/datamodels/forest_model.sav',
             'files/datamodels/gaussianNB_model.sav',
             'files/datamodels/multinomialNB_model.sav',
             'files/datamodels/sgd_model.sav',
             'files/datamodels/svc_model.sav',
             'files/datamodels/xgboost_model.sav'])
