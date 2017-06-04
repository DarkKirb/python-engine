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
from engine import tileset
import logging
import math
sdl=ffi
gl = glob.gl
xrot=0
yrot=0
zrot=0
def init_resources():
    global a_tile, face_tile, tiles, tilemap
    logging.debug("Loading vertex shader")
    vs = shader.Shader("shaders/tile.vs.glsl")
    fs = shader.Shader("shaders/tile.fs.glsl", fragment=True)
    program = shader.Program(vs, fs)
    tiles = tileset.Tileset(program)
    a_tile = tileset.Tile("assets/tiles/A_tile.png",tiles)
    face_tile = tileset.Tile("assets/tiles/badASCIIface.png", tiles)
    tiles.sync()
    tilemap = tileset.TileMap(program, tiles)
    for i in range(10):
        tilemap.setTile(0,i, a_tile)
    for i in range(10):
        tilemap.setTile(i,1, face_tile)
    return True
def logic():
    global zrot
    global yrot
    global xrot
    xrot+=12
    if xrot == 360:
        xrot=0
        yrot+=6
        if yrot == 360:
            yrot = 0
            zrot += 3
            if zrot == 360:
                zrot = 0
    tilemap.rotate(zrot)
    tilemap.rotateY(yrot)
    tilemap.rotateX(xrot)
    tilemap.tick()
def render(window):
    gl.glClearColor(0, 0, 0, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    tilemap.render()
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
