from _imports import *
from contrastset import *
from dectree import *
import makeAmodel as mam
from methods1 import *


def _treatments(dir='./Data'):
  train, test = explore(dir)

  # Training data
  train_DF = createTbl(train[1])
  # Testing data
  test_df = createTbl(test[1])

  t = discreteNums(tbl2, map(lambda x: x.cells, tbl2._rows))
  myTree = tdiv(t)
  showTdiv(myTree)

if __name__ == '__main__':
  _treatments(dir = './Data')


