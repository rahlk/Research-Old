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
from Prediction import rforest, CART, Bugs
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

def tuneRF(data):
  # Tune RF
  if not data:
    # In no training data, use Ant
    data = explore(dir = '../Data/')[0][0]  # Only training data to tune.
  train = createTbl([data[0]]); test = createTbl([data[1]])
#   set_trace()
  def f1(rows):
    mod = rforest(train, test
                , tunings = rows[1:-1]  # n_est, max_feat, mss, msl
                , smoteit = True)
    g = _Abcd(before = Bugs(test), after = mod, show = False)[-1]
    return g

  return Cols(tuneRF
        , [N(least = 10, most = 5e3)  # n_estimators
        , N(least = 1, most = 17)  # max_features
        , N(least = 1, most = 20)  # min_samples_leaf
        , N(least = 2, most = 20)  # min_samples_split
        , O(f = f1)])

def tuneCART(data):
  # Tune CART
  if not data:
    # In no training data, use Ant
    data = explore(dir = '../Data/')[0][0]  # Only training data to tune.
  train = createTbl([data[0]]); test = createTbl([data[1]])
#   set_trace()
  def f1(rows):
    [mss, msl, max_depth, max_feat, max_leaf_nodes] = rows[1:-1];
    mod = CART(train, test
               , tunings = rows[-1:1]
               , smoteit = True)
    g = _Abcd(before = Bugs(test), after = mod, show = False)[-1]
    return g

  return Cols(tuneCART
        , [N(least = 1, most = 50)  # max_depth
        , N(least = 2, most = 20)  # min_samples_split
        , N(least = 1, most = 20)  # min_samples_leaf
        , N(least = 1, most = 17)  # max features
        , N(least = 2, most = 1e3)  # max_leaf_nodes
        , O(f = f1)])

def _test(data):
  m = tuneRF(data)
  vals = [(m.any()) for _ in range(10)]
  vals1 = [m.score(v) for v in vals]
  print(vals, vals1)

def _de(model, data):
  "DE"
  DE = diffEvol(model, data);
#   set_trace()
  res = sorted([k for k in DE.DE()],
               key = lambda F: F[-1])[-1]
  return res

def tune(data, pred):
  if pred == rforest:
    return _de

if __name__ == '__main__':
  from timeit import time
  data = explore(dir = '../Data/')[0][0]  # Only training data to tune.
  for m in [tuneRF, tuneCART]:
    t = time.time()
#   _test(data)
    print _de(m, data)
    print time.time() - t
#   print _de()
#  print main()
#  import sk; xtile = sk.xtile
#  print xtile(G)

 # main(dir = 'Data/')
