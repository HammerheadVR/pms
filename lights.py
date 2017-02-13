import pms
import math

import matplotlib
# matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

from skimage import data
from skimage.filters import threshold_otsu, threshold_adaptive
from skimage.color import rgb2gray
from skimage.measure import moments

# Calculate light direction based on sphere
def calculateLightDirection(image_location, radius, threshold = 0.95, show = True):
    # Threshold the image
    im = pms.imread(image_location)
    im_gray = rgb2gray(im)

    # global_thresh = threshold_otsu(im_gray)
    im_gray_thresh = im_gray > threshold

    if show:
        plt.imshow(im_gray_thresh, cmap='gray')
        plt.show()

    # Cut out bounding box
    im_gray_thresh_box = im_gray_thresh
    # im_gray_thresh_box = im_gray_thresh[x1:x2, y1:y2]

    # Calculate center of pixels (hopefully only the highlight)
    m = moments(im_gray_thresh_box.astype(float), order=1)
    center = {'x': m[1, 0] / m[0, 0], 'y': m[0, 1] / m[0, 0]}

    if show:
        plt.scatter(center['x'], center['y'])

    # Calculate XYZ and return
    x = (center['x'] - radius) / radius
    y = (center['y'] - radius) / radius
    z = math.sqrt(1.0 - pow(x, 2.0) - pow(y, 2.0))

    return (x,y,z)

if __name__ == '__main__':
    print(calculateLightDirection("../psmImages/chrome/chrome.0.png", 200))