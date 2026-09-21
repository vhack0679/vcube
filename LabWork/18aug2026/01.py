d=dict(map(lambda x:x.split(":"),input().split(",")))
d1={}
for key,value in d.items():
    if value in d1:
        d1[value].append(key)
    else:
        d1[value]=[key]
print(d1)
