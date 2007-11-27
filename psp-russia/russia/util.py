#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG = True

def log(*arg_list):
    if DEBUG:
        print " ".join(map(str, arg_list))
