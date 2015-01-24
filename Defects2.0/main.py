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
from sk import rdivDemo
from pdb import set_trace
def Bugs(tbl):
  cells = [i.cells[-2] for i in tbl._rows]
  return cells

def withinClass(data):
  N = len(data)
  return [(data[:n], [data[n]]) for n in range(1, N)]

def write(str):
  sys.stdout.write(str)

def printsk(a, b):
  "Now printing only g"
  set_trace()
  dat1 = a[0][0] + [k[-1] for k in a]
  dat2 = b[0][0] + [k[-1] for k in b]
  rdivDemo[[dat1, dat2]]


def main():
  dir = '../Data'
  from os import walk
  dataName = [Name for _, Name, __ in walk(dir)][0]
  numData = len(dataName)  # Number of data
  Prd = [rforest]  # , CART, adaboost, logit, knn]
  _smoteit = [True, False]
  abcd = []
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
        print('### SMOTE-ing') if _smote else print('### No SMOTE-ing')
  #       print('```')
        for _n in [-1]:  # xrange(len(train)):
          # Training data
          reps = 10
          abcd = [];
          for _ in xrange(reps):
            train_DF = createTbl(train[_n])

            # Testing data
            test_df = createTbl(test[_n])

            # Find and apply contrast sets
            newTab = treatments(train = train[_n], test = test[_n], verbose = False)

            # Actual bugs
            actual = Bugs(test_df)
            actual1 = [0 if a == 0 else 1 for a in actual]
            # Use the classifier to predict the number of bugs in the raw data.
            before = p(train_DF, test_df, smoteit = _smote)
            before1 = [0 if b == 0 else 1 for b in before]
            # Use the classifier to predict the number of bugs in the new data.
            after = p(train_DF, newTab, smoteit = _smote)
            after1 = [0 if a == 0 else 1 for a in after]

            stat = [before, after]
            write('Training: '); [write(l + ', ') for l in train[_n]]; print('\n')
            write('Test: '); [write(l) for l in test[_n]], print('\n', '```')
            out = _Abcd(before = actual1, after = before1)
            out.insert(0, 'SMOTE') if _smote else out.insert(0, 'No SMOTE')
            abcd.append(out)
      printsk(abcd[1:reps], abcd[reps + 1:])
#             cd.append(showoff(dataName[n], before, after))

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
