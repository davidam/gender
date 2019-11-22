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

# This class is used to operations between all methods/apis

from damegender.app.dame_gender import Gender
from damegender.app.dame_sexmachine import DameSexmachine
from damegender.app.dame_genderize import DameGenderize
from damegender.app.dame_genderapi import DameGenderApi
from damegender.app.dame_namsor import DameNamsor
from damegender.app.dame_genderguesser import DameGenderGuesser


class DameAll(Gender):
    def average(self, name, surname):
        r = 0
        count = 0
        avg = 0
        dgg = DameGenderGuesser()
        guess1 = int(dgg.guess(name, binary="True"))
        if (guess1 != 2):
            r = r + guess1
            count = count + 1
        if (self.config['DEFAULT']['genderapi'] == 'yes'):
            dga = DameGenderApi()
            guess2 = int(dga.guess(name, binary="True"))
            if (guess2 != 2):
                r = r + guess2
                count = count + 1
        if (self.config['DEFAULT']['genderize'] == 'yes'):
            dg = DameGenderize()
            guess3 = int(dg.guess(name, binary="True"))
            if (guess3 != 2):
                r = r + guess3
                count = count + 1
        if (self.config['DEFAULT']['namsor'] == 'yes'):
            dn = DameNamsor()
            guess4 = int(dn.guess(str(name), str(surname), binary="True"))
            if (guess4 != 2):
                r = r + guess4
                count = count + 1
        avg = r / count
        return avg
