#!/bin/sh

set -e
set -x

pypy/pytest.py
nosetests

if [ "$RUN" = "hosted" ]; then
  ./som.sh -cp Smalltalk TestSuite/TestHarness.som;
elif [ "$RUN" = "translated" ]; then
  pypy/rpython/bin/rpython -O$OPTIMIZE --batch src/targetsomstandalone.py
  ./som -cp Smalltalk TestSuite/TestHarness.som
else
  exit 2
fi
