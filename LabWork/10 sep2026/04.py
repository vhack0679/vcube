class Temperature:
    def __init__(self,t=0):
        self.__temperature=t
    def set_temperature(self,t):
        if t>=-50 and t<100:
            self.__temperature=t
            
        else:
            print("invalid Temperature")
    def get_temperature(self):
        print(self.__temperature)
t=Temperature()
t.set_temperature(30)
t.set_temperature(150)
t.get_temperature()
        
