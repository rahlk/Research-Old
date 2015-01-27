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
from random import uniform as rand, randint as randi, choice as any
tree = treeings()
# set_trace()

def settings(**d): return o(
  name = "Differention Evolution",
  what = "DE tuner. Tune the predictor parameters parameters",
  author = "Rahul Krishna",
  adaptation = "https://github.com/ai-se/Rahul/blob/master/DEADANT/deadant.py",
  copyleft = "(c) 2014, MIT license, http://goo.gl/3UYBp",
  seed = 1,
  np = 10,
  k = 100,
  tiny = 0.01,
  de = o(np = 5,
       epsilon = 1.01,
       f = 0.3,
       cf = 0.4,
       lives = 100)
  ).update(**d)

The = settings()
class DE(object):
  def __init__(self, depen, indep, data):
    self.frontier = []
    self.depen = depen
    self.indep = indep
  def any(self, min, max):
    return [randi(min, max) for __ in len(self.depen)]
  def initFront(self, N):
    for _ in xrange(N):
      self.frontier.append([])
  def extrapolate(self, a, b, c):
    return int(a + The.de.f * (b - c))
  def one234(self, one, pop, f = lambda x:id(x)):
    def oneOther():
      x = any(pop)
      while f(x) in seen:
        x = any(pop)
      seen.append(f(x))
      return x
    seen = [ f(one) ]
    return oneOther(), oneOther(), oneOther()
  def dominates(self, a, b):
    return self.gscore(a) > self.gscore(b)
  def gscore(self, lst):
    
  def DE(self):
    self.initFront(The.np * self.indep)
    lives = The.de.lives
    while lives > 0:
      better = False
      for pos, l1 in enumerate(self.frontier):
       l2, l3, l4 = self.one234(l1, self.frontier)
       new = self.m.extrapolate(l2, l3, l4)
       if  self.m.dominates(new, l1):
        self.frontier.pop(pos)
        self.remember(new)
        better = True
       elif self.m.dominates(l1, new):
        better = False
       else:
        self.remember(new)
        better = True
       if not better:
          lives -= 1
    return self.frontier


ca tuneRF(data):
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

def tuner(model, data):
  if model == rforest:
    return _de(tuneRF, data)[1:-1]
  elif model == CART:
    return _de(tuneCART, data)[1:-1]

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
