class Payment:
    def pay(self):
        print("payment processing.")
class UPIPayment(Payment):
    def pay(self):
        print("paid using UPI")
obj=UPIPayment()
obj.pay()
