class BankAccount:
    def __init__(self,b):
        self.__balance=b
    def deposit(self,amt):
        if amt>0:
            self.__balance=self.__balance+amt
        else:
            print("enter positive amt")
    def withdraw(self,amt):
        if amt<=self.__balance:
            self.__balance=self.__balance-amt
        else:
            print("ne dagara antyha balance ledhu ra")
    def display_blance(self):
        print('balance=',self.__balance)
account=BankAccount(5000)
account.deposit(2000)
account.withdraw(1500)
account.display_blance()
        
        
