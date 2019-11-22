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
import numpy as np
import requests
import configparser
from damegender.app.dame_gender import Gender
from damegender.app.dame_utils import DameUtils


class DameNameapi(Gender):

    def get(self, name, surname="", binary=False):
        # guess method to check names dictionary
        nameapilist = []
        guess = ""
        confidence = ""
        if (self.config['DEFAULT']['nameapi'] == 'yes'):
            fichero = open(self.config['FILES']['nameapi'], "r+")
            contenido = fichero.readline().rstrip()

            # url of the NameAPI.org endpoint:
            url = (
                "http://rc50-api.nameapi.org/rest/v5.0/parser/personnameparser?"
                "apiKey="+contenido
            )

            # Dict of data to be sent to NameAPI.org:
            payload = {
                "inputPerson": {
                    "type": "NaturalInputPerson",
                    "personName": {
                        "nameFields": [
                            {
                                "string": name,
                                "fieldType": "GIVENNAME"
                            }, {
                                "string": surname,
                                "fieldType": "SURNAME"
                            }
                        ]
                    },
                    "gender": "UNKNOWN",
                    "confidence": "UNKNOW"
                }
            }

            # Proceed, only if no error:
            try:
                # Send request to NameAPI.org by doing the following:
                # - make a POST HTTP request
                # - encode the Python payload dict to JSON
                # - pass the JSON to request body
                # - set header's 'Content-Type' to 'application/json' instead of
                #   default 'multipart/form-data'
                resp = requests.post(url, json=payload)
                resp.raise_for_status()
                # Decode JSON response into a Python dict:
                resp_dict = resp.json()
                guess = resp_dict['matches'][0]['parsedPerson']['gender']['gender'].lower()
                confidence = resp_dict['matches'][0]['parsedPerson']['gender']['confidence']
                if (binary is True):
                    if (guess == 'female'):
                        guess = 0
                    elif (guess == 'male'):
                        guess = 1
                    else:
                        guess = 2
            except requests.exceptions.HTTPError as e:
                print("Bad HTTP status code:", e)
            except requests.exceptions.RequestException as e:
                print("Network error:", e)
        else:
            if (binary is True):
                guess = 2
            else:
                guess = "unknown"
        return [guess, confidence]

    def download(self, path="files/names/partial.csv"):
        du = DameUtils()
        nameapijson = open("files/names/nameapi"+du.path2file(path)+".json", "w+")
        names = self.csv2names(path)
        nameapijson.write("[")
        length = len(names)
        i = 0
        while (i < length):
            nameapijson.write('{"name":"'+names[i]+'",\n')
            g = self.get(names[i], "", binary=True)
            nameapijson.write('"gender":'+str(g[0])+',\n')
            nameapijson.write('"confidence":'+str(g[1])+'\n')
            if ((length -1) == i):
                nameapijson.write('} \n')
            else:
                nameapijson.write('}, \n')
            i = i + 1
        nameapijson.write("]")
        nameapijson.close()
        return 0


    def guess(self, name, surname, binary=False):
        v = self.get(name, surname, binary)
        return v[0]

    def confidence(self, name, surname, binary=False):
        v = self.get(name, surname, binary)
        return v[1]

    def guess_list(self, path='files/names/partial.csv', binary=False):
        # guess list method
        slist = []
        with open(path) as csvfile:
            sexreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(sexreader, None)
            for row in sexreader:
                name = row[0].title()
                name = name.replace('\"', '')
                surname = row[2].title()
                surname = surname.replace('\"', '')
                slist.append(self.guess(name, surname, binary))
        return slist
