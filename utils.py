# origin must be one of ['tl', 'tr', 'bl', 'br'] (top/bottom left/right)
def get_image_region(img, startx, starty, endx, endy, origin):
    h,w = img.shape[:2]
    origin = list(origin)
    startx = (w - startx) if origin[1] != "l" else startx
    starty = (h - starty) if origin[0] != "t" else starty

    endx = (w - endx) if origin[1] != "l" else endx
    endy = (h - endy) if origin[0] != "t" else endy
    print((startx, starty))
    print((endx, endy))
    return img[starty:endy, startx:endx]

