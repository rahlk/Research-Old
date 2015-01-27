import sys, os
sys.path.append(os.environ['HOME'] + '/git/axe/axe')
sys.path.insert(0, os.getcwd() + '/_imports');
from demos import *
import sk;  # @UnresolvedImport
from dectree import *
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
       N = 20,
       f = 0.3,
       cf = 0.4,
       lives = 100)
  ).update(**d)

The = settings()
class diffEvol(object):
  "Differential Evolution"
  def __init__(self, model, data):
    self.frontier = []
    self.model = model(data)

  def new(self):
    return [randi(d) for d in self.model.indep()]
  def initFront(self, N):
    for _ in xrange(N):
      self.frontier.append(self.new())
  def extrapolate(self, l2, l3, l4):
    return [int(a + The.de.f * (b - c)) for a, b, c in zip(l2, l3, l4)]
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
    return self.model.depen(a) > self.model.depen(b)

  def DE(self):
    self.initFront(The.de.N)
    lives = The.de.lives
    while lives > 0:
      better = False
      for pos, l1 in enumerate(self.frontier):
       l2, l3, l4 = self.one234(l1, self.frontier)
       new = self.extrapolate(l2, l3, l4)
       if  self.dominates(new, l1):
        self.frontier.pop(pos)
        self.frontier.insert(pos, new)
        better = True
       elif self.dominates(l1, new):
        better = False
       else:
        self.frontier.append(new)
        better = True
       if not better:
          lives -= 1
    return self.frontier


class tuneRF(object):
  # Tune RF
  def __init__(self, data):
    self.data = data
    self.train = createTbl([data[0]])
    self.test = createTbl([data[1]])
#   set_trace()
  def depen(self, rows):
    mod = rforest(self.train, self.test
                , tunings = rows[1:-1]  # n_est, max_feat, mss, msl
                , smoteit = True)
    g = _Abcd(before = Bugs(test), after = mod, show = False)[-1]
    return g

  def indep(self):
    return [(10, 5e3)  # n_estimators
          , (1, 17)  # max_features
          , (1, 20)  # min_samples_leaf
          , (2, 20)  # min_samples_split
          ]

class tuneCART(data):
  # Tune CART
  def __init__(self, data):
    self.data = data
    self.train = createTbl([data[0]])
    self.test = createTbl([data[1]])

  def depen(self, rows):
    [mss, msl, max_depth, max_feat, max_leaf_nodes] = rows[1:-1];
    mod = CART(self.train, self.test
               , tunings = rows[-1:1]
               , smoteit = True)
    g = _Abcd(before = Bugs(test), after = mod, show = False)[-1]
    return g

  def indep(self):
    return [(1, 50)  # max_depth
          , (2, 20)  # min_samples_split
          , (1, 20)  # min_samples_leaf
          , (1, 17)  # max features
          , (2, 1e3)]  # max_leaf_nodes

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
