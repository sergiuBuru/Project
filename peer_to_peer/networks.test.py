import unittest
from networks import *
import time


class Test(unittest.TestCase):

    def setUp(self): pass

    def tearDown(self): pass

    def test_01_constructor(self):
        n = Node(9000)
        self.assertEqual(9000, n.port)
        n.disconnect()

    def test_02_connect(self):
        n = Node(9000)
        m = Node(9001)
        n.listen()
        m.listen()
        m.connect_to_peer((n.ip, n.port))
        n.integrated.wait()
        m.integrated.wait()
        self.assertTrue(n.integrated.is_set())
        self.assertTrue(m.integrated.is_set())
        self.assertEqual(1, len(n.sockets))
        self.assertEqual(1, len(m.sockets))
        n.connect_to_peer((m.ip, m.port))
        self.assertEqual(1, len(n.sockets))
        self.assertEqual(1, len(m.sockets))
        time.sleep(1)
        n.disconnect()
        m.disconnect()

    def test_03_connect_with_3(self):
        n1 = Node()
        n2 = Node(9002)
        n3 = Node(9003)
        n1.listen()
        n2.listen()
        n3.listen()
        n2.connect_to_peer((n1.ip, n1.port))
        n3.connect_to_peer((n1.ip, n1.port))
        n1.integrated.wait()
        n2.integrated.wait()
        n3.integrated.wait()
        self.assertTrue(n1.integrated.wait())
        self.assertTrue(n2.integrated.wait())
        self.assertTrue(n3.integrated.wait())
        n1.connect_to_peer((n2.ip, n2.port))
        self.assertEqual(2, len(n1.sockets))
        self.assertEqual(1, len(n2.sockets))
        self.assertEqual(1, len(n3.sockets))
        time.sleep(1)
        n1.disconnect()
        n2.disconnect()
        n3.disconnect()


if __name__ == '__main__':
    unittest.main()
