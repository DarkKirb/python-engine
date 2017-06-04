from . import glob
from sdl2.sdl2 import ffi
import logging
gl=glob.gl

class VBO(object):
    def __init__(self, attr, data=None):
        vbo = ffi.new("unsigned int *",0)
        gl.glGenBuffers(1, vbo)
        self.vbo = vbo[0]
        logging.debug("Creating VBO #{}".format(self.vbo))
        self.length=0
        self.attr=attr
        if data is not None:
            self.setData(data)
    def setData(self, data):
        logging.debug("Setting data of VBO #{} to {}".format(self.vbo, repr(data)))
        d = ffi.new("float[]",data)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, ffi.sizeof(d), d, gl.GL_STATIC_DRAW)
        self.length=len(data)//self.attr.width

    def enable(self):
        self.attr.enable()
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glVertexAttribPointer(self.attr.attr, self.attr.width, gl.GL_FLOAT, False, 0, ffi.NULL)
    def disable(self):
        self.attr.disable()

    def __delete__(self):
        logging.debug("Deleting "+repr(self))
        vbo = ffi.new("unsigned int *",self.vbo)
        gl.glDeleteBuffers(1, vbo)
    def __repr__(self):
        return "VBO of size {}*{} for attribute {}".format(self.length, self.attr.width, self.attr.name)

    def __lt__(self, other):
        return self.length < other.length

class Vertex(object):
    def __init__(self, *args, **kwargs):
        self.vbos = list(args)
        self.uniforms = []
        if "uniforms" in kwargs:
            self.uniforms = kwargs["uniforms"]
    def render(self):
        self.vbos[0].attr.program.enable()
        for uniform in self.uniforms:
            uniform.render()
        for vbo in self.vbos:
            vbo.enable()
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, min(self.vbos).length)
        for vbo in self.vbos:
            vbo.disable()
