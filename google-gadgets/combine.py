#!/usr/bin/env python
# -*- coding: utf-8 -*-

template_path = './stock_template.xml'
html_path = './stock.html'
js_path = './stock.js'


def main():
    temp = open(template_path, 'r').read()
    html = open(html_path, 'r').read()
    js = open(js_path, 'r').read()
    output_file = './stock.xml'
    open(output_file, 'w').write( temp % { 'html_content' : html, 'js_content' : js } )


if __name__ == '__main__':
    main()



