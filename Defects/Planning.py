from __future__ import print_function

from pdb import set_trace
from random import uniform, randint
import sys

from abcd import _runAbcd
import sk
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from _imports import *
from contrastset import *
from dectree import *
from hist import *
import makeAmodel as mam
from methods1 import *
import numpy as np
import pandas as pd


def write(str):
  sys.stdout.write(str)

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

def Bugs(tbl):
  cells = [i.cells[-2] for i in tbl._rows]
  return cells

def formatData(tbl):
  Rows = [i.cells for i in tbl._rows]
  headers = [i.name for i in tbl.headers]
  return pd.DataFrame(Rows, columns = headers)

#=====================================================================================
# PREDICTION SYSTEMS: 1. RANDOM FORESTS, 2. DECISION TREES, 3. ADABOOST, 4. LOGISTIC
#                                                                           REGRESSION
#=====================================================================================

def rforest(train, test):
  """
  Random Forest
  """
  # Apply random forest classifier to predict the number of bugs.
  clf = RandomForestClassifier(n_estimators = 930, n_jobs = -1,
                               max_features = 3)
  train_DF = formatData(train)
  test_DF = formatData(test)
  features = train_DF.columns[:-2]
  klass = train_DF[train_DF.columns[-2]];
  # set_trace()
  clf.fit(train_DF[features], klass)
  preds = clf.predict(test_DF[test_DF.columns[:-2]]).tolist()
  return preds

def _RF():
  "Test RF"
  dir = './Data'
  one, two = explore(dir)
  # Training data
  train_DF = createTbl(train[0])
  # Test data
  test_df = createTbl(test[0])
  actual = Bugs(test_df)
  preds = rforest(train_DF, test_df)

def CART(train, test):
  """
  CART: Classification and Regression Trees
  """
  # Apply random forest classifier to predict the number of bugs.
  clf = DecisionTreeClassifier(max_features = 'auto')
  train_DF = formatData(train)
  test_DF = formatData(test)
  features = train_DF.columns[:-2]
  klass = train_DF[train_DF.columns[-2]];
  # set_trace()
  clf.fit(train_DF[features], klass)
  preds = clf.predict(test_DF[test_DF.columns[:-2]]).tolist()
  return preds

def _CART():
  "Test CART"
  dir = './Data'
  one, two = explore(dir)
  # Training data
  train_DF = createTbl(one[0])
  # Test data
  test_df = createTbl(two[0])
  actual = Bugs(test_df)
  preds = CART(train_DF, test_df)
  set_trace()
  _runAbcd(train = actual, test = preds, verbose = True)

def adaboost(train, test):
  """
  ADABOOST
  """
  clf = AdaBoostClassifier()
  train_DF = formatData(train)
  test_DF = formatData(test)
  features = train_DF.columns[:-2]
  klass = train_DF[train_DF.columns[-2]];
  # set_trace()
  clf.fit(train_DF[features], klass)
  preds = clf.predict(test_DF[test_DF.columns[:-2]]).tolist()
  return preds

def _adaboost():
  "Test AdaBoost"
  dir = './Data'
  one, two = explore(dir)
  # Training data
  train_DF = createTbl(one[0])
  # Test data
  test_df = createTbl(two[0])
  actual = Bugs(test_df)
  preds = adaboost(train_DF, test_df)
  set_trace()
  _runAbcd(train = actual, test = preds, verbose = True)

def withinClass(data):
  N = len(data)
  return [(data[:n], [data[n]]) for n in range(1, N)]

def haupt():
  dir = './Data'
  from os import walk
  dataName = [Name for _, Name, __ in walk(dir)][0]
  numData = len(dataName)  # Number of data
  print('# CART')
  one, two = explore(dir)
  data = [one[i] + two[i] for i in xrange(len(one))];
  for n in xrange(numData):
    train = [dat[0] for dat in withinClass(data[n])]
    test = [dat[1] for dat in withinClass(data[n])]
    print('##', dataName[n])
    for _n in xrange(len(train)):
      # Training data
      train_DF = createTbl(train[_n])

      # Testing data
      test_df = createTbl(test[_n])


      # Save a histogram of unmodified bugs
      # saveImg(Bugs(test_df), num_bins = 10, fname = 'bugsBefore', ext = '.jpg')

      # Find and apply contrast sets
      newTab = _treatments(train = train[_n], test = test[_n], verbose = False)

      # Actual bugs
      actual = Bugs(test_df)
      actual = [a for a in actual if not a == 0]
      actual.insert(0, 'Actual')

  #     set_trace()

      # Use the random forest classifier to predict the number of bugs in the raw data.
      beforeRF = rforest(train_DF, test_df)
      beforeRF = [b for b in beforeRF if not b == 0]
      beforeRF.insert(0, 'Before')

      beforeCART = CART(train_DF, test_df)
      beforeCART = [b for b in beforeRF if not b == 0]
      beforeCART.insert(0, 'Before')

      # Use the random forest classifier to predict the number of bugs in the new data.
      after = CART(train_DF, newTab)
      after = [a for a in after if not a == 0]
      after.insert(0, 'After')

      stat = [actual, beforeCART, after]

      write('Training: '); [write(l + ', ') for l in train[_n]]; print('')
      write('Test: '); [write(l) for l in test[_n]], print('\n', '```')
      histplot(stat, bins = [1, 3, 5, 7, 10, 15, 20, 50])
      print('```')

      # sk.rdivDemo(stat)
      # Save the histogram after applying contrast sets.
      # saveImg(bugs, num_bins = 10, fname = 'bugsAfter', ext = '.jpg')

      # <<DEGUG: Halt Code>>
      # set_trace()


if __name__ == '__main__':
# _CART()
#   _adaboost()
  haupt()

