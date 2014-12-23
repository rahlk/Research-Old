from _imports import *
from contrastset import *
from dectree import *
import makeAmodel as mam
from methods1 import *


def _treatments(dir='./Data'):
  train, test = explore(dir)

  # Training data ===============================================================
  train_DF = createTbl(train[1])

  # Testing data ===============================================================
  test_df = createTbl(test[1])

  # Decision Tree ===============================================================
  t = discreteNums(train_DF, map(lambda x: x.cells, train_DF._rows))
  myTree = tdiv(t)
#  showTdiv(myTree)

  # Testing data ===============================================================
  testCase = test_df._rows
  
  for tC in [testCase[0]]:
   loc = drop(tC, myTree)

  print loc

if __name__ == '__main__':
  _treatments(dir = './Data')


