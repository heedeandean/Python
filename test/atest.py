Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 14:05:16) [MSC v.1915 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> 100
100
>>> 'a'
'a'
>>> dir
<built-in function dir>
>>> help
Type help() for interactive help, or help(object) for help about object.
>>> help(dir)
Help on built-in function dir in module builtins:

dir(...)
    dir([object]) -> list of strings
    
    If called without an argument, return the names in the current scope.
    Else, return an alphabetized list of names comprising (some of) the attributes
    of the given object, and of attributes reachable from it.
    If the object supplies a method named __dir__, it will be used; otherwise
    the default dir() logic is used and returns:
      for a module object: the module's attributes.
      for a class object:  its attributes, and recursively the attributes
        of its bases.
      for any other object: its attributes, its class's attributes, and
        recursively the attributes of its class's base classes.

>>> 
=================== RESTART: C:/haha/Python/test/ctest.py ===================
>>> 
=================== RESTART: C:/haha/Python/test/ctest.py ===================
100
a
>>> 
=================== RESTART: C:/haha/Python/test/ctest.py ===================
100
a
>>> 
=================== RESTART: C:/haha/Python/test/doit01.py ===================
연습입니다
>>> 100+100
200
>>> 100-100
0
>>> 
>>> message='도전과제'
>>> mess
Traceback (most recent call last):
  File "<pyshell#9>", line 1, in <module>
    mess
NameError: name 'mess' is not defined
>>> message
'도전과제'
>>> 
