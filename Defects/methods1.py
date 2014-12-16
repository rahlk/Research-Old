from table import *
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from dtree import *

def newTable(tbl, headerLabel, Rows):
 tbl2 = clone(tbl)
 newHead = Sym()
 newHead.col = len(tbl.headers)
 newHead.name = headerLabel
 tbl2.headers = tbl.headers + [newHead]
 return clone(tbl2, rows = Rows)

def drop(test, tree):
 loc = apex(test, tree)
 return loc

def saveImg(x, num_bins):
 n, bins, patches = plt.hist(x, num_bins, normed = False,
                             facecolor = 'blue', alpha = 0.5)
 # add a 'best fit' line
 plt.xlabel('Bugs')
 plt.ylabel('Frequency')
 plt.title(r'Histogram (Median Bugs in each class)')

 # Tweak spacing to prevent clipping of ylabel
 plt.subplots_adjust(left = 0.15)
 plt.savefig('./_fig/hist.jpg')
 plt.close()