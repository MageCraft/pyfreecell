#!/usr/bin/env python
# -*- coding: utf-8 -*-

#努力再努力 * 努 = 优优优优优优

from itertools import izip, count, imap, ifilter
from operator import and_


#oct_(1,2,3) = 123
def oct_(*args):
    sum = 0
    l = list(args)
    l.reverse()
    for i, e in izip(count(), l):
        assert e >= 0
        sum += e * (10 ** i)
    return sum


def test_func(nu,li,zai, you):
    return oct_(nu,li,zai,nu,li) * nu == oct_(you,you,you,you,you,you)

class xlist(list):
    def is_unique(self):
        for i in self:
            if self.count(i) > 1:
                return False
        return True


def main():
    for nu in range(10):
        for li in range(10):
            for zai in range(10):
                for you in range(10):
                    if test_func(nu,li,zai,you) and xlist([nu,li,zai,you]).is_unique():
                        print 'nu=%d, li=%d, zai=%d, you=%d' % (nu,li,zai,you)
                        print '%d%d%d%d%d * %d = %d%d%d%d%d%d' % (nu,li,zai,nu,li, nu, you,you,you,you,you,you)



if __name__ == '__main__':
    assert oct_(3,7,0,3,7) == 37037
    assert test_func(3,7,0,1) 
    main()
