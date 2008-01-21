#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

template_path = '../stock_template.xml'
html_path = '../stock.html'
test_path = './test.html'
js_path = '../stock.js'


def main():
    test_html = open(test_path, 'r').read()
    js = open(js_path, 'r').read()
    output_file = './stock_test.html'
    open(output_file, 'w').write( test_html % { 'js_content' : js } )
    

if __name__ == '__main__':
    main()



