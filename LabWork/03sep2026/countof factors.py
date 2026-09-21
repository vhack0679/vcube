n=5
cnt=0
for i in range(1,int(n**0.5)+1):
    if n%i==0:
        cnt+=2
        if i*i==n:
            cnt-=1
print(cnt)
