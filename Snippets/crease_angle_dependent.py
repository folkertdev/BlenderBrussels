# code by Tamito Kajiyama
# https://freestyleintegration.wordpress.com/2014/04/09/experimental-variable-line-thickness-shaders/

from freestyle.chainingiterators import *
from freestyle.predicates import *
from freestyle.shaders import *
from freestyle.types import Operators
import math
 
class CreaseAngleDependentThicknessShader(StrokeShader):
    def __init__(self, angle1, angle2, thickness1, thickness2):
        StrokeShader.__init__(self)
        self.__a1 = angle1
        self.__a2 = angle2
        self.__t1 = thickness1
        self.__t2 = thickness2
 
    def shade(self, stroke):
        delta_a = self.__a2 - self.__a1
        delta_t = self.__t2 - self.__t1
        fac = 1 / delta_a
        for v in stroke:
            fe = v.first_svertex.get_fedge(v.second_svertex)
            if not fe.is_smooth:
                angle = math.degrees(math.acos(-fe.normal_left.dot(fe.normal_right)))
                if angle < self.__a1:
                    t = self.__t1
                elif angle > self.__a2:
                    t = self.__t2
                else:
                    t = self.__t1 + delta_t * (angle - self.__a1) * fac
                #print(angle, t)
                v.attribute.thickness = (t/2, t/2)
 
upred = AndUP1D(QuantitativeInvisibilityUP1D(0), pyNatureUP1D(Nature.CREASE))
Operators.select(upred)
Operators.bidirectional_chain(ChainSilhouetteIterator(), NotUP1D(upred))
shaders_list = [
    SamplingShader(5.0),
    CreaseAngleDependentThicknessShader(70, 120, 5, 0),
    ConstantColorShader(0, 0, 0),
    ]
Operators.create(TrueUP1D(), shaders_list)