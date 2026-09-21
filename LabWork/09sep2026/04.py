'''
Create a class Mobile with attributes brand, model, and price.
Create an object and display the mobile details.
Input: brand = "Samsung" model = "A55" price = 30000 Output: Brand: Samsung Model: A55 Price: 30000
'''
class Mobile:
    def __init__(self,b,m,p):
        self.brand=b
        self.model=m
        self.price=p
    def info(self):
        print('brand:',self.brand,'model:',self.model,'price:',self.price)
obj1=Mobile("Samsung","A55",30000)
obj1.info()
