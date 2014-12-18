# code by Tamito Kajiyama
# https://freestyleintegration.wordpress.com/2014/04/09/experimental-variable-line-thickness-shaders/


from freestyle.chainingiterators import *
from freestyle.predicates import *
from freestyle.shaders import *
from freestyle.types import Operators
import math
 
class VariableContourThicknessShader(StrokeShader):
    def __init__(self, Kr1, Kr2, thickness1, thickness2):
        StrokeShader.__init__(self)
        self.__k1 = Kr1
        self.__k2 = Kr2
        self.__t1 = thickness1
        self.__t2 = thickness2
 
    def shade(self, stroke):
        delta_k = self.__k2 - self.__k1
        delta_t = self.__t2 - self.__t1
        fac = 1 / delta_k
        for v in stroke:
            c1 = v.first_svertex.curvatures
            c2 = v.second_svertex.curvatures
            if c1 is None and c2 is None:
                v.attribute.thickness = (0, 0)
                continue
            if c1 is None:
                Kr = abs(c2[4])
            elif c2 is None:
                Kr = abs(c1[4])
            else:
                Kr = abs(c1[4]) + v.t2d * (abs(c2[4]) - abs(c1[4]))
            if Kr < self.__k1:
                t = self.__t1
            elif Kr > self.__k2:
                t = self.__t2
            else:
                t = self.__t1 + delta_t * (Kr - self.__k1) * fac
            #print(Kr, t)
            v.attribute.thickness = (t/2, t/2)
 
upred = QuantitativeInvisibilityUP1D(0)
Operators.select(upred)
Operators.bidirectional_chain(ChainSilhouetteIterator(), NotUP1D(upred))
shaders_list = [
    #SamplingShader(1),
    VariableContourThicknessShader(0.001, 0.01, 0, 10),
    ConstantColorShader(1, 0, 0),
    ]
Operators.create(TrueUP1D(), shaders_list)