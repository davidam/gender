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

import unicodedata
import re
import os


class DameUtils():
    def is_not_blank(self, s):
        return bool(s and s.strip())

    def various_words_p(self, s):
        match = re.search(r"( ?(\w+)( \w)+)|( ?(\w+)(\+\w)+)", s)
        if match:
            return 1
        else:
            return 0

    def represents_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def split(self, arr, size):
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr = arr[size:]
        arrs.append(arr)
        return arrs

    def path2file(self, s):
        aux = ""
        for c in unicodedata.normalize('NFD', str(s)):
            if ((c == ' ') | (c == '/')):
                aux = aux + "_"
            else:
                aux = aux + c
        return aux

    def drop_dots(self, s):
        aux = ""
        for c in unicodedata.normalize('NFD', str(s)):
            if (c != '.'):
                aux = aux + c
        return aux

    def drop_quotes(self, s):
        aux = ""
        for c in unicodedata.normalize('NFD', str(s)):
            if ((c != '"') and (c != "'")):
                aux = aux + c
        return aux

    def drop_white_space(self, s):
        aux = ""
        for c in unicodedata.normalize('NFD', str(s)):
            if (c != ' '):
                aux = aux + c
        return aux

    def white_space_inside_by(self, s, by):
        inside = 0
        aux = ""
        string = self.drop_white_space_around(s)
        for c in unicodedata.normalize('NFD', str(string)):
            if (c == ' '):
                aux = aux + by
            else:
                aux = aux + c
        return aux

    def drop_white_space_around(self, s):
        aux = ""
        arr = unicodedata.normalize('NFD', str(s))
        i = 0
        j = -1
        while (i != j):
            if (arr[i] == " "):
                aux = ""
            else:
                aux = aux + arr[i]
                j = i + 1
            i = i + 1
        j = -1
        while (len(arr) > i) and (i != j):
            if (arr[i].isalpha()):
                aux = aux + arr[i]
            elif ((arr[i] == " ") and (len(arr) == (i+1))):
                j = i+1
            elif ((arr[i] == " ") and (arr[i+1].isalpha())):
                aux = aux + arr[i]
            else:
                j = i+1
            i = i+1
        return aux

    def drop_accents(self, s):
        return ''.join((c for c in unicodedata.normalize('NFD', s)
                        if unicodedata.category(c) != 'Mn'))

    def drop_pwd(self, s):
        cwd = os.getcwd()
        result = ""
        if re.search(cwd, s):
            result = re.sub(cwd+'/', '', s)
        return result

    def delete_duplicated(self, l):
        if (len(l) == 0):
            return l
        else:
            rest = []
            for i in l:
                if (i != l[0]):
                    rest = rest + [i]
        return [l[0]] + self.delete_duplicated(rest)

    def clean_list(self, l):
        if (len(l) == 0):
            print([])
        else:
            aux = []
            for i in l:
                if ((i != "") and (not(re.search(r' ?.*@.*\..*', i)))):
                    aux = aux + [i]
        return aux

    def files_one_level(self, directory):
        f = os.popen('find ' + directory)
        l = []
        for line in f:
            fields = line.strip().split()
            l.append(fields[0])
        return l

    def files_one_level_drop_pwd(self, directory):
        f = os.popen('find ' + directory)
        l = []
        for line in f:
            fields = line.strip().split()
            if not(os.path.isdir(fields[0])):
                l.append(self.drop_pwd(fields[0]))
        return l
