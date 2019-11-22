#!/bin/bash

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

if ! cmp files/tests/config.cfg config.cfg >/dev/null 2>&1
then
	echo "We suggest enable all apis for the tests."
	echo "Another test can be failing for this fact."
	echo "You can edit config.cfg file for it."
else
	echo "Your config.cfg is ok"
fi


python3 git2gender.py https://github.com/davidam/orgguide-es.git --directory="/tmp/clonedir" > files/tests/git2gender1-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/git2gender1.txt files/tests/git2gender1-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "git2gender1 test is failing"
else
	echo "git2gender1 test is ok"
fi

cd files/mbox
wget -c http://mail-archives.apache.org/mod_mbox/httpd-announce/201706.mbox
cd ../..
python3 mail2gender.py http://mail-archives.apache.org/mod_mbox/httpd-announce/ > files/tests/mail2gender-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mail2gender.txt files/tests/mail2gender-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "mail2gender test is failing"
else
	echo "mail2gender test is ok"
fi

# python3 api2gender.py David --api="genderize" > files/tests/api2genderDavidgenderize-$(date "+%Y-%m-%d-%H").txt

# if ! cmp files/tests/api2genderDavidgenderize.txt files/tests/api2genderDavidgenderize-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
# then
# 	echo "api2genderDavidgenderize test is failing"
# else
# 	echo "api2genderDavidgenderize test is ok"
# fi

python3 api2gender.py Leticia --surname="Martin" --api="namsor" > files/tests/api2genderLeticianamsor-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/api2genderLeticianamsor.txt files/tests/api2genderLeticianamsor-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "api2genderLeticianamsor test is failing"
else
	echo "api2genderLeticianamsor test is ok"
fi

python3 api2gender.py Inés --api="genderapi" > files/tests/api2genderInésgenderapi-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/api2genderInésgenderapi.txt files/tests/api2genderInésgenderapi-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "api2genderInésgenderapi test is failing"
else
	echo "api2genderInésgenderapi test is ok"
fi

python3 accuracy.py --api="genderapi" > files/tests/accuracygenderapi-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracygenderapi.txt files/tests/accuracygenderapi-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "accuracygenderapi test is failing"
else
	echo "accuracygenderapi test is ok"
fi

python3 accuracy.py --api="genderapi" --csv="files/names/min.csv" --json="files/names/genderapifiles_names_min.csv.json" > files/tests/accuracyminjsongenderapi-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/accuracyminjsongenderapi.txt files/tests/accuracyminjsongenderapi-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "accuracyminjsongenderapi test is failing"
else
	echo "accuracyminjsongenderapi test is ok"
fi

python3 confusion.py --api="genderapi" > files/tests/confusiongenderapi-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/confusiongenderapi.txt files/tests/confusiongenderapi-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "confusiongenderapi test is failing"
else
	echo "confusiongenderapi test is ok"
fi

# python3 confusion.py --api="genderize" > files/tests/confusiongenderize-$(date "+%Y-%m-%d-%H").txt

# if ! cmp files/tests/confusiongenderize.txt files/tests/confusiongenderize-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
# then
# 	echo "confusiongenderize test is failing"
# else
# 	echo "confusiongenderize test is ok"
# fi



rm -rf /tmp/clonedir
echo "cleaning temporary files"
rm files/tests/*$(date "+%Y")*.txt
