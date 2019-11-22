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

from genderize import Genderize
import csv
import requests
import json
import configparser
from damegender.app.dame_gender import Gender
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


class DameGenderize(Gender):

    def guess(self, name, binary=False):
        # guess method to check names dictionary
        if (self.config['DEFAULT']['genderize'] == 'no'):
            v = Genderize().get([name])
        elif (self.config['DEFAULT']['genderize'] == 'yes'):
            fichero = open(self.config['FILES']['genderize'], "r+")
            apikey = fichero.readline().rstrip()
            v = Genderize(
                user_agent='GenderizeDocs/0.0',
                api_key=apikey).get([name])
        g = v[0]['gender']
        if ((g == 'female') and binary):
            guess = 0
        elif ((g == 'male') and binary):
            guess = 1
        elif (not(binary)):
            guess = g
        return guess

    def prob(self, name, binary=False):
        # guess method to check names dictionary
        if (self.config['DEFAULT']['genderize'] == 'no'):
            v = Genderize().get([name])
        elif (self.config['DEFAULT']['genderize'] == 'yes'):
            fichero = open(self.config['DEFAULT']['genderizefile'], "r+")
            apikey = fichero.readline().rstrip()
            v = Genderize(
                user_agent='GenderizeDocs/0.0',
                api_key=apikey).get([name])
        prob = v[0]['probability']
        return prob

    def guess_list(self, path='files/names/partial.csv', binary=False):
        # guess list method
        slist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            i = 0
            listnames = list()
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                listnames.append(name)
        new = []
        # We must split the list in different lists with size 10
        for i in range(0, len(listnames), 10):
            new.append(listnames[i:i+10])
        for i in new:
            if (self.config['DEFAULT']['genderize'] == 'no'):
                jsonlist = Genderize().get(i)
            elif (self.config['DEFAULT']['genderize'] == 'yes'):
                fichero = open("files/apikeys/genderizepass.txt", "r+")
                apikey = fichero.readline().rstrip()
                jsonlist = Genderize(user_agent='GenderizeDocs/0.0',
                                     api_key=apikey).get(i)
            for item in jsonlist:
                if ((item['gender'] is None) & binary):
                    slist.append(2)
                elif ((item['gender'] is None) & (not binary)):
                    slist.append("unknown")
                elif ((item['gender'] == "male") & binary):
                    slist.append(1)
                elif ((item['gender'] == "male") & (not binary)):
                    slist.append("male")
                elif ((item['gender'] == "female") & binary):
                    slist.append(0)
                elif ((item['gender'] == "female") & (not binary)):
                    slist.append("female")
        return slist
