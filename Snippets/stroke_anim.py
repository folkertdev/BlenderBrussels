# stroke_anim.py by Tamito Kajiyama
# https://blenderyard.wordpress.com/2014/10/09/under-the-hood-stroke-animation-with-freestyle-for-blender/

from freestyle.types import Operators
from freestyle.utils import getCurrentScene
 
def postprocess(frame_start=None, frame_end=None, interval=0):
    """
    frame_start: the start frame (default Scene.frame_start)
    frame_end: the end frame (default: Scene.frame_end)
    interval: the number of frames inserted as interval between two strokes
    """
 
    totlen = 0.0
    nstrokes = Operators.get_strokes_size()
    #print('#strokes', nstrokes)
    for i in range(nstrokes):
        stroke = Operators.get_stroke_from_index(i)
        totlen += stroke.length_2d
    #print('totlen', totlen)
 
    scene = getCurrentScene()
    sta = scene.frame_start if frame_start is None else frame_start
    end = scene.frame_end if frame_end is None else frame_end
    cur = scene.frame_current
    fac = (cur - sta) / (end - sta)
    #print('fac', fac)
 
    totDrawingFrames = (end - sta + 1) - interval * (nstrokes - 1)
    if totDrawingFrames < 0:
        raise RuntimeError('The number of frames is too small')
 
    lengthPerFrame = totlen / totDrawingFrames
    #print('lengthPerFrame', lengthPerFrame)
 
    thresh = (cur - sta + 1) * lengthPerFrame + 1e-6
    #print('thresh', thresh)
 
    curlen = 0.0
    for i in range(nstrokes):
        stroke = Operators.get_stroke_from_index(i)
        for svert in stroke:
            svert.attribute.visible = curlen + svert.curvilinear_abscissa < thresh
        curlen += stroke.length_2d + lengthPerFrame * interval
    #print('done')