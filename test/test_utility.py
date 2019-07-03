# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

import richman.utility as util


class ForTest:
    a = 1
    b = 2
    def __init__(self, name):
        self.name = name
        self.c = 0
        self.__d = 4

class TestUtility(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_transaction_should_commit_and_rollback_correctly(self):
        t1 = ForTest('t1')
        t2 = ForTest('t2')
        t3 = ForTest('t3')
        test_classes = [t1, t2, t3]
        transaction = util.Transaction(False, test_classes,
                                       rollback_len=5)
        transaction.commit()
        t1.c = 1
        t2.c = 1
        t3.c = 1
        transaction.commit()
        t1.c = 2
        t2.c = 2
        t3.c = 2
        transaction.commit()
        t1.c = 3
        t2.c = 3
        t3.c = 3
        self.assertListEqual([3,3,3], [t.c for t in test_classes])
        transaction.rollback(2)
        self.assertListEqual([1,1,1], [t.c for t in test_classes])
