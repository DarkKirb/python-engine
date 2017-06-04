from . import glob
from sdl2.sdl2 import ffi
import logging
import math
gl=glob.gl
mat=[1, 0, 0, 0,
     0, 1, 0, 0,
     0, 0, 1, 0,
     0, 0, 0, 1]
def fixAspect(width, height):
    global mat
    #fovx = 2 * atan(tan(fovy/2) * aspect)
    #tan(fovx/2) = tan(fovy/2) * aspect
    #2*atan(tan(fovx/2)/aspect) = fovy
    aspect = height/width
    fovx = math.pi / 3 #60°
    hfovy = math.atan(math.tan(fovx/2)/aspect)
    logging.debug("Setting vertical FOV to {}°".format((hfovy*2)*(180/math.pi)))
    f = math.tan(hfovy)
    mat[0] = aspect
    mat[5] = 1
    gl.glMatrixMode(gl.GL_PROJECTION)
    matrix = ffi.new("float[]", mat)
    gl.glLoadMatrixf(matrix)
