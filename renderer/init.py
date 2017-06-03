from . import glob
from sdl2.sdl2 import *
from sdl2.gl import GL
import logging
import warnings
logging.basicConfig(level=logging.DEBUG)
warnings.simplefilter("always")
logging.captureWarnings(True)
def main():
    logging.debug("Starting the engine")
    SDL_Init(SDL_INIT_VIDEO)
    name=glob.gameName
    if isinstance(name, str):
        name=name.encode("UTF-8")
    window = SDL_CreateWindow(name, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 640, 480, SDL_WINDOW_RESIZABLE | SDL_WINDOW_OPENGL)
    SDL_GL_SetAttribute(SDL_GL_ALPHA_SIZE, 1)
    SDL_GL_CreateContext(window)
    gl=GL(2.0)
    glob.gl=gl
    glob.window=window
    logging.debug("Finished initializing")
main()
