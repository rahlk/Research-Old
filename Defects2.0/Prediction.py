from pdb import set_trace
from os import environ, getcwd
import sys
from scipy.spatial.distance import euclidean
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

def SMOTE(data = None, N = 5, k = 3, atleast = 50, atmost = 250):
  def minority(data):
    unique = list(set(sorted(Bugs(data))))
    counts = len(unique) * [0];
#     set_trace()
    for n in xrange(len(unique)):
      for d in Bugs(data):
        if unique[n] == d: counts[n] += 1
    return unique, counts

  def knn(one, two):
    pdistVect = []
#    set_trace()
    for ind, n in enumerate(two):
      pdistVect.append([ind, euclidean(one.cells[:-1], n.cells[:-1])])
    indices = sorted(pdistVect, key = lambda F:F[1])
    return [two[n[0]] for n in indices]

  def extrapolate(one, two):
    new = one;
#    set_trace()
    new.cells[3:-1] = [min(a, b) + rand() * (abs(a - b)) for
           a, b in zip(one.cells[3:-1], two.cells[3:-1])]
    return new

  def populate(data):
    newData = []
    while len(data) < atleast:
      for one in data:
        neigh = knn(one, data)[1:k + 1];
        two = choice(neigh)
        newData.append(extrapolate(one, two))
      data.extend(newData)
    return data

  def depopulate(data):
    return [choice(data) for _ in xrange(atmost)]
#   print minority(data)
  newCells = []
  unique, counts = minority(data)
#  set_trace()
  rows = data._rows
  for u, n in zip(unique, counts):
    if  1 < n < atleast:
      newCells.extend(populate([r for r in rows if r.cells[-2] == u]))
    elif n > atmost:
      newCells.extend(depopulate([r for r in rows if r.cells[-2] == u]))
    else:
      newCells.extend([r for r in rows if r.cells[-2] == u])

  set_trace()
  return clone(data, rows = newCells)

def _smote():
  dir = '../Data/camel/camel-1.6.csv'
  Tbl = createTbl([dir])
#   set_trace()
  newTbl = SMOTE(data = Tbl)
  for r in newTbl._rows:
    print r.cells


#=====================================================================================
# PREDICTION SYSTEMS: 1. RANDOM FORESTS, 2. DECISION TREES, 3. ADABOOST, 4. LOGISTIC
#                                                                           REGRESSION
#=====================================================================================
def rforest(train, test):
  "Random Forest"
  # Apply random forest classifier to predict the number of bugs.
  clf = RandomForestClassifier(n_estimators = 100, n_jobs = -1,
                               max_features = 5)
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
  "CART"
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
  _Abcd(train = actual, test = preds, verbose = True)

def adaboost(train, test):
  "ADABOOST"
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

def logit(train, test):
  "Logistic Regression"
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

def knn(train, test):
  "kNN"
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
  _smote()
