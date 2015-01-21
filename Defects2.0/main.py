
def Bugs(tbl):
  cells = [i.cells[-2] for i in tbl._rows]
  return cells

def withinClass(data):
  N = len(data)
  return [(data[:n], [data[n]]) for n in range(1, N)]

def haupt():
  dir = './Data'
  from os import walk
  dataName = [Name for _, Name, __ in walk(dir)][0]
  numData = len(dataName)  # Number of data
  Prd = [rforest, CART, adaboost, logit, knn]
  cd = []
  for p in [rforest]:
    print('#', p.__doc__)
    one, two = explore(dir)
    data = [one[i] + two[i] for i in xrange(len(one))];
    for n in xrange(numData):
      train = [dat[0] for dat in withinClass(data[n])]
      test = [dat[1] for dat in withinClass(data[n])]
      print('##', dataName[n])
#       print('```')
      for _n in [-1]:  # xrange(len(train)):
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
        # actual.insert(0, 'Actual')

        # Use the random forest classifier to predict the number of bugs in the raw data.
        before = sorted(p(train_DF, test_df))
        # before.insert(0, 'Before')

        # Use the random forest classifier to predict the number of bugs in the new data.
        after = sorted(p(train_DF, newTab))
        # after.insert(0, 'After')

        stat = [before, after]
#         set_trace()
        plotCurve(stat, fname = p.__doc__ + '_' + str(_n), ext = '.jpg')
        write('Training: '); [write(l + ', ') for l in train[_n]]; print('\n')
        write('Test: '); [write(l) for l in test[_n]], print('\n', '```')
        # sk.rdivDemo(stat)

        # histplot(stat, bins = [1, 3, 5, 7, 10, 15, 20, 50])
        # _Abcd(before = actual, after = before)
        print(showoff(dataName[n], before, after))
        cd.append(showoff(dataName[n], before, after))
      print('```')

        # sk.rdivDemo(stat)
        # Save the histogram after applying contrast sets.
        # saveImg(bugs, num_bins = 10, fname = 'bugsAfter', ext = '.jpg')

        # <<DEGUG: Halt Code>>
    set_trace()


if __name__ == '__main__':
#  _CART()
#  _logit()
#  _adaboost()
  haupt()
