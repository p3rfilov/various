# -*- coding: utf-8 -*-

import unittest
from vendingMachine import Cash

class TestCash(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cash = Cash()
         
#     @classmethod
#     def tearDownClass(self):
#         pass

    def testConvertStringToCash(self):
        result = sorted([self.cash.convertStringToCash(i) for i in self.cash.bank.keys()], reverse=True)
        test = [100, 50, 20, 10, 5, 2, 1]
        self.assertEqual(result, test)
        
if __name__ == '__main__':
    unittest.main()