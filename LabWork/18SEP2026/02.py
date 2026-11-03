d=dict(map(lambda x:x.split(":"),input().split(",")))
pairs=list(d.items())
for i in range(len(pairs)):
    for j in range(i+1,len(pairs)):
        if pairs[i][1]>pairs[j][1]:
            pairs[i],pairs[j]=pairs[j],pairs[i]
print(dict(pairs))
