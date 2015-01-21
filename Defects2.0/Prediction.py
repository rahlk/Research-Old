from pdb import set_trace
from os import environ, getcwd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from Planning import formatData
from abcd import _Abcd
from dectree import *


# Update PYTHONPATH
HOME = environ['HOME']
axe = HOME + '/git/axe/axe/'  # AXE
pystat = HOME + '/git/pystats/'  # PySTAT
cwd = getcwd() # Current Directory
sys.path.extend([axe, pystat, cwd])


def Bugs(tbl):
  cells = [i.cells[-2] for i in tbl._rows]
  return cells

#=====================================================================================
# PREDICTION SYSTEMS: 1. RANDOM FORESTS, 2. DECISION TREES, 3. ADABOOST, 4. LOGISTIC
#                                                                           REGRESSION
#=====================================================================================
def rforest(train, test):
  "Random Forest"
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
