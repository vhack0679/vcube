d=dict(map(lambda x:x.split(":"),input().split(",")))
result=[]
for key, value in(d.items()):
    prime=True
    value=int(value)
    for i in range (2,value):
        if value%i==0:
            prime=False
    if prime:
        result.append(key)
print(result)
        
            
