#!/bin/bash
version()
{
    bv=$1
    cv=$2
    nv=$3
    if [ -z $nv ]
    then
	exit 1
    else
	sh deployc.sh -v $nv -destdir atasksd/media
    fi
}

versions=$(python version.py -r)
if [ $? -eq 0 ]
then
    version $versions
fi

