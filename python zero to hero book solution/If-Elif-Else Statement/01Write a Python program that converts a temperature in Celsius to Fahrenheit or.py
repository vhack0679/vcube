#Write a Python program that converts a temperature in Celsius to Fahrenheit or vice versa based on user input.
'''
step1:take input whether celsius or fahrenheit
step2: if c then take c value
step3 : apply the value in formula to convert fahrenheit
step4: if f then take f value
step5: apply rhe value in formila to convert celsius
'''
opt=input("Enter a C to convert temperature from celsius to fahrenheit or Enter a F to convert temperature from fahrenheit to celsius : ")
if opt.lower()=="c":
    c=float(input("enter celsius value to convert fahrenheit: "))
    f=c*9//5+31
    print(f'{c} celsius to fahrenheit is{f}')
if opt.lower()=="f":
    f=float(input("enter fahrenheit value to convert celsius"))
    c=f-32*5//9
    print(f'{f} fahrenheit to celsius is{c}')
