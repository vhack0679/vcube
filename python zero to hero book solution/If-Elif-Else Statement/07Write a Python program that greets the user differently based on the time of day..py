#Write a Python program that greets the user differently based on the time of day.
name=input("enter your name : ")
time=input("enter the current time in HH:MM in 24 hour formate : ")
if time=="" and name=="":
    print("Please enter the name and time")
    
else:
    timesplit=time.split(":")
    hour=int(timesplit[0])
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    elif 17 <= hour < 21:
        greeting = "Good evening"
    elif 22 <= hour <= 23:
        greeting = "Good night"
    else:
        greeting = "Invalid time."
    if name:
        print(f"{greeting}, {name}!")
    else:
        print(f"{greeting}!")
