import socket
import re

class ELockException(Exception): pass

class ResourceLocked(ELockException): pass

class NotLocked(ELockException): pass

class NotResumable(ELockException): pass

class BadRequest(ELockException): pass

class BadResponse(ELockException): pass

class Timeout(ELockException): pass

class ELock(object):
    """The elock protocol."""

    def __init__(self, remote_endpoint):
        '''
        Initializes an elock session.
        @param remote_endpoint elock server endpoint, e.g. ('127.0.0.1', 11400).
        '''
        self.socket = socket.socket()
        self.socket.connect(remote_endpoint)

        # This class doesn't support resuming connections, so set
        # the abandon timeout to zero.
        code,message = self.__cmd("set_timeout 0")
        if code != 200:
            raise BadResponse()

    def __del__(self):
        self.socket.close()
        del self.socket

    def __cmd(self, command, timeout=10.0):
        self.socket.settimeout(timeout)
        self.socket.sendall(command + "\r\n")
        buffer = ""
        while '\r\n' not in buffer:
            try:
                buffer += self.socket.recv(1024)
            except socket.timeout as e:
                raise Timeout()

        try:
            code, message = self.__read_status(buffer)
        except:
            raise BadResponse()

        '''match = re.match('^([0-9]{3}) (.+)$', buffer)
        if not match:
            raise BadResponse()

        code,message = match.groups()
        try:
            code = int(code)
        except:
            raise BadResponse()'''

        if code == 400:
            raise BadRequest()

        return code,message

    def lock(self, name, timeout=None):
        '''
        Acquire a lock.
        @name Name of the lock (cannot contain spaces).
        @timeout Time to wait for the lock if it's in use, in seconds.
            If None (the default), return immediately if the lock is in use.
        @return True if the lock was acquired; False otherwise.
        @note If you already hold a lock, locking it again will succeed.  However,
            multiple holds will not stack, such that a single unlock() will release
            the lock entirely, even after a number of lock() calls.
        '''

        cmd = 'lock %s%s' % (name, ' ' + str(timeout) if timeout else '')
        code, response = self.__cmd(cmd, timeout=(timeout or 0) + 10.0)
        if code == 200:
            return True
        elif code == 409:
            return False
        else:
            raise BadResponse()

    def unlock(self, name):
        '''
        Release an acquired lock.
        @name Name of the lock (cannot contain spaces).
        @return True if the lock was released; False if you did not own the lock.
        '''
        code, response = self.__cmd('unlock ' + name)
        if code == 200:
            return True
        elif code == 403:
            return False
        else:
            raise BadResponse()

    def unlock_all(self):
        '''
        Releases all locks held by the current session.
        @return True
        '''
        code, response = self.__cmd('unlock_all')
        if code != 200:
            raise BadResponse()
        return True

    def __read_status(self, line):
        status, msg = line.strip().split(' ', 1)
        return int(status), msg
