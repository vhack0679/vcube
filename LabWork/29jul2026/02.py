n=int(input("Enter a number: ")) 
for i in range(2,n+1):
    last_digit=i%10
    if last_digit==2 or last_digit==3 or last_digit==4 or last_digit==5 or last_digit==7:
        print(i, end=" ")
