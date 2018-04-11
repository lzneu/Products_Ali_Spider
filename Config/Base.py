#-*-encoding=utf-8-*-

LogPrint = True

def myPrint(*args, sep=' ', end='\n', file=None):
   if LogPrint:
      print(*args, sep=' ', end='\n', file=None)
   else:
      pass