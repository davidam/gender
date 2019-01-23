#!/usr/bin/python
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
# along with GNU Emacs; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import csv
import requests
import json
import numpy as np
import request
from app.dame_gender import Gender

class DameNameapi(Gender):

    def guess(self, name, surname, binary=False):
    # guess method to check names dictionary
        nameapilist = []
        fichero = open("files/nameapipass.txt", "r+")
        contenido = fichero.readline().rstrip()
        #print(contenido)

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
                "gender": "UNKNOWN"
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
            if (binary == True):
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

        return guess
