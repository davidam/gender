#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
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
"""Simple command-line example for Custom Search.

Command-line application that does a search.
"""

__author__ = 'davidam@gnu.org (David Arroyo Menéndez)'

import pprint
import argparse
from app.dame_customsearch import DameCustomsearch

# from googleapiclient.discovery import build

parser = argparse.ArgumentParser()
parser.add_argument('name', help="Name to be detected")
args = parser.parse_args()


def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  g = DameCustomsearch()
  d = g.get(args.name, binary=True)
  print("Google results of %s as male: %s" % (args.name, d["rmale"]))
  print("Google results of %s as female: %s" % (args.name, d["rfemale"]))

if __name__ == '__main__':
  main()
