# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 01:13:03 2014

@author: rkrsn
"""

def atom(x):
  """
  Type convert the input to a string
  """
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError : return x

d=atom
print atom(6.009), d.__doc__, d.func_name