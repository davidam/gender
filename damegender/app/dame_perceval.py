#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: David Arroyo Menéndez.
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

from perceval.backends.core.mbox import MBox
from perceval.backends.core.git import Git
import re


class DamePerceval(object):

    def numCommits(self, url, directory):
        repo = Git(uri=url, gitpath=directory)
        count = 0
        for commit in repo.fetch():
            count += 1
        return count

    def numMails(self, url, directory="files/mbox"):
        repo = MBox(uri=url, dirpath=directory)
        count = 0
        for message in repo.fetch():
            count += 1
        return count

    def removeMail(self, s):
        result = ""
        if re.search(r' ?<.*@.*>', s):
            result = re.sub(r' ?<.*@.*>', '', s)
        return result

    def firstName(self, s):
        result = ""
        m = re.match("(\w+)", s)
        if m:
            first = m.group(1)
        else:
            first = ""
        return first

    def secondName(self, s):
        result = ""
        m = re.match("(\w+) (\w+)", s)
        if m:
            second = m.group(2)
        else:
            second = ""
        return second

    def list_committers(self, url, directory):
        # Return the list containing the strings
        # from a git repository related to the
        # users ordered by commit including
        # repeated users to allow count gender contributions.
        repo = Git(uri=url, gitpath=directory)
        list_committers = []
        for user in repo.fetch():
            committer = self.removeMail(user['data']['Author'])
            list_committers.append(committer)
        return list_committers

    def list_mailers(self, url, directory="files/mbox"):
        repo = MBox(uri=url, dirpath=directory)
        count = 0
        list_mailers = []
        for message in repo.fetch():
            list_mailers.append(message['data']['From'])
        return list_mailers
