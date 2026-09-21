class User:
    def __init__(self,u,p):
        self.__username=u
        self.__password=p
    def login(self,u,p):
        if self.__username==u and self.__password==p:
            print("Login Successful")
        else:
            print("Invalid login details")
u=User("admin","python123")
u.login("admin","python123")
