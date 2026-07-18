#Write a Python program that calculates the final price of an item after applying a discount coupon code.
ItemPrice=int(input("enter a iteam price : "))
print("Please enter coupon code as VCUBE45 To get 45% off ")
Coupon=input("enter a coupon code : ")
Code="VCUBE45"
if Coupon==Code:
    Price=ItemPrice*(45/100)
    print(f'You have saved {Price}')
    finalPrice=ItemPrice-Price
    print(f'Total amount to Pay {finalPrice}')

else:
    print("Please enter correct coupon code. ")
