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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from app.dame_gender import Gender
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--csv')
args = parser.parse_args()

g = Gender()

if (args.csv == 'nocategorical'):
    g.features_list_no_categorical("files/names/all.csv")
    g.features_list2csv(csv="nocategorical")
    data = pd.read_csv('files/features_list_no_cat.csv', index_col=0)
elif (args.csv == 'categorical'):
    g.features_list_categorical("files/names/all.csv")
    g.features_list2csv(csv="categorical")
    data = pd.read_csv('files/features_list_cat.csv', index_col=0)
else:
    g.features_list2csv("files/names/all.csv")
    data = pd.read_csv('files/features_list.csv', index_col=0)

#data = pd.read_csv('files/features_list_cat.csv', index_col=0)
#data = pd.read_csv('files/features_list.csv', index_col=0)
corr = data.corr()
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(corr,cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,len(data.columns),1)
ax.set_xticks(ticks)
plt.xticks(rotation=90)
ax.set_yticks(ticks)
ax.set_xticklabels(data.columns)
ax.set_yticklabels(data.columns)
plt.show()
