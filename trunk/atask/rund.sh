#!/bin/bash
if [ $# -eq 1 ] 
then
    if [ "$1" = "--clean" ] 
    then
	dev_appserver.py --clear_datastore --debug atasksd/
    fi
else
    dev_appserver.py --debug atasksd/
fi
