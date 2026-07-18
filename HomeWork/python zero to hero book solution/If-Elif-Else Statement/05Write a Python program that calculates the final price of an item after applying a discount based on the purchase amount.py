#Write a Python program that calculates the final price of an item after applying a discount based on the purchase amount
'''
step1: take price of item
step2: take discount %
sterp3: item amount - discount%
'''
itemamount=int(input("Enter the price of amoutn: "))
discount=float(input("Enter the discount% :"))
dicamount=itemamount*(discount/100)
print(dicamount)
