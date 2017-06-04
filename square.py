#!/usr/bin/env python3
from sdl2.sdl2 import *
from renderer import glob
glob.gameName="Box"
from renderer import init
from renderer import shader
from renderer import attribute
from renderer import vertex
from renderer import texture
from renderer import frustrum
import logging
import math
sdl=ffi
gl = glob.gl
def init_resources():
    global triangleVertex
    logging.debug("Loading vertex shader")
    vs = shader.Shader("shaders/base.vs.glsl")
    fs = shader.Shader("shaders/base.fs.glsl", fragment=True)
    program = shader.Program(vs, fs)
    attribute_coord2d = attribute.Attribute("coord2d", 2, program)
    trianglevbo = vertex.VBO(attribute_coord2d, [
        -1, 1,
        -1,-1,
         1,-1,
        -1, 1,
         1, 1,
         1,-1
    ])
    textureVBO = texture.TextureVBO(program, [
        0.0, 1.0,
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 1.0,
        1.0, 0.0
    ])
    triangleVertex = texture.Texture("box", "assets/images/OpenGL_Tutorial_Texture.jpg", program, textureVBO, trianglevbo)
    return True
def logic():
    pass
def render(window):
    gl.glClearColor(0, 0, 0, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    triangleVertex.render()
    SDL_GL_SwapWindow(window)
    pass
def main_loop(window):
    while True:
        ev=sdl.new("SDL_Event *")
        while SDL_PollEvent(ev):
            if ev.type == SDL_QUIT:
                return
            if ev.type == SDL_WINDOWEVENT:
                if ev.window.event == SDL_WINDOWEVENT_RESIZED:
                    size = (ev.window.data1, ev.window.data2)
                    gl.glViewport(0, 0, *size)
                    frustrum.fixAspect(*size)
                    gl.glMatrixMode(gl.GL_MODELVIEW)
                    gl.glLoadIdentity()
        logic()
        render(window)
frustrum.fixAspect(640, 480)
init_resources()
main_loop(glob.window)
