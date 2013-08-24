=======
PyElock
=======

Pure Python wrapper for https://github.com/dustin/elock .

elock is "A simple, fault-tolerant distributed lock server in erlang."  Using
it in Python allows you to do all sorts of cool stuff, like ensuring a Celery
task doesn't run more than once simultaneously, even across different Celery
servers.

Note, if you are already using Twisted in your project, you should check out
dustin's wrapper at https://github.com/dustin/elock-twisted .

Usage
=====

Simple single lock:

    try:
      with pyelock.ELockSingle(('remote-server.domain.com', 11400), 'my_lock'):
        # Do some stuff
        time.sleep(10)
    except pyelock.LockInUse:
      print "Can't do stuff, my_lock is in use"

If you want precise control over your locking behavior, or want to acquire
multiple locks, use the following code:

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
