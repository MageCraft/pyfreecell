#!/bin/bash
releases_dir=atasksd/releases

version()
{
    bv=$1
    cv=$2
    nv=$3
    if [ -z $nv ]
    then
	exit 1
    else
	new_dir=${releases_dir}/xatasks-$nv
	mkdir -p $new_dir
	touch ${new_dir}/release_note.txt
	sh deployc.sh -v $nv -destdir $new_dir
	if [ $? -eq 0 ]
	then
	    python version.py -u $nv
	fi
    fi
}

versions=$(python version.py -r)
if [ $? -eq 0 ]
then
    version $versions
fi

