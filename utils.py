import matplotlib.pyplot as plt         # to draw skimages
import os                               # to get list of files in a directory
import matplotlib.patches as patches    # to draw bounding boxes on images
import skimage.io as io                 # to import mask image
import math                             # calculate mask transform
import cv2                              # efficiently overlay one image onto another
import numpy as np                      # matrix math for image overlay

# util function to apply correction to coordinates 
# (if (0,0) is not the top left corner), and extract image patch.
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

# helper function to display a single image:
def display_im(img, title="images"):
    plt.imshow(img, cmap="gray")
    plt.title(title)
    plt.tight_layout()
    plt.show()

# helper function to draw an image with a bounding boxes drawn on top:
def drawImageWithBoundingBox(image, boxCoords, boxDims, pltTitle="image"):
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    x, y = boxCoords
    w, h = boxDims
    rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor="r", facecolor="none")

    ax.add_patch(rect)
    plt.title(pltTitle)
    plt.show()

    return fig

# helper function to get all filepaths in a directory
def getFileNames(mypath):
    flist = []
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        flist.extend(filenames)
        break
    print(f'GOT ALL FILENAMES IN {mypath}:\n{flist}')
    return [mypath+f for f in flist]

if __name__=='__main__':
    getFileNames()

def get_x_y_distances(landmarks):
    x=int(math.dist(landmarks[0], landmarks[1]))
    y=int(math.dist(((landmarks[0][0]+landmarks[1][0])//2 , (landmarks[0][1]+landmarks[1][1])//2 ), landmarks[2]))
    return x,y

def drawBoundingBoxes(frame, landmarks):
    colors=[(255,0,0),(0,255,0),(0,0,255)]
    # print(f'Bounding boxes: landmarks are {",".join(map(str, landmarks))}')
    for pos,color in zip(landmarks, colors):
        x,y=pos
        offset = globals.SQUARE_SIDE
        bottom_right = (x+offset, y+offset)
        cv2.rectangle(frame, (x,y), bottom_right,color, 2)
    return frame

def rotate_image(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]
    if center is None:
        center = (w / 2, h / 2)
    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated