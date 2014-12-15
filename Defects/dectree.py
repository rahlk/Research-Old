from __future__ import division
import sys, pdb, os
from lib    import *
import libWhere
from dtree import tdiv, showTdiv
sys.dont_write_bytecode = True
from dtree import *
from where2 import *
from table import *
from settingsWhere import *
from settings import *
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import random, numpy as np
randi = random.randint
rseed = random.seed

def say(text):
  sys.stdout.write(str(text)), sys.stdout.write(' ')
class o:
  def __init__(self, **d): self.update(**d)
  def update(self, **d): self.__dict__.update(**d); return self

class makeAModel(object):
 def __init__(self):
  self.seen = []
  self.translate = {}
  pass

 def data(self, indep = [], less = [], more = [], _rows = []):
  nindep = len(indep)
  ndep = len(less) + len(more)
  m = o(lo = {}, hi = {}, w = {},
       eval = lambda m, it : True,
       _rows = [o(cells = r, score = 0, scored = False,
                  x0 = None, y0 = None)
                for r in _rows],
       names = indep + less + more)
  m.decisions = [x for x in range(nindep)]
  m.objectives = [nindep + x - 1 for x in range(ndep)]
  for k, indx in enumerate(m.decisions):
   for l in m.objectives:
    if k == l: m.decisions.pop(indx)
  m.cols = m.decisions + m.objectives
  for x in m.decisions :
    m.w[x] = 1
  for y, _ in enumerate(less) :
    m.w[x + y] = -1
  for z, _ in enumerate(more) :
    m.w[x + y + z] = 1
  for x in m.cols:
    all = sorted(row.cells[x] for row in m._rows)
    m.lo[x] = all[0]
    m.hi[x] = all[-1]
  return m

 def str2num(self, tbl):
    P = 1;
    for row in tbl._rows:
      for k in row.cells:
        if not k in self.seen and isinstance(k, str):
          self.seen.append(k)
          self.translate.update({k:P}) if isinstance(k, str) \
                                 else self.translate.update({k:k})
          P += 1

 def csv2py(self, filename):
  "Convert a csv file to a model file"
  tbl = table(filename)
  self.str2num(tbl)
  tonum = lambda x: self.translate[x] if isinstance(x, str) else x

  for indx, k in enumerate(tbl.indep):
   for l in tbl.depen:
    if k.name == l.name:
     tbl.indep.pop(indx)

  # [(sys.stdout.write(tI.name), sys.stdout.write(' ')) for tI in tbl.depen]

  return self.data(indep = [i.name for i in tbl.indep],
                   less = [i.name for i in tbl.depen],
                   _rows = map(lambda x: [tonum(xx) for xx in x.cells],
                               tbl._rows))



def makeMeATable(tbl, headerLabel, Rows):
 tbl2 = clone(tbl)
 newHead = Sym()
 newHead.col = len(tbl.headers)
 newHead.name = headerLabel
 tbl2.headers = tbl.headers + [newHead]
 return clone(tbl2, rows = Rows)

def getContrastSet(loc, myTree):
 contrastSet = {};
 # print loc.f.name, loc.lvl+1, loc.val
 def remember(node):
  key = node.f.name
  Val = node.val
  contrastSet.update({key: Val})
  # print contrastSet
 def forget(key):
  del contrastSet[key]
 def objectiveScores(lst):
  obj = ([k.cells[-2] for k in lst.rows])
  return np.median([k for k in obj]), [k for k in obj]
 def compare(node, test):
   leaves = [n for n in test.kids] if len(test.kids) > 0 else [test]
   for k in leaves:
    return objectiveScores(k) < objectiveScores(node), [objectiveScores(k),
                                                        objectiveScores(node)]
 def trackChanges(testing):
  lvl = testing.lvl
  while lvl > 0:
   lvl = testing.lvl  # @IndentOk
   remember(testing)
   testing = testing.up
 cost = 0
 newNode = loc
 print 'Test Case: '
 print ('Variable name: ', newNode.f.name, 'ID: ', newNode.mode,
        'Value: ', newNode.val, 'Level: ', newNode.lvl + 1)
 print 'No. of Kids: ', len(newNode.kids)
 print 'Cost: ', cost
 def isOnlyNode(node):
  return len(node.kids) <= 1
 while isOnlyNode(newNode):
  # go 1 level up
  newNode = newNode.up;
  # remember(newNode)
  cost += 1
 toScan = [neigh for neigh in newNode.kids if not loc == neigh]
 for testing in toScan:
  isBetter, obj = compare(loc, testing)
  if isBetter:
   trackChanges(testing)
 return contrastSet


def leaveOneOut(test, tree):
 loc = apex(test, tree)
 return loc

def _tdivdemo(file = 'Data/'):
 #==============================================================================
 # We start by recursively clustering the model.
 #==============================================================================
 makeaModel = makeAModel()
 m = makeaModel.csv2py(file)
 rseed(1)

 prepare(m)  # Initialize all parameters for where2 to run
 tree = where2(m, m._rows)  # Decision tree using where2
 tbl = table(file)
 headerLabel = '=klass'
 Rows = []
 for k, _ in leaves(tree):
   for j in k.val:
     tmp = (j.cells)
     tmp.append('_' + str(id(k) % 1000))
     j.__dict__.update({'cells': tmp})
     Rows.append(j.cells)
 tbl2 = makeMeATable(tbl, headerLabel, Rows)
 # print
 testCase = [tbl2._rows.pop(randi(0, len(tbl2._rows))) for k in xrange(500)]
 t = discreteNums(tbl2, map(lambda x: x.cells, tbl2._rows))
 myTree = tdiv(t)
 showTdiv(myTree)
 loc = leaveOneOut(testCase[randi(0, len(testCase))], myTree)
 # contrastSet = getContrastSet(loc, myTree)
 # print 'Contrast Set:', contrastSet

