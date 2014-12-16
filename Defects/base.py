import sys, os
sys.path.append(os.environ['HOME']+'/git/axe/axe')
from abcd import _runAbcd  # @UnresolvedImport
import sk;  # @UnresolvedImport
from dectree import *
from diffevol import *
from settings import *


class model():
	def __init__(self):
		pass
	def treeTune():
    
    treeParam = The.tree
    whereParm = 
    def f1():
    	[test, train] = tdivPrec(trainDat[case], testDat[case]);
    	g = _runAbcd(train = train, test = test, verbose = False)
    	return g
	  return Cols(Schaffer,
                [N(least=-10, most=10)
                , O(f=f1) 
                , O(f=f2)
                ])

def main(dir = None):
 xtile = sk.xtile
 G = []; reps = 1;
 trainDat, testDat = explore(dir)
 case = 0
 for _ in xrange(reps):
  [test, train] = tdivPrec(trainDat[case], testDat[case]);
  # print test
  # print train
  # sys.path.insert(0, '/Users/rkrsn/git/axe/axe')
  g = _runAbcd(train = train, test = test, verbose = True)
  G.append(g)
  print xtile(G)

if __name__ == '__main__':
 main(dir = 'Data/')
