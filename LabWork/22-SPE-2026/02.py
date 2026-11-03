'''

Write a function max_product_number(n) that finds the maximum product of two adjacent digits
in a given number and returns both the digits and their product.
Input: n = 58392641 Output: Digits: 92 Product: 18
'''
def max_product_number(n):
    n=str(n)
    currentval=int(n[0])
    max_prod=0
    max_digits=""
    for i in range(1,len(n)):
        prd=currentval*int(n[i])
        if prd>max_prod:
            max_prod=prd
            max_digits = n[i - 1] + n[i]
            
        currentval=int(n[i])
    
    return int(max_digits),max_prod
print(max_product_number(58392641))
        
        
