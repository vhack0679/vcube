def calculator(n):
    def add(x):
        return x+n
    def sub(x):
        return x-n
    def mul(x):
        return x*n
    return add,sub,mul
add,sub,mul=calculator(5)
print(add(5))
print(sub(3))
print(mul(2))

