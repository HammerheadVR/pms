import pms
import math
from operator import sub

import matplotlib
# matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

from skimage import data
from skimage.filters import threshold_otsu, threshold_adaptive
from skimage.color import rgb2gray
from skimage.measure import moments
from skimage.feature import canny

import numpy as np

def centroid(im):
    m = moments(im.astype(float), order=1)
    return (m[1, 0] / m[0, 0], m[0, 1] / m[0, 0]) # (x,y)

# Calculate light direction based on sphere
# bounding_box: [x,y,width,height]
def calculateLightDirection(image_location, center, radius, threshold = 0.95, show = False):
    # Threshold the image
    im = pms.imread(image_location)
    im_gray = rgb2gray(im)

    # global_thresh = threshold_otsu(im_gray)
    im_gray_thresh = im_gray > threshold

    # Cut out bounding box
    im_gray_thresh_box = im_gray_thresh

    if show:
        plt.imshow(im_gray_thresh_box, cmap='gray')
        plt.show()

    # Calculate center of pixels (hopefully only the highlight)
    specular_center = centroid(im_gray_thresh_box)

    if show:
        plt.scatter(specular_center[0], specular_center[1])
        plt.scatter(center[0], center[1])

    # Calculate XYZ and return
    x = (specular_center[0] - center[0]) / radius
    y = (specular_center[1] - center[1]) / radius
    z = math.sqrt(1.0 - pow(x, 2.0) - pow(y, 2.0)) # Equation of a sphere is x^2 + y^2 = 1

    return (x,y,z)

if __name__ == '__main__':
    # Load mask image
    im = pms.imread("../psmImages/chrome/chrome.mask.png")
    im_gray = rgb2gray(im)

    # Calculate centroid
    center = centroid(im_gray)

    # Calculate edge image
    edges = canny(im_gray)
    edge_pixels = np.transpose(np.nonzero(edges))

    radii = map(lambda x: np.linalg.norm(map(sub, x, center)), edge_pixels)
    radius = np.mean(radii)

    print(calculateLightDirection("../psmImages/chrome/chrome.0.png", center, radius, 0.95, True))