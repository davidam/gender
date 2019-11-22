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
from app.dame_perceval import DamePerceval


class TddInPythonExample(unittest.TestCase):

    def test_dame_perceval_numcommits_method_returns_correct_result(self):
        gg = DamePerceval()
        n = gg.numCommits("https://github.com/grimoirelab/perceval.git",
                          "/tmp/clonedir")
        self.assertTrue(1000 < n)

    def test_dame_perceval_removeMail_method_returns_correct_result(self):
        gg = DamePerceval()
        nomail = gg.removeMail("Santiago Dueñas <sduenas@bitergia.com>")
        self.assertEquals(nomail, "Santiago Dueñas")

    def test_dame_perceval_firstName_method_returns_correct_result(self):
        gg = DamePerceval()
        first = gg.firstName("Santiago Dueñas")
        self.assertEquals(first, "Santiago")

    def test_dame_perceval_secondName_method_returns_correct_result(self):
        gg = DamePerceval()
        second = gg.secondName("Santiago Dueñas")
        self.assertEquals(second, "Dueñas")

    def test_dame_perceval_list_committers_method_returns_correct_result(self):
        gg = DamePerceval()
        self.assertTrue(
            len(gg.list_committers(
                "https://github.com/grimoirelab/perceval.git",
                "/tmp/clonedir")) > 100)

    def test_dame_perceval_list_mailers_method_returns_correct_result(self):
        gg = DamePerceval()
        n = gg.numMails(
            "http://mail-archives.apache.org/mod_mbox/httpd-announce/")
        self.assertTrue(n >= 0)

    def test_dame_perceval_list_mailers_method_returns_correct_result(self):
        gg = DamePerceval()
        self.assertTrue(
            len(
                gg.list_mailers(
                    'http://mail-archives.apache.org/mod_mbox/httpd-announce/')
            ) >= 0)
