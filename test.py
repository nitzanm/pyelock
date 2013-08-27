import unittest
from pyelock import ELock

ELOCK_SERVER = ('staging2.6scan.com', 11400)

LOCKS = ['lock%d' % i for i in range(5)]

class TestBasicFunctions(unittest.TestCase):
    def setUp(self):
        self.elock = ELock(ELOCK_SERVER)

    def tearDown(self):
        self.elock.close()
        del self.elock

    def testBasic(self):
        self.assertTrue(self.elock.lock(LOCKS[0]))
        self.assertTrue(self.elock.lock(LOCKS[0]))
        self.assertTrue(self.elock.unlock(LOCKS[0]))

class TestTwoConnections(unittest.TestCase):
    def setUp(self):
        self.l1 = ELock(ELOCK_SERVER)
        self.l2 = ELock(ELOCK_SERVER)

    def tearDown(self):
        self.l1.close()
        self.l2.close()

    def testConcurrentLockUnlock(self):
        self.assertTrue(self.l1.lock(LOCKS[0]))
        self.assertFalse(self.l2.lock(LOCKS[0]))
        self.assertTrue(self.l1.unlock(LOCKS[0]))
        self.assertTrue(self.l2.lock(LOCKS[0]))

    def testUnlockAll(self):
        self.assertTrue(self.l1.lock(LOCKS[0]))
        self.assertFalse(self.l2.lock(LOCKS[0]))
        self.assertTrue(self.l1.unlock_all())
        self.assertTrue(self.l2.lock(LOCKS[0]))

if __name__ == '__main__':
    unittest.main()