from __future__ import print_function

import sys
import os
from copy import copy
from itertools import product

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add parent directory into sys.path
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

from generate import generateImages
import pms
import mesh


def setup_images(func):
    def inner(template, lights):
        images, lightning_file = generateImages(template, lights)
        file_prefix = template.rsplit(".", 1)[0]
        try:
            func(images, lightning_file, file_prefix)
        finally:
            pass
            #for image in images:
            #    os.remove(image)
            #os.remove(lightning_file)
    return inner

@setup_images
def doTestAndComparePMS(images, lightning_file, file_prefix):
    normals = pms.photometricStereo(lightning_file, images)

    color = pms.colorizeNormals(normals)
    plt.imsave('{}-normals.png'.format(file_prefix), color)
    mesh.write3dNormals(normals, '{}-3dn.stl'.format(file_prefix))


@setup_images
def doTestAndComparePMSwL(images, lightning_file, file_prefix):
    normals = pms.photometricStereoWithoutLightning(images)

    color = pms.colorizeNormals(normals)
    plt.imsave('{}-normals.png'.format(file_prefix), color)
    mesh.write3dNormals(normals, '{}-3dn.stl'.format(file_prefix))
    surface = mesh.surfaceFromNormals(normals)
    mesh.writeMesh(surface, normals, '{}-mesh.stl'.format(file_prefix))


lights = (
    (30, 60),
    (-80, -60, -15, 0, 15, 60, 80),
    (-80, -60, -15, 0, 15, 60, 80),
)
light_positions = list(product(*lights))


def test_sphere():
   doTestAndComparePMS("sphere.pov.tmpl", light_positions)
#     doTestAndComparePMSwL("sphere.pov.tmpl", light_positions)

def test_cube_front():
   doTestAndComparePMS("cube_front.pov.tmpl", light_positions)
#    doTestAndComparePMSwL("cube_front.pov.tmpl", light_positions)

def test_cube_angled():
   doTestAndComparePMS("cube_angled.pov.tmpl", light_positions)
#    doTestAndComparePMSwL("cube_angled.pov.tmpl", light_positions)


if __name__ == '__main__':
    funcs = list(globals().keys())
    for func in funcs:
        try:
            func_name = globals()[func].__name__
        except AttributeError:
            continue
        if not func_name.startswith('test'):
            continue
        print("Executing", func_name)
        globals()[func]()