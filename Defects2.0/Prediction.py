from pdb import set_trace
from os import environ, getcwd
import sys
from scipy.stats.mstats import mode
from scipy.spatial.distance import euclidean
from numpy import mean
# Update PYTHONPATH
HOME = environ['HOME']
axe = HOME + '/git/axe/axe/'  # AXE
pystat = HOME + '/git/pystats/'  # PySTAT
cwd = getcwd()  # Current Directory
sys.path.extend([axe, pystat, cwd])
from random import choice, uniform as rand
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from smote import *
import pandas as pd
from abcd import _Abcd
from dectree import *


def formatData(tbl):
  Rows = [i.cells for i in tbl._rows]
  headers = [i.name for i in tbl.headers]
  return pd.DataFrame(Rows, columns = headers)

def Bugs(tbl):
  cells = [i.cells[-2] for i in tbl._rows]
  return cells

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PREDICTION SYSTEMS:
# ```````````````````
# 1. WHERE2 2. RANDOM FORESTS, 3. DECISION TREES, 4. ADABOOST,
# 5. LOGISTIC REGRESSION
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def where2prd(train, test, smoteit = True):
  "WHERE2"
  t = discreteNums(train, map(lambda x: x.cells, train._rows))
  myTree = tdiv(t)
  testCase = test._rows
  rows, preds = [], []
  for tC in testCase:
    newRow = tC;
    loc = drop(tC, myTree)  # Drop a test case in the tree & see where it lands
    if not loc.kids:
      rows.extend(loc.rows)
    else:
      for k in loc.kids: rows.extend(k.rows)
    vals = [r.cells[-2] for r in rows]
    preds.append([mode([k for k in vals])[0].tolist()])  # \
                 # if median(vals) > 0 else preds.extend([0])
  return preds

def _where2pred():
  "Test where2"
  dir = '../Data'
  one, two = explore(dir)
  # Training data
  train_DF = createTbl(one[0])
  # Test data
  test_df = createTbl(two[0])
  actual = Bugs(test_df)
  preds = where2prd(train_DF, test_df)
  for a, b in zip(actual, preds): print a, b
  set_trace()
  print _Abcd(before = actual, after = preds, show = False)


def rforest(train, test, mss = 2, msl = 2,
            max_feat = "auto", n_est = 10,
            smoteit = True):
  "    RF"
  # Apply random forest classifier to predict the number of bugs.
  if smoteit: train = SMOTE(train)
  clf = RandomForestClassifier(n_estimators = n_est,
                               n_jobs = -1,
                               max_features = max_feat,
                               min_samples_leaf = msl,
                               min_samples_split = mss
                               )
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
  dir = '../Data'
  one, two = explore(dir)
  # Training data
  train_DF = createTbl(one[0])
  # Test data
  test_df = createTbl(two[0])
  actual = Bugs(test_df)
  preds = rforest(train_DF, test_df, mss = 96, msl = 76,
            max_feat = 3, n_est = 9756,
            smoteit = True)
  print _Abcd(before = actual, after = preds, show = False)[-1]

def CART(train, test, smoteit = True):
  "  CART"
  # Apply random forest classifier to predict the number of bugs.
  if smoteit: train = SMOTE(train)
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
  _Abcd(train = actual, test = preds, verbose = True)

def adaboost(train, test, smoteit = True):
  "ADABOOST"
  if smoteit: train = SMOTE(train)
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
  _Abcd(train = actual, test = preds, verbose = True)

def logit(train, test, smoteit = True):
  "Logistic Regression"
  if smoteit: train = SMOTE(train)
  clf = LogisticRegression(penalty = 'l2', dual = False, tol = 0.0001, C = 1.0,
                           fit_intercept = True, intercept_scaling = 1,
                           class_weight = None, random_state = None)
  train_DF = formatData(train)
  test_DF = formatData(test)
  features = train_DF.columns[:-2]
  klass = train_DF[train_DF.columns[-2]];
  # set_trace()
  clf.fit(train_DF[features], klass)
  preds = clf.predict(test_DF[test_DF.columns[:-2]]).tolist()
  return preds

def _logit():
  "Test LOGIT"
  dir = './Data'
  one, two = explore(dir)
  # Training data
  train_DF = createTbl(one[0])
  # Test data
  test_df = createTbl(two[0])
  actual = Bugs(test_df)
  preds = logit(train_DF, test_df)
  set_trace()
  _Abcd(train = actual, test = preds, verbose = True)

def knn(train, test, smoteit = True):
  "kNN"
  if smoteit: train = SMOTE(train)
  neigh = KNeighborsClassifier()
  train_DF = formatData(train)
  test_DF = formatData(test)
  features = train_DF.columns[:-2]
  klass = train_DF[train_DF.columns[-2]];
  # set_trace()
  neigh.fit(train_DF[features], klass)
  preds = neigh.predict(test_DF[test_DF.columns[:-2]]).tolist()
  return preds

if __name__ == '__main__':
  random.seed(0)
  for _ in xrange(10): _RF()
