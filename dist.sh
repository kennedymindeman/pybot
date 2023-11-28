#!/bin/bash

if [ -z "$1" ]; then
	VERSION=
else
	VERSION="-$1"
fi

pushd `dirname $0`

rm -f *.pyc bots/*.pyc pybots*.bz2 pybots*.zip run.log
find . -type d -exec chmod 0750 \{\} \;
find . -type f -exec chmod 0640 \{\} \;
find . -type f -name '*.py*' -exec chmod 0750 \{\} \;
find . -type f -name '*.sh*' -exec chmod 0750 \{\} \;

mkdir -p pybots
for f in `ls *.py`; do
	sed 's/\t/ /g' < $f > pybots/$f
done
cp -r bots pybots
zip -r pybots_symbian.zip pybots
rm -rf pybots

mkdir -p pybots
cp *.py *.sh README LICENSE *.bat pybots
cp -r sl4a pybots
cp -r bots pybots
tar jcvf pybots$VERSION.tar.bz2 pybots
rm -rf pybots

popd

