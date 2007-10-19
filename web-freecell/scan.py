#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Image

W,H = 71,96
TRANS_COLOR=0
fn_format="card_%d.gif" 

trans_border_pts = ((0,0), (1,0), (0,1),
                    (W-1,0), (W-2,0), (W-1,1),
                    (W-1,H-1), (W-2,H-1), (W-1,H-2),
                    (0,H-1), (1,H-1), (0,H-2),
                    )

def split_save(fn, output_dir, max_count=54, trans_border=True):
    im = Image.open(fn)
    big_w, big_h = im.size
    col = big_w / W
    row = big_h / H
    assert col == 14
    assert row == 4
    count = 0
    for c in range(col):
        for r in range(row):
            count += 1
            if count > max_count:
                break;
            rect = (W*c, H*r, W*c+W, H*r+H)
            im1 = im.crop(rect)
            #print im1.size
            if trans_border:
                for pt in trans_border_pts:
                    im1.putpixel(pt, TRANS_COLOR)
            output_fn = output_dir + "/" + fn_format % count
            im1.save(output_fn, transparency=TRANS_COLOR)


def scan(fn):
    im = Image.open(fn)
    w,h = im.size
    colors = []
    for i in range(w):
        for j in range(h):
            c = im.getpixel((i,j))
            if colors.count(c) == 0:
                colors.append(c)
    colors.sort()
    print colors

if __name__ == "__main__":
    #scan("cards.bmp")
    split_save("cards.bmp", "cards")

    
        
    

