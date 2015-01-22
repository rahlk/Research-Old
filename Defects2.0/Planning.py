from __future__ import print_function

from os import environ, getcwd
from pdb import set_trace
from random import uniform, randint
import sys

# Update PYTHONPATH
HOME = environ['HOME']
axe = HOME + '/git/axe/axe/'  # AXE
pystat = HOME + '/git/pystats/'  # PySTAT
cwd = getcwd()  # Current Directory
sys.path.extend([axe, pystat, cwd])

from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from Prediction import *
from _imports import *
from abcd import _Abcd
from cliffsDelta import *
from contrastset import *
from dectree import *
from hist import *
import makeAmodel as mam
from methods1 import *
import numpy as np
import pandas as pd
import sk


#===============================================================================
# PLANNING PHASE: 1. Decision Trees, 2. Contrast Sets
#===============================================================================

  
def _treatments(train = None, test = None, verbose = True):

#   if not train_DF or test_df:
#     dir = './Data'
#
#     train, test = explore(dir)
#
#     # set_trace()
#     # Training data
  train_DF = createTbl(train)
#
#     # Testing data
  test_DF = createTbl(test)

  # Decision Tree

  t = discreteNums(train_DF, map(lambda x: x.cells, train_DF._rows))
#   set_trace()
  myTree = tdiv(t)
  if verbose: showTdiv(myTree)

  # Testing data
  testCase = test_DF._rows

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
  def getKey():
    keys = {}
    for i in xrange(len(test_DF.headers)):
      keys.update({test_DF.headers[i].name[1:]:i})
    return keys

  keys = getKey();
  newTab = []
  for tC in testCase:
    newRow = tC;
    loc = drop(tC, myTree)
    # Reach the tree top
    newNode = loc;
    branches = [];
    while newNode.lvl >= 0:
      newNode = newNode.up;
      branches.append(newNode);
    # A dict of contrast sets
    contrastSet = {};
    # print loc.f.name, loc.lvl+1, loc.val
    for nn in branches:
      toScan = nn.kids
    #    set_trace()
      for testing in toScan:
        isBetter, obj = compare(loc, testing)
        if isBetter:
          remember(testing)
          continue  # As soon as the first better node is found, exit..

    # Pick a random value in the range suggested by the contrast set and
    # assign it to the row.
    for k in contrastSet:
      min, max = contrastSet[k]
      if isinstance(min, int) and isinstance(max, int):
        val = randint(min, max)
      else: val = uniform(min, max)
      newRow.cells[keys[k]] = val

    newTab.append(newRow.cells)

  updatedTab = clone(test_DF, rows = newTab, discrete = True)
  return updatedTab
#  saveImg(bugs(test_df), num_bins = 50, fname = 'bugsBefore', ext = '.jpg')
#  set_trace()
