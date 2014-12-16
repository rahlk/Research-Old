import sys, os
sys.path.append(os.environ['HOME'] + '/git/axe/axe')
sys.path.insert(0, os.getcwd() + '/_imports');
from demos import *
from abcd import _runAbcd  # @UnresolvedImport
import sk;  # @UnresolvedImport
from dectree import *
from diffevol import *
from settings import *
from settingsWhere  import *
from pdb import set_trace

tree = treeings()
# set_trace()
def model():
 trainDat, testDat = explore(dir = 'Data/')
 def f1(rows):
  indep = rows[1:-1]; case = 0
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

  [test, train] = tdivPrec(whereParm, tree, train = trainDat[case], test = testDat[case]);
  g = _runAbcd(train = train, test = test, verbose = False)
  return g

 return Cols(model,
        [N(least = 0, most = 20)
        , N(least = 2, most = 10)
        , N(least = 2, most = 15)
        , Bool(items = [True, False])
        , N(least = 0, most = 0.99)

        , N(least = 1, most = 10)
        , N(least = 1, most = 25)
        , N(least = 1, most = 10)
        , N(least = 1, most = 10)
        , O(f = f1)])

def _test():
  m = model()
  for _ in range(10):
    one = m.any()
    m.score(one)
    print(one)

def _de(m):
 "DE"
 DE = diffEvol(model = model);
 res = sorted([k for k in DE.DE()],
              key = lambda F: np.sum(F[-depenLen(m):]))
 return res[0][-depenLen(m):], DE.evals, spread(res, depenLen(m))

def main(dir = None):
 for _ in xrange(reps):
  g = _runAbcd(train = train, test = test, verbose = True)
  G.append(g)
  print xtile(G)

if __name__ == '__main__':
 _test()
 # main(dir = 'Data/')
