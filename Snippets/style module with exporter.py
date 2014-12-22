from  render_freestyle_svg import SVGPathShader, svg_primitive

import xml.etree.cElementTree as et

# without this namespace definition the namespace won't get 
# recognized, leading to unusable results
# this should be put into the addon, not in an external script
#et.register_namespace('', "http://www.w3.org/2000/svg")

with open("test.svg",  "w") as f:
    f.write(svg_primitive.format(960, 540))


from freestyle.chainingiterators import *
from freestyle.functions import *
from freestyle.predicates import *
from freestyle.shaders import *
from freestyle.types import *

from itertools import tee

def tripplewise(iterable):
    """Yields a tuple containing the current object and its immediate neighbors """
    a, b, c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    return zip(a, b, c)

class S(StrokeShader):
    def shade(self, stroke):
        # the StrokeVertex(sv) duplicates the SV, if you don't do this, 
        # blender will crash. 
        initials = [StrokeVertex(sv) for sv in stroke]
        stroke.remove_all_vertices()
        for sv in initials:
            stroke.insert_vertex(sv, stroke.stroke_vertices_end())


Operators.select(QuantitativeInvisibilityUP1D(0))
Operators.bidirectional_chain(ChainSilhouetteIterator(), NotUP1D(QuantitativeInvisibilityUP1D(0)))
## Splits strokes at points of highest 2D curavture 
## when there are too many abrupt turns in it
func = pyInverseCurvature2DAngleF0D()
Operators.recursive_split(func, pyParameterUP0D(0.2, 0.8), NotUP1D(pyHigherNumberOfTurnsUP1D(3, 0.5)), 2)
## Keeps only long enough strokes
Operators.select(pyHigherLengthUP1D(100))
## Sorts so as to draw the longest strokes first
## (this will be done using the causal density)
Operators.sort(pyLengthBP1D())

style = {
    "stroke-opacity":"1.0", 
    "stroke-width":"3.0",
    "stroke": "rgb(112, 50, 160)"
    }

s = SVGPathShader("test", style, "test.svg", 540, False, 0)
shaders_list = [
    #pySamplingShader(50),
    #BezierCurveShader(30),
    ConstantThicknessShader(10),
    ConstantColorShader(0.2, 0.9, 0.2,1.0),
    TipRemoverShader(10),
    s,
    #S(),
    ]

## Use the causal density to avoid cluttering
Operators.create(pyDensityUP1D(8, 0.4, IntegrationType.MEAN), shaders_list)
s.write()

