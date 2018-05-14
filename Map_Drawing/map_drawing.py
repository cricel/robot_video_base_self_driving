#import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

verts = [
    (0., -3.), # left, bottom
    (-1.06, -2.54), # left, top
    (-1.74,-1.47),
    (-2.,0.),
    (-1.87,1.03),
    (-1.,2.59),
    (0.,3.),
    (1.12,2.48),
    (1.87,1.06),
    (2.,0.),
    (1.84,-1.06),
    (1.22,-2.37),
    (0.,-3.)
    ]

codes = [Path.MOVETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.CLOSEPOLY,
         ]

path = Path(verts, codes)

fig = plt.figure()
ax = fig.add_subplot(111)
patch = patches.PathPatch(path, facecolor='orange', lw=2)
ax.add_patch(patch)
ax.set_xlim(-4,4)
ax.set_ylim(-4,4)
plt.show()