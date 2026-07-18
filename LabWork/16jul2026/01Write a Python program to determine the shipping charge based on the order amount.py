'''1. Write a Python program to determine the *shipping charge* based on the order amount.
   *Input:* Order Amount = ₹1800
   *Output:* Shipping Charge = ₹50

   *Conditions:*

   * Below ₹500 → ₹100
   * ₹500 to ₹1999 → ₹50
   * ₹2000 and above → Free Shipping
   '''

orderamount=int(input("Enter Order Amount :₹"))
if orderamount<500:
    print("Shipping Charge = ₹100")
elif orderamount<=1999:
    print("Shipping Charge = ₹50")
else:
    print("Free Shipping")