def saveAs(x, num_bins):
 n, bins, patches = plt.hist(x, num_bins, normed = False, facecolor = 'blue', alpha = 0.5)
 # add a 'best fit' line
 plt.xlabel('Bugs')
 plt.ylabel('Frequency')
 plt.title(r'Histogram (Median Bugs in each class)')

 # Tweak spacing to prevent clipping of ylabel
 plt.subplots_adjust(left = 0.15)
 plt.savefig('hist.jpg')
 plt.close()


def _tdivPrec(dir = 'camel/'):

 #==============================================================================
 # Recursively clustering the model.
 #==============================================================================

 rseed(1)
 makeaModel = makeAModel()
 _rows = []


 def explore(dir):
  from os import walk
  datasets = []
  for (dirpath, dirnames, filenames) in walk(dir):
     datasets.append(dirpath)

  training = []
  testing = []
  for k in datasets[1:]:
   train = [[dirPath, fname] for dirPath, _, fname in walk(k)]
   test = [train[0][0] + '/' + train[0][1].pop(-1)]
   training.append([train[0][0] + '/' + p for p in train[0][1] if not p == '.DS_Store']);
   testing.append(test)
  return training, testing

 train, test = explore(dir)
 _r = []
 # pdb.set_trace()
 for t in train[10]:
  m = makeaModel.csv2py(t)
  _r += m._rows
 m._rows = _r
 # print len(_r)
 prepare(m)  # Initialize all parameters for where2 to run
 tree = where2(m, m._rows)  # Decision tree using where2
 tbl = table(t)
 headerLabel = '=klass'
 Rows = []
 for k, _ in leaves(tree):  # for k, _ in leaves(tree):
  for j in k.val:
   tmp = (j.cells)
   tmp.append('_' + str(id(k) % 1000))
   j.__dict__.update({'cells': tmp})
   Rows.append(j.cells)
 tbl2 = makeMeATable(tbl, headerLabel, Rows)

 _r = []
 for tt in test[10]:
  mTst = makeaModel.csv2py(tt)
  _r += mTst._rows

  mTst._rows = _r
 # print len(_r)
 prepare(mTst)  # Initialize all parameters for where2 to run
 tree = where2(mTst, mTst._rows)  # Decision tree using where2
 tbl = table(tt)
 headerLabel = '=klass'
 Rows = []
 for k, _ in leaves(tree):  # for k, _ in leaves(tree):
  for j in k.val:
   tmp = (j.cells)
   tmp.append('_' + str(id(k) % 1000))
   j.__dict__.update({'cells': tmp})
   Rows.append(j.cells)
 tbl3 = makeMeATable(tbl, headerLabel, Rows)


 def isdefective(case, test = False):
  if not test:
   return 'Defect' if case.cells[-2] > 0 else 'No Defect'
  else:
   bugs = [r.cells[-2] for r in case.rows];
   meanBugs = np.mean(bugs);
   medianBugs = np.median(bugs);
   rangeBugs = (sorted(bugs)[0] + sorted(bugs)[-1]) / 2; tmp.append(meanBugs);
   # print(tmp)
   # print [r.cells[-2] for r in case.rows]
   return 'Defect' if meanBugs > 1.5 else 'No Defect'

 testCase = tbl3._rows
 # print testCase

 testDefective = []
 defectivClust = []

 t = discreteNums(tbl2, map(lambda x: x.cells, tbl2._rows))
 myTree = tdiv(t)
 # showTdiv(myTree)

 testCase = tbl3._rows
#   # print testCase

 for tC in testCase:
  loc = leaveOneOut(tC, myTree)
  # if len(loc.kids)==0:
  testDefective.append(isdefective(tC))
  defectivClust.append(isdefective(loc, test = True))

#
#   saveAs(tmp, 10)
#
#   contrastSet = getContrastSet(loc, myTree)
#   # print 'Contrast Set:', contrastSet
 return [testDefective, defectivClust]


if __name__ == '__main__':
#  G = []; reps = 10
#  for _ in xrange(reps):
#   [test, train] = _tdivPrec(dir = 'Data/');
#   # print test
#   # print train
#   sys.path.insert(0, '/Users/rkrsn/git/axe/axe')
#   from abcd import _runAbcd
#   import sk; xtile = sk.xtile
#   g = _runAbcd(train = train, test = test, verbose = False)
#   G.append(g)
#  # G.insert(0,'Test1')
#  print G
#  print xtile(G)
#
 G = []; reps = 10
 for _ in xrange(reps):
  [test, train] = _tdivPrec(dir = 'Data/');
  # print test
  # print train
  # sys.path.insert(0, '/Users/rkrsn/git/axe/axe')
  from abcd import _runAbcd  # @UnresolvedImport
  import sk; xtile = sk.xtile
  g = _runAbcd(train = train, test = test, verbose = True)
  G.append(g)
 # G.insert(0, 'Test1')
 # print G
 print xtile(G)
