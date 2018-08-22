# -*- coding: utf-8 -*-
import time

class VendingMachine():
    '''
    This class runs the program loop and includes the main logic.
    Most methods are provided by Stock() and Cash() classes (see below)
    '''
    def __init__(self):
        self.running = True
        self.Stock = Stock()
        self.Cash = Cash()
        self.help()
    
    def help(self):
        s = '''
======= Welcome to Python Vending Machine! =======
    
    
====================== HELP ======================
Usage:
    1. Select operation type (follow instructions)
    2. If buying, type the name of the item
    3. Insert coins one-by-one
        
Accepted coins:
    1p, 2p, 5p, 10p, 20p, 50p, 1 (one pound)
    
Type 'exit' to quit application at any time
=================================================='''
        print s
    
    def manageHelp(self):
        s = '''
===========================================
The following operations are available:
funds - displays available funds
stock - displays current stock of products
coins - add coins to the machine
add - add existing products (re-stock)
price - change prices of existing products
new - add a new product
        
back - to go to the previous menu
==========================================='''
        print s
    
    def run(self):
        while self.running:
            newSession = False
            s = raw_input('Please select operation: "buy" or "manage"\n>>> ')
            if s == 'manage':
                while not newSession and self.running:
                    opr = raw_input('Type "help" or enter operation\n>>> ')
                    if opr == 'help':
                        self.manageHelp()
                    if opr == 'funds':
                        self.Cash.getAvailableFunds()
                    if opr == 'stock':
                        self.Stock.getCurrentStock()
                    if opr == 'coins':
                        coin = raw_input('Please enter coin type.\n>>> ')
                        quantity = raw_input('Please enter quantity.\n>>> ')
                        self.Cash.addCoins(coin, quantity)
                    if opr == 'add':
                        product = raw_input('Please enter existing product name.\n>>> ')
                        quantity = raw_input('Please enter quantity.\n>>> ')
                        self.Stock.reStock(product, quantity)
                    if opr == 'price':
                        product = raw_input('Please enter existing product name.\n>>> ')
                        price = raw_input('Please enter new price.\n>>> ')
                        self.Stock.changeProductPrice(product, price)
                    if opr == 'new':
                        product = raw_input('Please enter new product name.\n>>> ')
                        price = raw_input('Please enter price.\n>>> ')
                        quantity = raw_input('Please enter quantity.\n>>> ')
                        self.Stock.addNewProduct(product, price, quantity)
                    if opr == 'back':
                        newSession = True
                        break
                    if opr == 'exit':
                        self.stop()
                
            if s == 'buy':
                self.Stock.getCurrentStock()
                while not newSession and self.running:   
                    item = raw_input('What would you like to buy?\n>>> ')   
                    if item == 'exit':
                        self.stop()  
                    if item in self.Stock.stock.keys():
                        qty = self.Stock.getProductQuantity(item)
                        if qty == 0:
                            print 'Sorry, this Item is out of stock...'
                        
                        else:
                            insertedCash = 0
                            price = self.Stock.getProductPrice(item)
                            remainder = price - insertedCash
                            while not newSession and self.running:
                                s = raw_input(u'Please insert £{p}:\n>>> '.format(p=remainder/self.Cash.poundScaleFactor))
                                if s == 'exit': self.stop()
                                cash = self.Cash.convertStringToCash(s)
                                
                                if cash:
                                    self.Cash.insertCoinString(s)
                                    insertedCash += cash
                                    remainder -= cash
                                    if insertedCash >= price:
                                        hasChange = self.Cash.giveChange(price, insertedCash)
                                        if hasChange:
                                            self.sellItem(item)
                                            print 'Your change: ' + str(hasChange)
                                            newSession = True
                                        else:
                                            print 'Sorry, there is not enough change... Please try again.'
                                            self.Cash.returnCoins()
                                            insertedCash = 0
                                else:
                                    if self.running:
                                        print 'Bad input!'
                    else:
                        if self.running:
                            print 'No such item! Try again.'
            if s == 'exit': self.stop()
    
    def stop(self):
        if self.running:
            self.Cash.returnCoins()
            print 'Bye! Thank you for shopping!'
            time.sleep(1.5)
            self.running = False
            
    def sellItem(self, product):
        self.Stock.giveItem(product)
        self.Cash.addToBank()
        self.Stock.getCurrentStock()
        print "Enjoy your {p}!".format(p=product)

