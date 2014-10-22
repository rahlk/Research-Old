### Quick Summary
- I tried to use dtree to create a decision tree. Some datasets didn't have the 'class' variable. 
- I used where2 to do a recursive fastmap clustering an generate a new column in datasets without a class variable.
- The [csv2py](https://github.com/rahlk/Research/blob/master/kontrastSets/kontrastsets.py#L54) method converts the *.csv file to a model format so where2 may run on it
```python
def csv2py(self, filename):
  "Convert a csv file to a model file"
  tbl=table(filename)
  self.str2num(tbl)
  tonum= lambda x: self.translate[x] if isinstance(x, str) else x
  _rows=map(lambda x: [tonum(xx) for xx in x.cells], tbl._rows)
  
  return self.data(indep=[i.__dict__['name'] for i in tbl.indep],
                   less=[i.__dict__['name'] for i in tbl.depen],
                   _rows=map(lambda x: [tonum(xx) for xx in x.cells], tbl._rows))
```
- I wrapped this in the [makeAModel](https://github.com/rahlk/Research/blob/master/kontrastSets/kontrastsets.py#L15) class. 
- I then wrote a  [_tdivdemo()](https://github.com/rahlk/Research/blob/master/kontrastSets/kontrastsets.py#L75) to create the decision tree. It works like a charm, if I may add. Here's what I get for `_tdivdemo(file='data/nasa93dem.csv')`
```
.cat2=2	:400 #3
|...modp=7	:928 #1 33% * 6
|...modp=10	:424 #1 36% * 11
.cat2=35	:688 #5
|...project=34	:688 #1 50% * 8
|...project=53	:976 #1 75% * 4
|...project=118	:920 #3
|..|...data=8	:848 #1 50% * 4
|..|...data=10	:920 #2
|..|..|...modp=8	:920 #1 50% * 4
|..|..|...modp=10	:352 #1 60% * 5
.cat2=56	:64 #1 25% * 4
.cat2=59	:904 #1 62% * 8
.cat2=103	:472 #2
|...project=118	:64 #1 100% * 4
.cat2=147	:848 #1 25% * 4
```

### Issues
- The files lib.py, settings.py in the where repo are different and incompatible with the file having the same filename in the axe repo. I had to rename them to get them working.

- In [nasa93.py](https://github.com/ai-se/where/blob/master/nasa93.py#L18) I noticed the variables have numeric values assigned to them, I guess their values are arbitrary given the way AHA distance works. Am I correct in making this assumption?


