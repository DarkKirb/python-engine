from . import glob
from sdl2.sdl2 import ffi
import logging
from PIL import Image
import numpy as np
from . import attribute
from . import vertex
from . import frustrum
gl = glob.gl

class TextureUniform(attribute.Uniform):
    def __init__(self, name, fname, program):
        logging.debug("Creating new texture")
        texture = ffi.new("unsigned int *",0)
        gl.glGenTextures(1, texture)
        texture = texture[0]
        self.texture = texture
        super().__init__(name, program)
        self.setData(fname)
    def setData(self, fname):
        logging.debug("Loading new texture #{}".format(self.texture))
        im = Image.open(fname).rotate(180).transpose(Image.FLIP_LEFT_RIGHT).convert("RGBA")
        data = np.asarray(im).flatten()
        cdata = ffi.cast("uint8_t *", data.ctypes.data)
        logging.debug("Copying texture #{} to the GPU".format(self.texture))

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D,
                      0,
                      gl.GL_RGBA,
                      im.size[0],
                      im.size[1],
                      0,
                      gl.GL_RGBA,
                      gl.GL_UNSIGNED_BYTE,
                      cdata)
        super().setData(0)
    def render(self):
        gl.glActiveTexture(gl.GL_TEXTURE0)
        super().render()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
    def __del__(self):
        texture = ffi.new("unsigned int *",self.texture)
        gl.glDeleteTextures(1, texture)


class TextureVBO(vertex.VBO):
    def __init__(self, program, data=None):
        if not "textureCoord" in program.__dict__:
            program.textureCoord = attribute.Attribute("texcoord", 2, program)
        super().__init__(program.textureCoord, data)

class Texture(vertex.Vertex):
    def __init__(self, name, fname, program, *args, **kwargs):
        aspect = attribute.Uniform("aspectRatio", program)
        aspect.setData(frustrum.mat)
        uniforms = [TextureUniform("texture_"+name, fname, program),
                    aspect]
        if "uniforms" in kwargs:
            uniforms += kwargs["uniforms"]
        super().__init__(*args, uniforms=uniforms)

