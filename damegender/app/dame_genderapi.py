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

import csv
import requests
import json
from damegender.app.dame_gender import Gender
from damegender.app.dame_utils import DameUtils

class DameGenderApi(Gender):

    def get(self, name):
        if (self.config['DEFAULT']['genderapi'] == 'yes'):
            fichero = open("files/apikeys/genderapipass.txt", "r+")
            contenido = fichero.readline()
            contenido = contenido.replace('\n', '')
            string = 'https://gender-api.com/get?name=' + name
            string = string + '&key=' + contenido
            r = requests.get(string)
            j = json.loads(r.text)
            v = [j['gender'], j['accuracy']]
        return v

    def guess(self, name, binary=False):
        v = self.get(name)
        if (self.config['DEFAULT']['genderapi'] == 'yes'):
            guess = v[0]
            if (guess == 'male'):
                if binary:
                    guess = 1
            elif (guess == 'female'):
                if binary:
                    guess = 0
            else:
                if binary:
                    guess = 2
                else:
                    guess = 'unknown'
        else:
            if binary:
                guess = 2
            else:
                guess = 'unknown'
        return guess

    def accuracy(self, name):
        v = self.get(name)
        return v[1]

    def download(self, path="files/names/partial.csv"):
        du = DameUtils()
        fichero = open("files/apikeys/genderapipass.txt", "r+")
        backup = open("files/names/genderapi"+du.path2file(path)+".json", "w+")
        contenido = fichero.readline()
        contenido = contenido.replace('\n', '')
        string = ""
        names = self.csv2names(path)
        names_list = du.split(names, 20)
        jsondict = {'names': []}
        string = ""
        for l in names_list:
            # generating names string to include in url
            count = 1
            stringaux = ""
            for n in l:
                if (len(l) > count):
                    stringaux = stringaux + n + ";"
                else:
                    stringaux = stringaux + n
                count = count + 1
                #            string = string + ";" + stringaux
            url1 = 'https://gender-api.com/get?name=' + stringaux
            url1 = url1 + '&multi=true&key=' + contenido
            r = requests.get(url1)
            j = json.loads(r.text)
            jsondict['names'].append(j['result'])
        jsonv = json.dumps(jsondict)
        backup.write(jsonv)
        backup.close()
        return 1

    def json2guess_list(self, jsonf="", binary=False):
        jsondata = open(jsonf).read()
        json_object = json.loads(jsondata)
        guesslist = []
        for i in json_object["names"]:
            if binary:
                if (i['gender'] == 'female'):
                    guesslist.append(0)
                elif (i['gender'] == 'male'):
                    guesslist.append(1)
                else:
                    guesslist.append(2)
            else:
                guesslist.append(i['gender'])
        return guesslist

    def confusion_matrix_gender(self, path='', dimensions="2x3", jsonf=""):
        truevector = self.gender_list(path)
        if (jsonf != ""):
            guessvector = self.json2guess_list(jsonf="", binary=True)
        else:
            guessvector = self.guess_list(path, binary=True)
        # femalefemale
        self.ff = self.count_true2guess(truevector, guessvector, 0, 0)
        # femalemale
        self.fm = self.count_true2guess(truevector, guessvector, 0, 1)
        # femaundefined
        self.fu = self.count_true2guess(truevector, guessvector, 0, 2)
        # malefemale
        self.mf = self.count_true2guess(truevector, guessvector, 1, 0)
        # malemale
        self.mm = self.count_true2guess(truevector, guessvector, 1, 1)
        # maleundefined
        self.mu = self.count_true2guess(truevector, guessvector, 1, 2)
        # undefinedfemale
        self.uf = self.count_true2guess(truevector, guessvector, 1, 0)
        # undefinedmale
        self.um = self.count_true2guess(truevector, guessvector, 1, 1)
        # undefinedundefined
        self.uu = self.count_true2guess(truevector, guessvector, 1, 2)

        l = [[self.ff, self.fm, self.fu],
             [self.mf, self.mm, self.mu],
             [self.uf, self.um, self.uu]]

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
            res = [[l[0][0], l[0][1]], [l[1][0], l[1][1]], [l[2][0], l[2][1]]]
        elif (dimensions == "3x3"):
            res = [[l[0][0], l[0][1], l[0][2]],
                   [l[1][0], l[1][1], l[1][2]],
                   [l[2][0], l[2][1], l[2][2]]]
        return res

    def print_confusion_matrix_gender(self, path='files/names/partial.csv', dimensions="2x3", jsonf=""):
        cmd = self.confusion_matrix_gender(path, dimensions, jsonf)
        print("[[ %s, %s, %s]" % (cmd[0][0], cmd[0][1], cmd[0][2]))
        print(" [ %s, %s, %s]]\n" % (cmd[1][0], cmd[1][1], cmd[1][2]))
        return ""

    def guess_list(self, path="files/names/partial.csv", binary=False):
        du = DameUtils()
        fichero = open("files/apikeys/genderapipass.txt", "r+")
        contenido = fichero.readline()
        string = ""
        names = self.csv2names(path)
        list_total = []
        names_list = du.split(names, 20)
        for l in names_list:
            count = 1
            string = ""
            for n in l:
                if (len(l) > count):
                    string = string + n + ";"
                else:
                    string = string + n
                count = count + 1
            url = 'https://gender-api.com/get?name='
            url = url + string + '&multi=true&key=' + contenido
            r = requests.get(url)
            d = json.loads(r.text)
            slist = []
            for item in d['result']:
                if (((item['gender'] is None) or (item['gender'] == 'unknown')) & binary):
                    slist.append(2)
                elif (((item['gender'] is None) or (item['gender'] == 'unknown')) & (not binary)):
                    slist.append("unknown")
                elif ((item['gender'] == "male") & binary):
                    slist.append(1)
                elif ((item['gender'] == "male") & (not binary)):
                    slist.append("male")
                elif ((item['gender'] == "female") & binary):
                    slist.append(0)
                elif ((item['gender'] == "female") & (not binary)):
                    slist.append("female")
            # print("string: " + string)
            # print("slist: " + str(slist))
            # print("slist len:" + str(len(slist)))
            list_total = list_total + slist
        return list_total
