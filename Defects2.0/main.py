from __future__ import print_function
from os import environ, getcwd
import sys

# Update PYTHONPATH
HOME = environ['HOME']
axe = HOME + '/git/axe/axe/'  # AXE
pystat = HOME + '/git/pystats/'  # PySTAT
cwd = getcwd()  # Current Directory
sys.path.extend([axe, pystat, cwd])

from Prediction import *
from Planning import *
from _imports import *
from abcd import _Abcd
from cliffsDelta import showoff
from contrastset import *
from dectree import *
from methods1 import *
import numpy as np
import pandas as pd
import sk

def Bugs(tbl):
  cells = [i.cells[-2] for i in tbl._rows]
  return cells

def withinClass(data):
  N = len(data)
  return [(data[:n], [data[n]]) for n in range(1, N)]

def write(str):
  sys.stdout.write(str)


def main():
  dir = '../Data'
  from os import walk
  dataName = [Name for _, Name, __ in walk(dir)][0]
  numData = len(dataName)  # Number of data
  Prd = [CART]  # , adaboost, logit, knn]
  _smoteit = [True, False]
  cd = {}
  for p in Prd:
    print('#', p.__doc__)
    one, two = explore(dir)
    data = [one[i] + two[i] for i in xrange(len(one))];
    for n in xrange(numData):
      train = [dat[0] for dat in withinClass(data[n])]
      test = [dat[1] for dat in withinClass(data[n])]
      print('##', dataName[n])
      for _smote in _smoteit:
        if _smote: print('### SMOTE-ing')
        else: print('### No SMOTE-ing')
  #       print('```')
        for _n in [-1]:  # xrange(len(train)):
          # Training data
          train_DF = createTbl(train[_n])

          # Testing data
          test_df = createTbl(test[_n])

          # Save a histogram of unmodified bugs
          # saveImg(Bugs(test_df), num_bins = 10, fname = 'bugsBefore', ext = '.jpg')

          # Find and apply contrast sets
          newTab = treatments(train = train[_n], test = test[_n], verbose = False)

          # Actual bugs
          actual = Bugs(test_df)
          # actual.insert(0, 'Actual')
          actual1 = [0 if a == 0 else 1 for a in actual]
          # Use the random forest classifier to predict the number of bugs in the raw data.
          before = p(train_DF, test_df, smoteit = _smote)
          # before.insert(0, 'Before')
          before1 = [0 if b == 0 else 1 for b in before]
          # Use the random forest classifier to predict the number of bugs in the new data.
          after = p(train_DF, newTab, smoteit = _smote)
          after1 = [0 if a == 0 else 1 for a in after]
          # after.insert(0, 'After')

          stat = [before, after]
  #         set_trace()
          # plotCurve(stat, fname = p.__doc__ + '_' + str(_n), ext = '.jpg')
          write('Training: '); [write(l + ', ') for l in train[_n]]; print('\n')
          write('Test: '); [write(l) for l in test[_n]], print('\n', '```')
          # sk.rdivDemo(stat)
          # histplot(stat, bins = [1, 3, 5, 7, 10, 15, 20, 50])
          _Abcd(before = actual1, after = before1)
  #         print(showoff(dataName[n], before1, after1))
          # cd.append(showoff(dataName[n], before, after))
        print('```')

          # sk.rdivDemo(stat)
          # Save the histogram after applying contrast sets.
          # saveImg(bugs, num_bins = 10, fname = 'bugsAfter', ext = '.jpg')

          # <<DEGUG: Halt Code>>
     # cd.update({p.__doc__:sorted(cd)})
      # set_trace()


if __name__ == '__main__':
#  _CART()
#  _logit()
#  _adaboost()
  main()
