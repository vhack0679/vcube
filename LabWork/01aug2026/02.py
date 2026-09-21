def closercount():
    count=0
    def d():
        nonlocal count
        count=count+1
        return count
    return d
c=closercount()
print(c())
print(c())
print(c())
