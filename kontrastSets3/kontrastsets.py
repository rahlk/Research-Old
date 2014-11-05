from __future__ import division
import sys,pdb
from lib    import *
import libWhere
from dtree import tdiv, showTdiv
sys.dont_write_bytecode = True
from dtree import *
from where2 import *
from table import *
from settingsWhere import *
import random
randi=random.randint

class o:
  def __init__(self,**d): self.update(**d)
  def update(self,**d): self.__dict__.update(**d); return self

class makeAModel(object):
 def __init__(self):
  self.seen=[]
  self.translate={}
  pass
 
 def data(self,indep=[], less=[], more=[], _rows=[]):
  nindep= len(indep)
  ndep  = len(less) + len(more)
  m= o(lo={}, hi={}, w={}, 
       eval  = lambda m,it : True,
       _rows = [o(cells=r,score=0,scored=False,
                  x0=None,y0=None) 
                for r in _rows],
       names = indep+less+more)
  m.decisions  = [x for x in range(nindep)]
  m.objectives = [nindep+ x- 1 for x in range(ndep)]
  m.cols       = m.decisions + m.objectives
  for x in m.decisions : 
    m.w[x]=  1
  for y,_ in enumerate(less) : 
    m.w[x+y]   = -1
  for z,_ in enumerate(more) : 
    m.w[x+y+z] =  1
  for x in m.cols:
    all = sorted(row.cells[x] for row in m._rows)
    m.lo[x] = all[0]
    m.hi[x] = all[-1]
  return m
 
 def str2num(self,tbl):
  P=1;
  for row in tbl._rows:
   for k in row.cells:
    if not k in self.seen:
     self.seen.append(k)
     self.translate.update({k:P})
     P+=1
    
 def csv2py(self, filename):
  "Convert a csv file to a model file"
  tbl=table(filename)
  self.str2num(tbl)
  tonum= lambda x: self.translate[x] if isinstance(x, str) else x
  
  for indx, k in enumerate(tbl.indep):
   for l in tbl.depen:
    if k.name==l.name:
     tbl.indep.pop(indx)
    
  return self.data(indep=[i.name for i in tbl.indep],
                   less=[i.name for i in tbl.depen],
                   _rows=map(lambda x: [tonum(xx) for xx in x.cells], tbl._rows))
   

def makeMeATable(tbl,headerLabel,Rows):
 tbl2=clone(tbl)
 newHead=Num()
 newHead.col = len(tbl.headers)
 newHead.name= headerLabel 
 tbl2.headers=tbl.headers+[newHead]
 return clone(tbl2,Rows)
 

def _tdivdemo(file='data/nasa93dem.csv'): 
 #==============================================================================
 # We start by recursively clustering the model.
 #==============================================================================
 makeaModel=makeAModel()
 m=makeaModel.csv2py(file) 
 prepare(m) # Initialize all parameters for where2 to run
 tree=where2(m, m._rows) # Decision tree using where2
 tbl = table(file)  
 headerLabel='=klass'
 Rows=[]
 for k,_ in leaves(tree):
  for j in k.val:
    tmp=j.cells
    tmp.append('_'+str(id(k) % 1000)) 
    j.__dict__.update({'cells': tmp})
    Rows.append(j.cells)
 tbl2=makeMeATable(tbl, headerLabel, Rows)
 
 testCase=tbl2._rows.pop(1)
 t=discreteNums(tbl2, map(lambda x: x.cells, tbl2._rows))  
 myTree=tdiv(t) 
 loc=apex(testCase, myTree)
 print loc.__dict__
 print 'Id: ',loc.mode, ' Level: ', loc.lvl, ' Variable: ', loc.f.name
 showTdiv(myTree)
 #==============================================================================
 for node, lvl in dtnodes(myTree):
  rows=map(lambda x:x.cells,node.rows)
  #pdb.set_trace()
  print lvl, len(rows), rows
 #==============================================================================
_tdivdemo(file='data/nasa93dem.csv')