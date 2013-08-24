pyelock
=======

Pure Python wrapper for https://github.com/dustin/elock .  If you are already
using Twisted in your project, check out https://github.com/dustin/elock-twisted
instead.

Usage
=====

Simple Single Lock
------------------

If you need to lock a single lock, perform a task, and then release it,
use the following code:

More complex use cases
----------------------

If you want precise control over your locking behavior, or want to acquire
multiple locks, use the following code:

```python
with pyelock.ELock(('remote-server.domain.com', 11400)) as elock:
  # Acquire a lock, waiting up to 30 seconds for it
  if not elock.lock('my_lock', timeout=30.0):
    print "Oh no, can't get my_lock"
  
  # Acquire another lock, without waiting if it's locked
  if not elock.lock('my_other_lock'):
    print "Can't get my_other_lock"
  
  # Do some stuff...
  
  # Release first lock
  elock.unlock('my_lock')
  
  # Do some other stuff...
  
  # Note: you don't technically need to release locks right before the end
  # of the 'with' block, since all locks held will be automatically released
  # when the object is destroyed.
```
