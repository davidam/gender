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



python3 main.py "Jesús" --total=genderguesser > files/tests/mainjesusgenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainjesusgenderguesser.txt files/tests/mainjesusgenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "mainjesusgenderguesser test is failing"
else
	echo "mainjesusgenderguesser test is ok"
fi

python3 main.py "Sara" --total=genderguesser > files/tests/mainsaragenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainsaragenderguesser.txt files/tests/mainsaragenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "mainsaragenderguesser test is failing"
else
	echo "mainsaragenderguesser test is ok"
fi

python3 main.py sara --total=genderguesser > files/tests/mainsara2genderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainsaragenderguesser.txt files/tests/mainsara2genderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "mainsara2genderguesser test is failing"
else
	echo "mainsara2genderguesser test is ok"
fi


python3 main.py silla --ml=xgboost > files/tests/mainsilla-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/mainsilla.txt files/tests/mainsilla-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
    echo "mainsilla test is failing"
else
    echo "mainsilla test is ok"
fi

python3 main.py casa --ml=forest > files/tests/maincasa-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/maincasa.txt files/tests/maincasa-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
    echo "maincasa test is failing"
else
    echo "maincasa test is ok"
fi

python3 api2gender.py David --api="genderguesser" > files/tests/api2genderDavidgenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/api2genderDavidgenderguesser.txt files/tests/api2genderDavidgenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "api2genderDavidgenderguesser test is failing"
else
	echo "api2genderDavidgenderguesser test is ok"
fi

python3 accuracy.py --csv=files/names/min.csv > files/tests/accuracymin-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracymin.txt files/tests/accuracymin-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "accuracymin test is failing"
else
	echo "accuracymin test is ok"
fi

python3 accuracy.py --api="genderguesser" --csv=files/names/min.csv > files/tests/accuracygenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracygenderguesser.txt files/tests/accuracygenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "accuracygenderguesser test is failing"
else
	echo "accuracygenderguesser test is ok"
fi

python3 accuracy.py --api="genderguesser" --measure="precision" --csv=files/names/partialnoundefined.csv > files/tests/accuracypartialprecisiongenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracypartialprecisiongenderguesser.txt files/tests/accuracypartialprecisiongenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "accuracypartialprecisiongenderguesser test is failing"
else
	echo "accuracypartialprecisiongenderguesser test is ok"
fi

python3 accuracy.py --api="genderguesser" --measure="f1score" --csv=files/names/partialnoundefined.csv > files/tests/accuracypartialf1scoregenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracypartialf1scoregenderguesser.txt files/tests/accuracypartialf1scoregenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "accuracypartialf1scoregenderguesser test is failing"
else
	echo "accuracypartialf1scoregenderguesser test is ok"
fi

python3 accuracy.py --api="genderguesser" --measure="recall" --csv=files/names/partialnoundefined.csv > files/tests/accuracypartialrecallgenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracypartialrecallgenderguesser.txt files/tests/accuracypartialrecallgenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "accuracypartialrecallgenderguesser test is failing"
else
	echo "accuracypartialrecallgenderguesser test is ok"
fi


python3 accuracy.py --api="damegender" --csv=files/names/partial.csv > files/tests/accuracypartialdamegender-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracypartialdamegender.txt files/tests/accuracypartialdamegender-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "accuracypartialdamegender test is failing"
else
	echo "accuracypartialdamegender test is ok"
fi


python3 confusion.py --api="damegender" --dimensions=2x3 --csv=files/names/min.csv > files/tests/confusiondamegender-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/confusiondamegender.txt files/tests/confusiondamegender-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "confusiondamegender test is failing"
else
	echo "confusiondamegender test is ok"
fi

python3 confusion.py --api="genderguesser" --dimensions=2x3 --csv=files/names/min.csv > files/tests/confusiongenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/confusiongenderguesser.txt files/tests/confusiongenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "confusiongenderguesser test is failing"
else
	echo "confusiongenderguesser test is ok"
fi

python3 errors.py --csv="files/names/partial.csv" > files/tests/errorspartial-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/errorspartial.txt files/tests/errorspartial-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
    echo "errorspartial test is failing"
else
    echo "errorspartial test is ok"
fi

python3 errors.py --csv="files/names/partial.csv" --api="genderguesser" > files/tests/errorsgenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/errorsgenderguesser.txt files/tests/errorsgenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "errorsgenderguesser test is failing"
else
	echo "errorsgenderguesser test is ok"
fi

rm -rf /tmp/clonedir
echo "cleaning temporary files"
rm files/tests/*$(date "+%Y")*.txt

