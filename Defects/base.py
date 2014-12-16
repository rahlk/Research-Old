import sys
sys.path += ['./_imports'];
from abcd import _runAbcd  # @UnresolvedImport
import sk;  # @UnresolvedImport
from dectree import *

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
 print sys.path
#  main(dir = 'Data/')
