- I tried to use dtree to create a decision tree. Some datasets didn't have the 'class' variable. 
- I used where2 to do a recursive fastmap clustering an generate a new column in datasets without a class variable.
- The csv2py method converts the *.csv file to a model format so where2 may run on it
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
