import psp2d
font_path = 'images/font_arial_10_white.png'

def main():
    scr = psp2d.Screen()
    fnt = psp2d.Font(font_path)
    img = psp2d.Image(480, 272)
    img.clear(psp2d.Color(0, 0, 0))
    fnt.drawText(img, 0, 0, 'Hello, world')
    scr.blit(img)
    scr.swap()
    while True:
        pad = psp2d.Controller()
        if pad.circle:
            break


if __name__ == '__main__':
    main()
