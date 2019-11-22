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

from app.dame_gender import Gender
from app.dame_genderguesser import DameGenderGuesser
from app.dame_genderapi import DameGenderApi
from app.dame_genderize import DameGenderize
from app.dame_namsor import DameNamsor
from app.dame_nameapi import DameNameapi
from app.dame_all import DameAll
from app.dame_utils import DameUtils
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('name',  help="Name to be detected")
parser.add_argument('--surname', help="Surname to be detected")
parser.add_argument("--api", choices=['namsor', 'genderize', 'genderguesser', 'genderapi', 'nameapi'], required=True)
#parser.add_argument('--prob', default="yes", choices=['yes', 'no'])
parser.add_argument('--version', action='version', version='0.1')

args = parser.parse_args()

du = DameUtils()
dg = Gender()

if (len(sys.argv) > 1):
    if (args.api == "genderguesser"):
        dgg = DameGenderGuesser()
        print(dgg.guess(args.name))
    elif (args.api == "genderapi"):
        if (dg.config['DEFAULT']['genderapi'] == 'yes'):
            dga = DameGenderApi()
            print(dga.guess(args.name))
            print("accuracy: " + str(dga.accuracy(args.name)))
        else:
            print("You must enable genderapi in config.cfg file")
    elif (args.api == "genderize"):
        if (dg.config['DEFAULT']['genderize'] == 'yes'):
            dg = DameGenderize()
            print(dg.guess(args.name))
            print("probability: " + str(dg.prob(args.name)))
        else:
            print("You must enable genderize in config.cfg file")
    elif (args.api == "namsor"):
        if (dg.config['DEFAULT']['namsor'] == 'yes'):
            dn = DameNamsor()
            if (du.is_not_blank(args.surname)):
                print(dn.guess(str(args.name), str(args.surname)))
                print("scale: " + str(dn.scale(str(args.name), str(args.surname))))
            else:
                print("Surname is required in namsor api")
        else:
            print("You must enable namsor in config.cfg file")
    elif (args.api == "nameapi"):
        if (dg.config['DEFAULT']['nameapi'] == 'yes'):
            dn = DameNameapi()
            print(dn.guess(str(args.name), str(args.surname)))
            print("confidence: " + str(dn.confidence(str(args.name), str(args.surname))))
        else:
            print("You must enable nameapi in config.cfg file")

    # elif (args.api == "average"):
    #     da = DameAll()
    #     average = da.average(args.name, args.surname)
    #     print("average: " + str(average))
