from . import glob
from sdl2.sdl2 import ffi
import logging
gl=glob.gl
class ShaderCompileError(Exception):
    def __init__(self, shader):
        length=ffi.new("int *")
        gl.glGetShaderiv(shader, gl.GL_INFO_LOG_LENGTH, length)
        buf1 = ffi.new("char["+str(length[0])+"]")
        gl.glGetShaderInfoLog(shader, length[0], ffi.NULL, buf1)
        super().__init__(ffi.string(buf1).decode("UTF-8"))
class ProgramLinkError(Exception):
    def __init__(self, program):
        length = ffi.new("int *")
        gl.glGetProgramiv(program, gl.GL_INFO_LOG_LENGTH, length)
        buf1 = ffi.new("char["+str(length[0])+"]")
        gl.glGetProgramInfoLog(program, length[0], ffi.NULL, buf1)
        super().__init__(ffi.string(buf1).decode("UTF-8"))
class Shader(object):
    def __init__(self, fname, fragment=False):
        logging.debug("Loading shader {}".format(fname))
        with open(fname, "rb") as f:
            self.code = f.read()
        logging.debug("Compiling shader {}".format(fname))
        if fragment:
            self.shader=gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        else:
            self.shader=gl.glCreateShader(gl.GL_VERTEX_SHADER)
        self.fragment=fragment
        compileOK=ffi.new("int *",0)
        source = ffi.new("char[]",self.code)
        source2 = ffi.new("char **", source)
        gl.glShaderSource(self.shader, 1, source2, ffi.NULL)
        gl.glCompileShader(self.shader)
        gl.glGetShaderiv(self.shader, gl.GL_COMPILE_STATUS, compileOK)
        if not compileOK[0]:
            raise ShaderCompileError(self.shader)
        logging.debug("Compiled {}".format(fname))
    def __repr__(self):
        return ("Fragment" if self.fragment else "Vertex")+" Shader #"+str(self.shader)

class Program(object):
    def __init__(self, *args):
        logging.debug("Linking {}".format(repr(args)))
        self.program = gl.glCreateProgram()
        for shader in args:
            gl.glAttachShader(self.program, shader.shader)
        gl.glLinkProgram(self.program)
        linkOK=ffi.new("int *", 0)
        gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS, linkOK)
        if not linkOK[0]:
            raise ProgramLinkError(self.program)
        logging.debug("Linked {}".format(repr(args)))
    def enable(self):
        gl.glUseProgram(self.program)
    def __del__(self):
        logging.debug("Deleting Program #{}".format(self.program))
        gl.glDeleteProgram(self.program)
