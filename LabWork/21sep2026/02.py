def max_after_removal(n, digit):
    s=str(n)
    max_num=0
    for i in range(len(s)):
        if s[i]==str(digit):
            new_num=int(s[:i]+s[i+1:])
            if new_num>max_num:
                max_num=new_num
    return int(max_num)
res=max_after_removal(15435, 5)
print(res)
