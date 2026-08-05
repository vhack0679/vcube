 #Write a Python program to count how many digits in a given number are multiples
#of 3 using a while loop. Input: 9362481 Output: 4
num=int(input("enter thr number: "))
cnt=0
while num>0:
    digit=num%10
    if digit%3==0:
        cnt=cnt+1
    num=num//10
print(cnt)
