import sys, os
sys.path.append(os.environ['HOME'] + '/git/axe/axe')
sys.path.insert(0, os.getcwd() + '/_imports');
from demos import *
import sk;  # @UnresolvedImport
from dectree import *
from diffevol import *
from settings import *
from settingsWhere  import *
from pdb import set_trace
from abcd import _Abcd
from Prediction import rforest, Bugs
from methods1 import createTbl
tree = treeings()
# set_trace()
def update(indep):
  whereParm = defaults().update(verbose = True,
                                minSize = int(indep[0]),
                                depthMin = int(indep[1]),
                                depthMax = int(indep[2]),
                                prune = int(indep[3]),
                                wriggle = int(indep[4]))
  tree.min = int(indep[5])
  tree.infoPrune = int(indep[6])
  tree.variancePrune = int(indep[7])
  tree.m = int(indep[6])
  tree.n = int(indep[7])
  prune = int(indep[8])
  return whereParm, tree

def tuneRF():
  # Tune RF
  trainDat = explore(dir = '../Data/')[0]  # Only training data to tune.
  train = createTbl(trainDat[0]); test = createTbl(trainDat[1])
  def f1(rows):
    [mss, msl, n_est, max_feat] = rows[1:-1];
    mod = rforest(train, test, mss = int(mss), msl = int(msl),
                  max_feat = int(max_feat), n_est = int(n_est),
                  smoteit = True)
    g = _Abcd(before = Bugs(train), after = mod, show = False)[0]
    return g

  return Cols(tuneRF,
        [N(least = 1, most = 10)
        , N(least = 1, most = 10)
        , N(least = 10, most = 1e6)
        , N(least = 1, most = 17)
        , O(f = f1)])

def _test():
  m = tuneRF()
  for _ in range(10):
    one = m.any()
    m.score(one)
  print(one)

def _de():
  "DE"
  DE = diffEvol(model = tuneRF);
  res = sorted([k for k in DE.DE()],
               key = lambda F: F[-1])[-1]
  return res

def main(dir = None):
  whereParm, tree = None, None  # _de()
  G = []; G1 = []; reps = 1;
  trainDat, testDat = explore(dir = 'Data/')
  for _ in xrange(reps):
    print reps
    [test, train] = tdivPrec(whereParm, tree, train = trainDat[1], test = testDat[0]);
    g = _runAbcd(train = train, test = test, verbose = False)
    G.append(g)
  G.insert(0, 'DT  ')

  for _ in xrange(reps):
    print reps
    [test, train] = tdivPrec1(whereParm, tree, train = trainDat[1], test = testDat[0]);
    g = _runAbcd(train = train, test = test, verbose = False)
    G1.append(g)
  G1.insert(0, 'C4.5')
  return [G, G1]

if __name__ == '__main__':
  from timeit import timeit
  s = _test()
  timeit(stmt = s, number = 1)
#   print _de()
#  print main()
#  import sk; xtile = sk.xtile
#  print xtile(G)

 # main(dir = 'Data/')
