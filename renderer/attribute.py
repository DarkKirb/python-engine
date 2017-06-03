from . import glob
from sdl2.sdl2 import ffi
import logging
gl=glob.gl

class Attribute(object):
    def __init__(self, name, width, program):
        logging.debug("Creating a new attribute "+name)
        self.attr = gl.glGetAttribLocation(program.program, name.encode("UTF-8"))
        self.width = width
        self.name = name
        self.program=program
    def __repr__(self):
        return self.name

    def enable(self):
        gl.glEnableVertexAttribArray(self.attr)
    def disable(self):
        gl.glDisableVertexAttribArray(self.attr)

class Uniform(object):
    def __init__(self, name, program):
        logging.debug("Creating new uniform "+name)
        self.uniform = gl.glGetUniformLocation(program.program, name.encode("UTF-8"))
        self.data = 0.0
    def setData(self, data):
        self.data = data
    def render(self):
        gl.glUniform1f(self.uniform, self.data)
