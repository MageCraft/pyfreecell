#!/bin/env python
import os
import os.path
from xml.dom.minidom import *
import sys

cur_dir=os.getcwd()
atasksd_dir=os.path.join(cur_dir, 'atasksd')
version_file=os.path.join(atasksd_dir, 'version.xml')

def read_version():
    f = open(version_file)
    dom = parse(f)
    root = dom.documentElement
    bvNode = root.getElementsByTagName('base_version')[0]
    cvNode = root.getElementsByTagName('current_version')[0]
    bv = bvNode.firstChild.data
    cv = cvNode.firstChild.data
    #print "base version is " + bv
    #print "current version is " + cv
    nv=None
    if cv.startswith(bv):
        v1=cv[len(bv):]
        v2=str(int(v1)+1)
        nv=bv+v2
    else:
        nv=bv+'1'
    #print 'new version is ' + nv
    return bv, cv, nv

def update_version(nv):
    f = open(version_file)
    dom = parse(f)
    root = dom.documentElement
    bvNode = root.getElementsByTagName('base_version')[0]
    cvNode = root.getElementsByTagName('current_version')[0]
    bv = bvNode.firstChild.data
    cv = cvNode.firstChild.data
    cvNode.firstChild.data = nv
    f.close()
    f1 = open(version_file, 'w')
    f1.write(dom.toxml())
    f1.close()


def main():
    pass

def usage():
    print 'usage:'
    print '%s [-r|-u new_vesion]' %  (sys.argv[0],)


if __name__ == '__main__':
    if len(sys.argv)  == 1:
        usage()
        sys.exit(1)

    opt = sys.argv[1]
    if opt == '-r':
        bv, cv, nv = read_version()
        print bv,cv,nv
    elif opt == '-u':
        if len(sys.argv) != 3:
            usage()
            sys.exit(1)
        nv = sys.argv[2]
        update_version(nv)
    else:
        print 'error'

