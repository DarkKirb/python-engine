#!/usr/bin/env python3
from sdl2.sdl2 import *
from renderer import glob
glob.gameName="Triangle"
from renderer import init
from renderer import shader
from renderer import attribute
from renderer import vertex
from renderer import texture
import logging
import math
sdl=ffi
gl = glob.gl
def init_resources():
    global triangleVertex
    global triangleUniform
    logging.debug("Loading vertex shader")
    vs = shader.Shader("shaders/triangle.vs.glsl")
    fs = shader.Shader("shaders/triangle.fs.glsl", fragment=True)
    program = shader.Program(vs, fs)
    attribute_coord2d = attribute.Attribute("coord2d", 2, program)
    trianglevbo = vertex.VBO(attribute_coord2d, [
         0.0, 0.8,
        -0.8,-0.8,
         0.8,-0.8
    ])
    textureVBO = texture.TextureVBO(program, [
        0.0, 1.0,
        0.0, 0.0,
        1.0, 0.0
    ])
    triangleUniform = attribute.Uniform("fade", program)
    triangleUniform.setData(0.1)
    triangleVertex = texture.Texture("box", "assets/images/OpenGL_Tutorial_Texture.jpg", program, textureVBO, trianglevbo, uniforms=[triangleUniform])
    return True
def logic():
    global triangleUniform
    triangleUniform.setData(math.sin(SDL_GetTicks() / 1000 * (2*math.pi) / 5) / 2 + 0.5)
def render(window):
    gl.glClearColor(1.0, 1.0, 1.0, 1.0)
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
        logic()
        render(window)
init_resources()
main_loop(glob.window)
