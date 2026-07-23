#Write a Python program that determines the number of days in a given month
print("Plz Enter in this formate jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov and dec ")
month=input("Enter The Month :").lower()
if month=="jan":
    print("31 Days")
elif month=="feb":
    print("28days")
elif month=="mar":
    print("31 days")
elif month=="apr":
    print("30 days")
elif month=="may":
    print("31 days")
elif month=="jun":
    print("30 days")
elif month=="jul":
    print("31 days")
elif month=="aug":
    print("31 days")
elif month=="sep":
    print("30 days")
elif month=="oct":
    print("31 days")
elif month=="nov":
    print("30 days")
elif month=="dec":
    print("31 days")
else:
    print("Enter the month in valid formate and you  incorrect month")
