from __future__ import division
import sys
sys.dont_write_bytecode = True

def atom(x):
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError : return x

def cmd(com="demo('-h')"): ## if no arguments, spit out help file.
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring) ## Python has 2 kinds of strings. Check if
  def wrap(x): return "'%s'"%x if strp(x) else str(x) ## what does this do?
  words = map(wrap,map(atom,sys.argv[2:])) ## Apply function to every item of 
  ## iterable and return a list of the results.
  return sys.argv[1] + '(' + ','.join(words) + ')' ## This creates a function 
  ## of the command line arguments


## This is the decorator function:
def demo(f=None,cache=[]):   
  def doc(d):
    return '# '+d.__doc__ if d.__doc__ else ""  ## Print the first lies as strings
  if f == '-h':
    print '# sample demos'
    for n,d in enumerate(cache): 
      print '%3s) ' %(n+1),d.func_name,doc(d) ## Print out 1) function name, and
      # all the initial comment lines. That is if the input argument is -h
  elif f: 
    cache.append(f); # If f is a function then append f to the cache
  else:
    s='|'+'='*40 +'\n'
    for d in cache: 
      print '\n==|',d.func_name,s,doc(d),d()
  return f

def test(f=None,cache=[]):
  if f: 
    cache += [f]
    return f
  ok = no = 0
  for t in cache: 
    print '#',t.func_name ,t.__doc__ or ''
    prefix, n, found = None, 0, t() or []
    while found:
      this, that = found.pop(0), found.pop(0)
      if this == that:
        ok, n, prefix = ok+1, n+1,'CORRECT:'
      else: 
        no, n, prefix = no+1, n+1,'WRONG  :'
      print prefix,t.func_name,'test',n
  if ok+no:
    print '\n# Final score: %s/%s = %s%% CORRECT' \
        % (ok,(ok+no),int(100*ok/(ok+no)))

@test
def tested():
  return [True,True,  # should pass
          False,True, # should fail
          1, 2/2]     # should pass

@demo
def demoed(show=1):
  "Sample demo."
  print show/2

@demo
def tests():
  "Run all the test cases."
  test()

