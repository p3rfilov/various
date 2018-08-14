# -*- coding: utf-8 -*-

import unittest
from vendingMachine import Cash

class TestMXSCommands(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cash = Cash()
         
#     @classmethod
#     def tearDownClass(self):
#         pass

    def testConvertStringToCash(self):
        result = sorted([self.cash.convertStringToCash(i) for i in self.cash.bank.keys()], reverse=True)
        test = [1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
        self.assertEqual(result, test)
        
if __name__ == '__main__':
    unittest.main()