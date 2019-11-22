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

import configparser
config = configparser.ConfigParser()

genderapi_p = input("Do you have a genderapi key: (Y|N) ")
if (genderapi_p.upper() == "Y"):
   config['DEFAULT']['genderapi'] = 'yes'
   genderapi_key = str(input("Introduce your genderapi key: "))
   fo = open("files/apikeys/genderapipass.txt", "w")
   fo.write(genderapi_key)
   fo.close()
else:
   config['DEFAULT']['genderapi'] = 'no'

genderize_p = input("Do you have a genderize key: (Y|N) ")
if (genderize_p.upper() == "Y"):
   config['DEFAULT']['genderize'] = 'yes'
   genderize_key = input("Introduce your genderize key: ")
   fo = open("files/apikeys/genderizepass.txt", "w")
   fo.write(genderize_key)
   fo.close()
else:
   config['DEFAULT']['genderize'] = 'no'

nameapi_p = input("Do you have a nameapi key: (Y|N) ")
if (nameapi_p.upper() == "Y"):
   config['DEFAULT']['nameapi'] = 'yes'
   nameapi_key = input("Introduce your nameapi key: ")
   fo = open("files/apikeys/nameapipass.txt", "w")
   fo.write(nameapi_key)
   fo.close()
else:
   config['DEFAULT']['nameapi'] = 'no'

namsor_p = input("Do you have a namsor api key: (Y|N) ")
if (namsor_p.upper() == "Y"):
   config['DEFAULT']['namsor'] = 'yes'
   namsor_key = input("Introduce your namsor api key: ")
   fo = open("files/apikeys/namsorpass.txt", "w")
   fo.write(namsor_key)
   fo.close()
else:
   config['DEFAULT']['namsor'] = 'no'

   
customsearch_p = input("Do you have a custom search google key: (Y|N) ")
if (customsearch_p.upper() == "Y"):
   config['DEFAULT']['customsearch'] = 'yes'
   customsearchapikey = input("Introduce your custom search google api key: ")
   customsearchcxkey = input("Introduce your custom search google cx key: ")
   fo1 = open("files/apikeys/customsearchapikey.txt", "w")
   fo2 = open("files/apikeys/customsearchcxkey.txt", "w")
   fo1.write(customsearchapikey)
   fo2.write(customsearchcxkey)
   fo1.close()
   fo2.close()
else:
   config['DEFAULT']['customsearch'] = 'no'


with open('config.cfg', 'w') as configfile:
   config.write(configfile)


# import configparser

# config = configparser.RawConfigParser()
# config.read('example.ini')

# for key in config['bitbucket.org']:
#    print(key)

# print(config['bitbucket.org']['ForwardX11'])
