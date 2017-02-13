import pms
from lights import *

if __name__ == '__main__':
    # Process the mask image
    (center, radius) = findCircleInMask("../psmImages/chrome/chrome.mask.png", debug=False)

    # Calculate light directions of images
    base_dir = '../psmImages'
    light_directions = [ calculateLightDirection(base_dir + '/chrome/chrome.%i.png' % i, center, radius, debug=False) for i in range(12)]

    # Calculate Photometric stereo
    name = 'rock'
    images = [base_dir + '/%s/%s.%i.png' % (name,name,i) for i in range(12)]
    normals = pms.photometricStereo(light_directions, images)

    color = pms.colorizeNormals(normals)
    # mask = pms.getImage(base_dir + '/%s/%s.mask.png' % (name,name))

    plt.imshow(np.rot90(color,3))
    plt.show()