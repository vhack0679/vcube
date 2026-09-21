'''
Create a BankAccount class with attributes account_number, owner_name, and balance.
Add methods to deposit, withdraw,
 and check balance. 
'''
class BankAccount:
    def __init__(self,accno,ownername,balance):
        self.account_number=accno
        self.owner_name=ownername
        self.balance=balance
    def deposit(self,amt):
        self.amt=amt
        if self.amt>0:
            self.balance=self.balance+self.amt
        else:
            print("deposit only correct amount")
        

    def withdraw(self,amt):
        self.amt=amt
        if self.amt>0:
            self.balance=self.balance-self.amt

    def check_balance(self):
        print(self.balance)
        
obj=BankAccount(6301123051,"vishal",1000)
obj.check_balance()
