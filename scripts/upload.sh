#!/bin/sh

TARGET=""

if [ $# -gt 0 ] ; then
 TARGET=" --repository testpypi "
fi

echo python3 -m twine upload $TARGET dist/*
     python3 -m twine upload $TARGET dist/*

if [ $? -ne 0 ] ; then
 echo "twine upload failed"
 echo "You might want to review your token in ~/.pypirc"
fi
