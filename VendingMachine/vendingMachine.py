# -*- coding: utf-8 -*-
import time

class VendingMachine():
    def __init__(self):
        self.running = True
        self.Stock = Stock()
        self.Cash = Cash()
        self.help()
        self.Stock.getCurrentStock()
    
    def help(self):
        s = '''
        ============= WELCOME =============
            What would you like to buy?
            
        ================ HELP ================
        Usage:
            1. Type the name of the item
            2. Insert coins in following ways:
                a: all in one row - 1p 10p 50p 1gbp
                b: or enter one-by-one
                
        Accepted coins:
            1p, 2p, 5p, 10p, 20p, 50p, 1gbp
            
        Type 'exit' to quit application
        ======================================
        '''
        print s
    
    def run(self):
        while self.running:
            newSession = False
            item = raw_input('Please input Item Name: ')
            if item in self.Stock.stock.keys():
                qty = self.Stock.getProductQuantity(item)
                if qty == 0:
                    print 'Sorry, this Item is out of stock...'
                else:
                    insertedCash = 0
                    price = self.Stock.getProductPrice(item)
                    while not newSession and self.running:
                        s = raw_input('Please insert Coins: ')
                        if s == 'exit': self.stop()
                        coins = filter(None, s.split())
                        for c in coins:
                            if insertedCash < price:
                                self.Cash.insertCoin(c)
                                cash = self.Cash.convertStringToCash(c)
                                if cash:
                                    insertedCash += cash
                                    if insertedCash >= price:
                                        hasChange = self.Cash.giveChange(price, insertedCash)
                                        if hasChange:
                                            self.giveItem(item)
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
            if item == 'exit': self.stop()
    
    def stop(self):
        if self.running:
            self.Cash.returnCoins()
            print 'Bye! Thank you for shopping!'
            time.sleep(1.5)
            self.running = False
            
    def giveItem(self, product):
        self.Stock.giveItem(product)
        self.Stock.getCurrentStock()
        print "Enjoy your {p}!".format(p=product)

class Cash():
    def __init__(self):
        self.bank = {
            '1p':10,
            '2p':10,
            '5p':10,
            '10p':10,
            '20p':10,
            '50p':10,
            '1gbp':10
            }
        self.coinsInserted = []
        self.poundScaleFactor = 100
    
    def getPoundScaleFactor(self):
        return self.poundScaleFactor
        
    def addToBank(self):
        for coin in self.coinsInserted:
            if coin in self.bank.keys():
                self.bank[coin] += 1
                self.coinsInserted.remove(coin)
        if self.coinsInserted:
            self.returnCoins()
            
    def getAvailableFunds(self):
        return self.bank
    
    def insertCoin(self, string):
        self.coinsInserted.append(string)
        
    def returnCoins(self):
        if self.coinsInserted:
            print 'Returning coins: ' + ', '.join(self.coinsInserted)
            self.coinsInserted = []
                
    def convertStringToCash(self, string):
        if string in self.bank.keys():
            if string.endswith('gbp'):
                c = filter(None, string.split('gbp'))
                return int(c[0])*self.poundScaleFactor
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
        if price == cash:
            return 'No change needed'
        else:
            change = cash - price
            changeStr = self.convertCashToString(change)
            if changeStr in self.bank.keys() and self.bank[changeStr] > 0:
                return changeStr
            coinsToReturn = []
            rem = change
            for coin in sorted([self.convertStringToCash(i) for i in self.bank.keys()], reverse=True):
                i = 0
                coinStr = self.convertCashToString(coin)
                while i != self.bank[coinStr]:
                    if (rem - coin) >= 0:
                        rem -= coin
                        coinsToReturn.append(coinStr)
                        i += 1
                        if rem == 0:
                            return coinsToReturn
                    else:
                        break
            print rem, coinsToReturn
            return False
    
class Stock():
    def __init__(self):
        self.stock = {
            'spam':{'price':2.0, 'qty':0},
            'bread':{'price':1.6, 'qty':2},
            'juice':{'price':1.7, 'qty':3},
            'water':{'price':1.0, 'qty':1}
            }
        
    def reStock(self, product, quantity):
        if product in self.stock.keys():
            self.stock[product]['qty'] += quantity
    
    def changeProductPrice(self, product, price):
        if product in self.stock.keys():
            self.stock[product]['price'] = price
            
    def addNewProduct(self, product, price, quantity):
        self.stock[product]['price'] = price
        self.stock[product]['qty'] = quantity
        
    def getCurrentStock(self):
        s = '=== CURRENT STOCK ===\n'
        s += 'Item | £ | Qty\n'
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