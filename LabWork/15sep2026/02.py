class Mobile:
    def power_on(self):
        print("Powerd On")
class SmartPhone(Mobile):
    def use_app(self):
        print("Using Instagram")
obj=SmartPhone()
obj.power_on()
obj.use_app()
