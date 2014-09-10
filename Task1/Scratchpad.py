# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 01:13:03 2014

@author: rkrsn
"""
from demos import *

def findmax(a,b):
  sys.stdout.write(str(a)) if a>b else sys.stdout.write(str(b))
  sys.stdout.write('\n')

if __name__=='__main__': eval(cmd())

"""
def atom(x):

  Type convert the input to a string
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError : return x

d=atom
print atom(6.009), d.__doc__, d.func_name
"""
