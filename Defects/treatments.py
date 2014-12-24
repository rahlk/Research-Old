from __future__ import print_function

from pdb import set_trace

from _imports import *

from contrastset import *
from dectree import *
import makeAmodel as mam
from methods1 import *


def _treatments(dir = './Data', verbose = True):
  train, test = explore(dir)

  # Training data ===============================================================
  train_DF = createTbl(train[1])

  # Testing data ===============================================================
  test_df = createTbl(test[1])

  # Decision Tree ===============================================================
  t = discreteNums(train_DF, map(lambda x: x.cells, train_DF._rows))
  myTree = tdiv(t)
  if verbose: showTdiv(myTree)

  # Testing data ===============================================================
  testCase = test_df._rows
  
  for tC in testCase:
    loc = drop(tC, myTree)
    # Reach the tree top =========================================================
    newNode = loc;
    branches = [];
    while newNode.lvl >= 0:
      newNode = newNode.up;
      branches.append(newNode);
    
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
     return np.mean([k for k in obj]), [k for k in obj]
    def compare(node, test):
      leaves = [n for n in test.kids] if len(test.kids) > 0 else [test]
      for k in leaves:
       return objectiveScores(k) < objectiveScores(node), [objectiveScores(k),
                                                           objectiveScores(node)]
    #  def trackChanges(testing):
    #    lvl = testing.lvl
    #    while lvl > 0:
    #      lvl = testing.lvl
    #      remember(testing)
    #      testing = testing.up
    
    for nn in branches:
      toScan = nn.kids
    #    set_trace()
      for testing in toScan:
        isBetter, obj = compare(loc, testing)
        if isBetter:
          remember(testing)
          continue
    
    print(contrastSet)


if __name__ == '__main__':
  _treatments(dir = './Data', verbose = False)