class Cash():
    '''
    This class manages all monetary operations (apart from stock prices).
    The same data structure (self.bank) is used throughout the program, to avoid duplicate code.
    '''
    def __init__(self):
        self.bank = {
            '1p':10,
            '2p':10,
            '5p':10,
            '10p':10,
            '20p':10,
            '50p':10,
            '1':10 # £1
            }
        self.coinsInserted = []
        self.poundScaleFactor = 100
    
    def getPoundScaleFactor(self):
        return self.poundScaleFactor
        
    def addToBank(self):
        for coin in self.coinsInserted[:]: # make a in-place slice copy
            if coin in self.bank.keys():
                self.bank[coin] += 1
                self.coinsInserted.remove(coin)
                
    def addCoins(self, coin, quantity):
        if coin in self.bank.keys():
            try:
                self.bank[coin] += abs(int(quantity))
                print 'Coins added!'
            except:
                print 'Quantity must be a number!'
        else:
            print 'Unknown coin type!'
            
    def getAvailableFunds(self):
        for key, val in self.bank.iteritems():
            print '{k} : {v}'.format(k=key, v=val)
        return self.bank
    
    def insertCoinString(self, string):
        self.coinsInserted.append(string)
        
    def returnCoins(self):
        if self.coinsInserted:
            print 'Returning coins: ' + ', '.join(self.coinsInserted)
            self.coinsInserted = []
                
    def convertStringToCash(self, string):
        if string in self.bank.keys():
            if string == '1':
                return int(string)*self.poundScaleFactor
            elif string.endswith('p'):
                return int(string[:-1])
        else:
            return False
        
    def convertCashToString(self, cash):
        for coin in self.bank.keys():
            c = self.convertStringToCash(coin)
            if not c:
                return False
            elif c == cash:
                return coin
        return False
        
    def getInsertedCoins(self):
        return self.coinsInserted
    
    def giveChange(self, price, cash):
        '''
        A greedy change-making algorithm without recursion.
        Aims to return the highest possible values.
        Operates on a finite amount of coins (self.bank).
        '''
        if price == cash:
            return 'No change needed'
        else:
            coinsToReturn = []
            rem = cash - price
            for coin in sorted([self.convertStringToCash(i) for i in self.bank.keys()], reverse=True):
                i = 0
                coinStr = self.convertCashToString(coin)
                while i != self.bank[coinStr]: # while there are still coins of this type in the bank
                    if (rem - coin) >= 0:
                        rem -= coin
                        coinsToReturn.append(coinStr)
                        i += 1
                        if rem == 0:
                            return coinsToReturn
                    else:
                        break
            return False
    
class Stock():
    '''
    This class manages the available stock of products.
    The same data structure (self.stock) is used throughout the program, to avoid duplicate code.
    '''
    def __init__(self):
        self.stock = {
            'spam':{'price':2.09, 'qty':1},
            'bread':{'price':1.6, 'qty':2},
            'juice':{'price':1.8, 'qty':3},
            'water':{'price':1.0, 'qty':0}
            }
        
    def reStock(self, product, quantity):
        if product in self.stock.keys():
            try:
                self.stock[product]['qty'] += abs(int(quantity))
                print 'Product(s) added!'
            except:
                print 'Quantity must be a number!'
        else:
            print 'No such item!'
    
    def changeProductPrice(self, product, price):
        if product in self.stock.keys():
            try:
                self.stock[product]['price'] = abs(float(price))
                print 'Price changed!'
            except:
                print 'Price must be a number!'
        else:
            print 'No such item!'
            
    def addNewProduct(self, product, price, quantity):
        try:
            self.stock[product] = {'price':abs(float(price)), 'qty':abs(int(quantity))}
            print 'Product added!'
        except:
            print 'Price and Quantity must be numbers!'
        
    def getCurrentStock(self):
        s = '=== CURRENT STOCK ===\n'
        s += u'Item | £ | Qty\n'
        s += '---------------\n'
        for product, options in self.stock.iteritems():
            s += product + ' | '
            for key, val in options.iteritems():
                s += str(val) + ' | '
            s += '\n'
        s += '====================='
        print s
        
    def getProductPrice(self, product):
        return self.stock[product]['price']*Cash().getPoundScaleFactor()
    
    def getProductQuantity(self, product):
        return self.stock[product]['qty']
    
    def giveItem(self, product):
        self.stock[product]['qty'] -= 1

if __name__ == '__main__':
    machine = VendingMachine()
    machine.run()
    