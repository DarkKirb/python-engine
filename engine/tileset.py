from renderer import glob
import logging
from renderer import texture
from renderer import vertex
from renderer import attribute
from renderer import frustrum
from PIL import Image
import math
"""This code deals with tilesets. There can be a implementation-defined number of total tilesets.

The size of  a tileset is dynamic and depends on the number of total tiles.
Here is a list of maximum tiles per tileset with a percentage how likely a GPU supports that many tiles and how big the memory usage is when completely filled

  16384 | 100% |   4MB
  65536 |  99% |  16MB
 262144 |  94% |  64MB
1048576 |  89% | 256MB
4194304 |  43% |   1GB

In general, you can say that you can basically just load the entire tileset for your game to the GPU and it will just work™
Also no need to support palettes, they just slow down.
"""
class Tile:
    def __init__(self, fname, tileset):
        self.image = Image.open(fname)
        self.tileset = tileset
        self.tilepos = tileset.addTile(self.image)
    def render(self):
        return self.tileset.render(*self.tilepos)
def pairGenerator(width, height):
    for x in range(width):
        for y in range(height):
            yield x,y

class Tileset:
    def __init__(self, program):
        self.texture = None
        self.im = None
        self.tiles={}
        self.width=0
        self.height=0
        self.program=program
    def addTile(self, tile):
        if self.im is None:
            #Initialize variables here.
            self.im = Image.new("RGBA", (16,16))
            self.im.paste(tile)
            self.width=1
            self.height=1
            self.tiles[(0,0)]=tile
            return 0,0
        found = False
        x,y=0,0
        for x,y in pairGenerator(self.width, self.height):
            if (x,y) not in self.tiles:
                found = True
                break
        if not found:
            self.width+=1
            self.height+=1
            im = Image.new("RGBA", (self.width*16, self.height*16))
            im.paste(self.im)
            self.im=im
            for x,y in pairGenerator(self.width, self.height):
                if (x,y) not in self.tiles:
                    break
        self.im.paste(tile, (x*16, y*16))
        self.tiles[(x,y)] = tile
        return x,y
    def render(self, x, y):
        width = self.width
        w=x+1
        z=y+1
        x/=width
        y/=width
        w/=width
        z/=width

        return [x, y, # Top left
                x, z, # Bottom left
                w, z, # Bottom right
                x, y, # Top left
                w, y, # Top right
                w, z] # Bottom right

    def sync(self):
        """Syncs the texture with the GPU. Has to be called before you can see any tileset differences!"""
        if self.texture is None:
            self.texture = texture.TextureUniform("texture_tileset", self.im, self.program)
        else:
            self.texture.setData(self.im)

class TileMap(object):
    def __init__(self, program, tileset):
        self.program=program
        self.tileset=tileset
        self.scrollX=0.0
        self.scrollY=0.0
        self.rotX=0.0
        self.rotY=0.0
        self.rotZ=0.0
        if not "tilemapUniform" in program.__dict__:
            self.xScroll=attribute.Uniform("xScroll",program)
            self.yScroll=attribute.Uniform("yScroll",program)
            self.xRot=attribute.Uniform("xRot",program)
            self.yRot=attribute.Uniform("yRot",program)
            self.zRot=attribute.Uniform("zRot",program)
            self.Uzoom=attribute.Uniform("zoom",program)
            self.aspect=attribute.Uniform("aspectRatio", program)
            self.aspect.setData(frustrum.mat)
            program.tilemapUniform=[self.xScroll,self.yScroll,self.xRot,self.yRot,self.zRot,self.Uzoom, self.aspect]
        self.zoom=1/12 #1 == the top left tile takes up the entire screen
        self.setZoom(self.zoom)
        self.textureVBO=None
        self.VBO = None
        self.changed=True
        self.tiles={}

    def setXScroll(self, xOff, relative=False):
        if relative:
            self.scrollX+=xOff
        else:
            self.scrollX=xOff
        self.xScroll.setData(self.scrollX)
    def setYScroll(self, yOff, relative=False):
        if relative:
            self.scrollY+=yOff
        else:
            self.scrollY=yOff
        self.yScroll.setData(self.scrollY)
    def rotate(self, angle):
        """Standard rotation"""
        self.rotZ=angle
        self.zRot.setData(angle*math.pi/180)
    def rotateY(self, angle):
        """3D rotation: makes image pan sideways"""
        self.rotY=angle
        self.yRot.setData(angle*math.pi/180)
    def rotateX(self, angle):
        """3D rotation: makes the image pan forwards"""
        self.rotX=angle
        self.xRot.setData(angle*math.pi/180)
    def setZoom(self, factor):
        """ for each n there are 1/n tiles to each direction from the center:
            1 ≜ 2x2
            0.5 ≜ 4x4
        """
        self.zoom=factor
        self.Uzoom.setData(1/factor)
    def render(self):
        if self.textureVBO is None or self.VBO is None:
            logging.warning("Tried to render a unusable tilemap!")
            return
        v = vertex.Vertex(self.textureVBO, self.VBO, uniforms=self.program.tilemapUniform+[self.tileset.texture])
        v.render()
    def tick(self):
        if not self.changed:
            return
        vbo=[]
        textureVBO=[]
        for (x,y),t in self.tiles.items():
            w=x+1
            z=y-1
            vbo += [x, y,
                    x, z,
                    w, z,
                    x, y,
                    w, y,
                    w, z]
            textureVBO+=t.render()
        #Push them to GPU
        if self.textureVBO is None:
            self.textureVBO=vertex.VBO(attribute.Attribute("texture_uv", 2, self.program),textureVBO)
        else:
            self.textureVBO.setData(textureVBO)

        if self.VBO is None:
            self.VBO = vertex.VBO(attribute.Attribute("coord2d", 2, self.program), vbo)
        else:
            self.textureVBO.setData(vbo)
        self.changed=False
    def setTile(self, x, y, tile):
        self.tiles[(x,y)] = tile
        self.changed=True
    def deleteTile(self, x, y):
        del self.tiles[(x,y)]
        self.changed=True
    def clear(self):
        self.tiles={}
        self.changed=True
