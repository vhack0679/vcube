def create_counter(n):
    num=n
    def d(z):
        nonlocal num
        num=num+z
        return num
    return d
c = create_counter(10)
print(c(5))
print(c(3))
print(c(7))
        
        
