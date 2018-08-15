# -*- coding: utf-8 -*-

import unittest
from vendingMachine import Cash

class TestCash(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cash = Cash()

    def testConvertStringToCash(self):
        result = sorted([self.cash.convertStringToCash(i) for i in self.cash.bank.keys()], reverse=True)
        test = [100, 50, 20, 10, 5, 2, 1]
        self.assertEqual(result, test)
        
    def testGiveChange(self):
        r1 = self.cash.giveChange(50, 50)
        r2 = self.cash.giveChange(50, 100)
        r3 = self.cash.giveChange(112, 200)
        r4 = self.cash.giveChange(112, 2000)
        
        t1 = 'No change needed'
        t2 = ['50p',]
        t3 = ['50p', '20p', '10p', '5p', '2p', '1p'] # 200p - 112p = 88p
        t4 = False # not enough change
        
        self.assertEqual(r1, t1)
        self.assertEqual(r2, t2)
        self.assertEqual(r3, t3)
        self.assertEqual(r4, t4)
        
if __name__ == '__main__':
    unittest.main()
