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

import pprint
from googleapiclient.discovery import build
from damegender.app.dame_gender import Gender


class DameCustomsearch(Gender):

    def get(self, name, binary=True):
        filekey = open("files/apikeys/customsearchapikey.txt", "r+")
        cxfilekey = open("files/apikeys/customsearchcxkey.txt", "r+")
        content = filekey.readline().rstrip()
        cxcontent = cxfilekey.readline().rstrip()
        service = build("customsearch", "v1", developerKey=content)
        res1 = service.cse().list(
            q=name+'+male',
            cx=cxcontent,
        ).execute()
        res2 = service.cse().list(
            q=name+'+female',
            cx=cxcontent,
        ).execute()
        rmale = res1['searchInformation']['totalResults']
        rfemale = res2['searchInformation']['totalResults']
        if (rfemale > rmale):
            if (binary is True):
                guess = 0
            else:
                guess = "female"
        elif (rmale > rfemale):
            if (binary is True):
                guess = 1
            else:
                guess = "male"
        dicc = {"guess": guess, "rfemale": rfemale, "rmale": rmale}
        return dicc

    def prob(self, name):
        v = self.get(name, False)
        if (guess == "female"):
            prob = dicc["rfemale"] / (dicc["rfemale"] + dicc["rmale"])
        elif (guess == "male"):
            prob = dicc["rmale"] / (dicc["rfemale"] + dicc["rmale"])
        return prob

    def guess(self, name, binary=True):
        return self.get(name, binary)["guess"]
