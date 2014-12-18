# pixelate.py by Tamito Kajiyama
# https://blenderyard.wordpress.com/2014/11/02/pixelating-freestyle-lines/
 
from freestyle.types import *
from freestyle.chainingiterators import *
from freestyle.predicates import *
from freestyle.shaders import *
from freestyle.utils import *
import bpy
import os
 
# full path to ImageMagick's "convert" command
CONVERT_COMMAND = r'C:\home\kajiyama\bin\convert.exe'
 
alpha = 0 # set to 1 for preview render
upred = QuantitativeInvisibilityUP1D(0)
Operators.select(upred)
Operators.bidirectional_chain(ChainSilhouetteIterator(), NotUP1D(upred))
shaders_list = [
    ConstantThicknessShader(1),
    ConstantColorShader(0, 0, 0, alpha),
    ]
Operators.create(TrueUP1D(), shaders_list)
 
# Based on the implementation of Bresenham's line drawing algorithm
# by Steve Cunningham and Tim Worsham, October 1988, CSU Stanislaus
# http://www.cs.csustan.edu/~rsc/SDSU/Interpolation.pdf
def line(x1, y1, x2, y2):
    pixels = []
    bx = x1
    by = y1
    dx = x2 - x1
    dy = y2 - y1
    if dy == 0: # horizontal line
        pixels.append((bx, by))
        xsign = -1 if dx < 0 else 1
        while bx != x2:
            bx += xsign
            pixels.append((bx, by))
    elif dx == 0: # vertical line
        pixels.append((bx, by))
        ysign = -1 if dy < 0 else 1
        while by != y2:
            by += ysign
            pixels.append((bx, by))
    else: # Bresenham's line drawing algorithm
        pixels.append((bx, by))
        xsign = -1 if dx < 0 else 1
        ysign = -1 if dy < 0 else 1
        dx = abs(dx)
        dy = abs(dy)
        if dx < dy: # the line is more vertical than horizontal
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx - dy)
            while by != y2:
                by += ysign
                if p < 0:
                    p += const1
                else:
                    p += const2
                    bx += xsign
                pixels.append((bx, by))
        else: # the line is more horizontal than vertical
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy - dx)
            while bx != x2:
                bx += xsign
                if p < 0:
                    p += const1
                else:
                    p += const2
                    by += ysign
                pixels.append((bx, by))
    return pixels
 
scene = getCurrentScene()
w = scene.render.resolution_x * scene.render.resolution_percentage / 100
h = scene.render.resolution_y * scene.render.resolution_percentage / 100
 
# write pixels as a set of drawing instructions in the Magick Vector Graphics (MVG) format
# http://www.imagemagick.org/script/magick-vector-graphics.php
pixels = []
nstrokes = Operators.get_strokes_size()
for i in range(nstrokes):
    stroke = Operators.get_stroke_from_index(i)
    points = [(int(svert.point.x), (h-1)-int(svert.point.y)) for svert in stroke]
    prev = points.pop(0)
    for curr in points:
        pixels.extend(line(prev[0], prev[1], curr[0], curr[1]))
        prev = curr
mvg_filename = bpy.path.abspath(scene.render.filepath + "%04d_line.mvg" % scene.frame_current)
with open(mvg_filename, 'wt') as mvg:
    for x, y in pixels:
        mvg.write("point %d,%d\n" % (x, y))
print('Wrote', mvg_filename)
 
# render the pixels using the ImageMagick convert command
png_filename = bpy.path.abspath(scene.render.filepath + "%04d_line.png" % scene.frame_current)
cmd = '%s -size %dx%d -background none "%s" "%s"' % (CONVERT_COMMAND, w, h, mvg_filename,png_filename)
#print(cmd)
os.system(cmd)
print('Wrote', png_filename)