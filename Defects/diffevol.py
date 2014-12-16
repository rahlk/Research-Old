from __future__ import division, print_function
import sys, random, time; import os, pdb, math, numpy as np
from math import sin
_pwd=os.getcwd()
from re import search
import sk; rdivDemo=sk.rdivDemo
sys.dont_write_bytecode = True
exp=math.e

def settings(**d): return o(
  name="Differention Evolution",
  what="DE tuner. Tune the dtree and where parameters",
  author="Rahul Krishna",
  adaptation = "https://github.com/ai-se/Rahul/blob/master/DEADANT/deadant.py",
  copyleft="(c) 2014, MIT license, http://goo.gl/3UYBp",
  seed=1,
  np=10,
  k=100,
  tiny=0.01,
  de=o(np=5,
       epsilon=1.01,
       f=0.3,
       cf=0.4,
       lives=100)
  ).update(**d)

def say(lst):
 sys.stdout.write(lst)
 
class o:
  def __init__(self, **d): self.update(**d)
  def update(self, **d): self.__dict__.update(**d); return self

rand = random.random
seed = random.seed
any = random.choice
exp = math.exp

def say(*lst):
  sys.stdout.write(' '.join(map(str, lst)))
  sys.stdout.flush()
def sayln(*lst):
  say(*lst); print("")

def _say(): sayln(1, 2, 3, 4)

The = settings()


def cmd(com=The.start):
  if globals()["__name__"] == "__main__":
    if len(sys.argv) == 3:
      if sys.argv[1] == '--cmd':
        com = sys.argv[2] + '()'
    if len(sys.argv) == 4:
        com = sys.argv[2] + '(' + sys.argv[3] + ')'
    eval(com)

class Col:
  def any(self): return None
  def fuse(self, x, w1, y, w2): return None
  def nudge(self, x, y, sampled): return None
  def dist(self, x, y): return 0
  def norm(self, x) : return x
  def extrapolate(self, x, y, z): return None

class N(Col):
  "For nums"
  def __init__(self, col=0, least=0, most=1, name=None):
    self.col = col
    self.name = None
    self.least, self.most = least, most  
    self.lo, self.hi = 10 ** 32, -1 * 10 ** 32
  def extrapolate(self, x, y, z):
    f = The.de.f
    return x + f * (y - z)    
  def any(self):
   return max(self.least,
               min(self.most,
                   self.least + rand() * (self.most - self.least)))
  def __iadd__(self, x):
    #print("x",x,"least",self.least,"most",self.most)
    #x = x if not x >= self.least else self.most if x >
    self.lo = min(self.lo, x)
    self.hi = max(self.hi, x)
    return self
  def norm(self, x):
    tmp = (x - self.lo) / (self.hi - self.lo + 0.00001)
    return max(0, min(1, tmp))
  def dist(self, x, y):
    return np.sqrt(self.norm(x)**2 - self.norm(y)**2)
  def fuse(self, x, w1, y, w2):
    return (x * w1 + y * w2) / (w1 + w2)
  def nudge(self, x, y, sampled):
   if sampled: 
    tmp = sorted([x + rand() * 1.5 * (y - x) 
                  for _ in xrange(100)], 
                 key = lambda F: abs(F-x))[-1]
   else:
    tmp = x + rand() * 1.5 * (y - x) 
   if tmp > self.most : tmp = self.least
   if tmp < self.least: tmp = self.most
   return tmp
    
class S(Col):
  "For syms"
  def __init__(self, col=0, items=[], name=None):
    self.index = frozenset(items)
    self.items = items
    self.col = col
    self.name = name 
  def any(self):
    return random.choice(self.items)
  def __iadd__(self, x): 
    assert x in self.index
  def dist(self, x, y): return 0 if x == y else 0
  def fuse(self, x, w1, y, w2):
    return x if rand() <= w1 / (w1 + w2) else y
  def nudge(self, x, y, sampled=True):
    return x if rand() < 0.33 else y
  def extrapolate(self, x, y, z):
    if rand() >= The.de.cf: 
      return x
    else:
      w = y if rand() <= f else z 
      return x if rand() <= 0.5 else w

class O(Col):
  "for objectives"
  def __init__(self, col=0, f=lambda x: 1, name=None,
    love=False  # for objectives to maximize, set love to True
    ):
    self.f = f
    self.love = love
    self.name = name or f.__name__
    self.n = N(col=col, least=-10 ** 32, most=10 ** 32)
  def score(self, lst):
    x = lst[self.col]
    if x == None:
        x = self.f(lst)
        self.n += x
        lst[self.col] = x
    return x
  def better(self, x, y):
    e = The.de.epsilon
    return x > y * e if self.love else x < y / e
  def worse(self, x, y):
    return x < y if self.love else x > y
  
class Meta(Col):
  id = 0
  def __init__(self, of, weight=1, dead=True):
    self.weight, self.dead, self.of = weight, dead, of
    self.id = Meta.id = Meta.id + 1
  def any(self):
    return Meta(self.of)
  def fuse(self, x, w1, y, w2): 
    tmp = self.any()
    tmp.weight = w1 + w2
    return tmp
  def nudge(self, x, y, sampled=True): return self.any()
  def extrapolate(self, x, y, z):
   return Meta(self.of)
  def __repr__(self):
    return self.of.name

class diffEvol(object):
  "DE"
  
  def __init__(self, model=Schaffer):
    self.m=model()
    self.pop = {}
    self.frontier=[]
    self.evals=0
  
  def itsAlive(self, lst): 
   lst[0].dead = False; self.m.score(lst); 
   return lst
  
  def remember(self, new): 
   self.frontier.append(self.itsAlive(new)); self.evals+=1;
  
  def initFront(self, n) :
    for _ in range(n):
      self.remember(self.m.any())

  def one234(one, pop, f=lambda x:id(x)): 
	  def oneOther():
	    x = any(pop)
	    while f(x) in seen: 
	      x = any(pop)
	    seen.append( f(x) )
	    return x
	  seen  = [ f(one) ]
	  return oneOther(), oneOther(), oneOther()

  def DE(self):
    self.initFront(The.np * len(self.m.indep))
    lives = The.de.lives
    while lives > 0:
      better = False
      for pos, l1 in enumerate(self.frontier):
       lives -= 1
       l2, l3, l4 = one234(l1, self.frontier)
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
      if better:
       lives += 1
    return self.frontier

class model():
	def __init__(self):
		pass
	def treeTune():
    
    def f1():
    	[test, train] = tdivPrec(trainDat[case], testDat[case]);
    	g = _runAbcd(train = train, test = test, verbose = False)
    	return g
	  return Cols(Schaffer,
                [N(least=-10, most=10)
                , O(f=f1) 
                , O(f=f2)
                ])
 


