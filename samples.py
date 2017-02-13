import pms
from lights import *

if __name__ == '__main__':
    # Process the mask image
    (center, radius) = findCircleInMask("../psmImages/chrome/chrome.mask.png", True)

    # Calculate light directions of images
    base_dir = '../psmImages'
    light_directions = [ calculateLightDirection(base_dir + '/chrome/chrome.%i.png' % i, center, radius) for i in range(12)]

    # Calculate Photometric stereo