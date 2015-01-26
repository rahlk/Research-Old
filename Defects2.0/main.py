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

def printsk(res):
  "Now printing only g"
  tosh = []
  for p in res:
    dat1, dat2 = res[p]
    tosh.append([dat1[0][0]] + [k[-1] for k in dat1])
    tosh.append([dat2[0][0]] + [k[-1] for k in dat2])
  rdivDemo(tosh, isLatex = False)

def main():
  dir = '../Data'
  from os import walk
  dataName = [Name for _, Name, __ in walk(dir)][0]
  numData = len(dataName)  # Number of data
  Prd = [rforest, CART]  # , adaboost, logit, knn]
  _smoteit = [True, False]
  abcd = []
  res = {}
  for n in xrange(numData):
    one, two = explore(dir)
    data = [one[i] + two[i] for i in xrange(len(one))];
    print('##', dataName[n])
    for p in Prd:
      train = [dat[0] for dat in withinClass(data[n])]
      test = [dat[1] for dat in withinClass(data[n])]
      reps = 10
      abcd = [];
      for _smote in _smoteit:
#         print('### SMOTE-ing') if _smote else print('### No SMOTE-ing')
  #       print('```')
        for _n in [0]:  # xrange(len(train)):
          # Training data
          for _ in xrange(reps):
            train_DF = createTbl(train[_n])

            # Testing data
            test_df = createTbl(test[_n])

            # Find and apply contrast sets
            newTab = treatments(train = train[_n],
                                test = test[_n], verbose = False)

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
            write('.')
#             write('Training: '); [write(l + ', ') for l in train[_n]]; print('\n')
#             write('Test: '); [write(l) for l in test[_n]],
            out = _Abcd(before = actual1, after = before1)
            out.insert(0, p.__doc__ + '-s') if _smote \
            else out.insert(0, p.__doc__ + '-ns')
            abcd.append(out)
      print()
      res.update({p.__doc__:(abcd[0:reps], abcd[reps:])})
    print('```')
    printsk(res)
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
