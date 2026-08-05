#list data Structure with Dummy Data
#here i used nested list for this application
movies = ["Kalki 2","Pushpa 2","War 2"]
shows = [["Kalki 2", "10:00 AM"],["Kalki 2", "2:00 PM"],["Pushpa 2", "11:00 AM"],["War 2", "6:30 PM"]]
seats = [[["Kalki 2", "10:00 AM"],[["S1","A"], ["S2","B"], ["S3","A"], ["S4","A"], ["S5","B"],["S6","A"], ["S7","A"], ["S8","A"], ["S9","B"], ["S10","A"]]],]
bookings = [["Vishal", "Kalki 2", "10:00 AM", "S2"],["Rahul", "Pushpa 2", "11:00 AM", "S8"],["Sneha", "War 2", "6:30 PM", "S3"],["Ajay", "Kalki 2", "2:00 PM", "S4"]]
users = [["Vishal", "Vishal@123"], ["Rahul", "Rahul@123"],["Sneha", "Sneha@123"],["Ajay", "Ajay@123"]]
print("*"*16,"Welcome to VCube Movie Booking System","*"*16)
#Admin or user options
while True:
    print('='*70)
    print(' '*30,'MENU',' '*30)
    print('='*70)
    print("1.Admin")
    print("2.User")
    print("3.Close")
    print('='*70)
    Authentication_option=int(input("Choose 1 or 2 or 3 options : "))
    print('='*70)
#Admin menus --------------------------------------------------------------------------------------------------
    if Authentication_option==1:
        User_Name_Authentication=input("Enter the user name:")
        User_password_authentication=input("Enter the password :")
        if User_Name_Authentication=='Admin' and User_password_authentication=='Admin@123':
            print()
            print("Welcome, Admin")
            print()
            while True:
                print('='*70)
                print(' '*30,'ADMIN MENU',' '*30)
                print('='*70)
                print('1. Add Movie')
                print('2. Add Show')
                print('3. Manage Seats')
                print('4. Delete Movie/Show')
                print('5. View Bookings')
                print('6. Logout')
                print('='*70)
                Admin_menu_option=int(input('Choose option 1 or 2 or 3 or 4 or 5 or 6: '))
#Admin menus operations ---------------------------------------------------------------------------------------------
                if Admin_menu_option==1:
                    Movie_name=input("Enter the movie name :")
#Add Movie-----------------------------------------------------------------------------------------------
                    if Movie_name in movies:
                        print(f'{Movie_name} Already exists ')
                    else:
                        movies.append(Movie_name)
                    print(f'{Movie_name} Movie Added  successfully')
#--------------------------------------------------------------------------------------------------------
                elif Admin_menu_option==2:
#Add Shows-----------------------------------------------------------------------------------------------
                    if len(movies)==0:
                        print("No movies available. Please add a movie first.")
                    else:
                        for i in range(len(movies)):
                            print(f'{i+1}.{movies[i]}')   
                        selected_movie=int(input("Select Movie Number: "))
                        if 1<=selected_movie<=len(movies):
                            show_time=input("Enter Show Time: ")
                            shows.append([movies[selected_movie - 1], show_time])
                            print("Show Added Successfully")
                        else:
                            print("Invalid Movie Selection")
#--------------------------------------------------------------------------------------------------------
                elif Admin_menu_option==3:
                    print('='*70)
                    print(' '*30,'Manage Seats',' '*30)
                    print('='*70)
                    print("1.Add Seat Layout")
                    print("2.Update Seat Layoout")
                    manage_seats_option=int(input("Choose option 1 or 2 "))
                    if manage_seats_option==1:
                        for i in range(len(shows)):
                            print(f'{i+1}.{shows[i][0]} - {shows[i][1]}')   
                        select_show_time_movie=int(input("Select Show time to add seat Layout"))
                        if 1<=select_show_time_movie<=len(shows):
                            total_seats=int(input("Enter Number of Seats : "))
                            seat_list=[]
                            for i in range(1,total_seats+1):
                                seat_list.append(["S"+str(i),"A"])
                            seats.append([shows[select_show_time_movie-1], seat_list])
                            print("Seat Layout Created Successfully")
                        else:
                            print("Invalid Show")
                    elif manage_seats_option==2:
                        if len(seats)==0:
                            print("No Seat Layout Available")
                        else:
                            print("="*70)
                            print("Available Shows")
                            print("="*70)
                            for i in range(len(seats)):
                                print(f"{i+1}. {seats[i][0][0]} - {seats[i][0][1]}")
                            select=int(input("Select Show : "))
                            if 1<=select<=len(seats):
                                print("="*70)
                                print(' '*30,"SCREEN",' '*30)
                                print("="*70)
                                count=0
                                for seat in seats[select-1][1]:
                                    print(f" {seat[0]}({seat[1]})",end="\t")
                                    count+=1
                                    if count%5==0:
                                        print()
                                print()
                                print(f"A = Available    B = Booked")
                                seat_number=input("\nEnter Seat Number to Block : ").upper()
                                found=False
                                for seat in seats[select-1][1]:
                                    if seat[0]==seat_number:
                                        seat[1]="B"
                                        found=True
                                        print("Seat Blocked Successfully")
                                        break
                                if found==False:
                                     print("Seat Not Found")
                    else:
                        print("Invalid Option")
                    
                elif Admin_menu_option==4:
                    print("="*70)
                    print("Delete Menu")
                    print("="*70)
                    print("1.Delete Movie")
                    print("2.Delete Show")
                    delete_option=int(input("Choose Option : "))
                    if delete_option==1:
                        print("="*70)
                        print("Delete Movie")
                        print("="*70)
                        if len(movies)==0:
                            print("No Movies Available")
                        else:
                            for i in range(len(movies)):
                                print(f"{i+1}. {movies[i]}")
                            delete_movie=int(input("Select Movie Number : "))
                            if 1<=delete_movie<=len(movies):
                                movie_name=movies[delete_movie-1]
                                movies.pop(delete_movie-1)
                                i=0
                                while i<len(shows):
                                    if shows[i][0]==movie_name:
                                        shows.pop(i)
                                    else:
                                        i+=1
                                i=0
                                while i<len(seats):
                                    if seats[i][0][0]==movie_name:
                                        seats.pop(i)
                                    else:
                                        i+=1
                                print("Movie Deleted Successfully")
                            else:
                                print("Invalid Movie")
                    elif delete_option==2:
                        print("="*70)
                        print("Delete Show")
                        print("="*70)
                        if len(shows)==0:
                            print("No Shows Available")
                        else:
                            for i in range(len(shows)):
                                print(f"{i+1}. {shows[i][0]} - {shows[i][1]}")
                                delete_show=int(input("Select Show Number : "))
                            if 1<=delete_show<=len(shows):
                                deleted_show=shows[delete_show-1]
                                deleted_show=shows[delete_show-1]
                                i=0
                                while i<len(seats):
                                    if seats[i][0]==deleted_show:
                                        seats.pop(i)
                                    else:
                                        i+=1
                                print("Show Deleted Successfully")
                            else:
                                 print("Invalid Show")
                    else:
                         print("Invalid Option")
                elif Admin_menu_option==5:
                    print("="*70)
                    print("All Bookings")
                    print("="*70)
                    if len(bookings)==0:
                        print("No Bookings Available")
                    else:
                        for booking in bookings:
                            print(f"""
                User  : {booking[0]}
                Movie : {booking[1]}
                Show  : {booking[2]}
                Seat  : {booking[3]}
                ----------------------------------
                """)
                elif Admin_menu_option==6:
                    print("Logging out.........")
                    break
                else:
                    print("Invalid option")
        else:
            print("Invalid username or password")
#User menus---------------------------------------------------------------------------------------------      
    elif Authentication_option==2:
        User_Name_Authentication=input("Enter the user name:")
        User_password_authentication=input("Enter the password :")
        login_success = False
        for user in users:
            if user[0]==User_Name_Authentication and user[1]==User_password_authentication:
                login_success = True
                print()
                print(f"Welcome, {User_Name_Authentication}")
                print()
                while True:
                    print('='*70)
                    print(' '*30,'User MENU',' '*30)
                    print('='*70)
                    print('1. View Movie')
                    print('2. View Booking')
                    print('3. Logout')
                    print('='*70)
                    user_selection=int(input("Choose Option 1 or 2 or 3"))
#user menu operations------------------------------------------------------------------------------------
                    if user_selection==1:
                        for i in range(len(movies)):
                            print(f'{i+1}.{movies[i]}')
                        movie_selection=int(input("Select you movie option"))
                        if 1<=movie_selection<=len(movies):
                            mm=movies[movie_selection-1]
                            print()
                            print(f'You selected {mm}')
                            print()
                            print('='*70)
                            print('Show Timings')
                            print('='*70)
                            print()
                            available_shows=[]
                            for i in range(len(shows)):
                                if mm==shows[i][0]:
                                    available_shows.append(shows[i])
                                    print(f"{len(available_shows)}. {shows[i][1]}")
                            show_selection=int(input("\nSelect Show : "))
                            if 1<=show_selection<=len(available_shows):
                                selected_show=available_shows[show_selection-1]
                                seat_layout=None
                                for seat in seats:
                                    if seat[0]==selected_show:
                                        seat_layout=seat[1]
                                        break
                                if seat_layout is None:
                                    print("Seat Layout Not Created By Admin")
                                else:
                                    print("="*70)
                                    print(" "*30+"SCREEN")
                                    print("="*70)
                                    count = 0
                                    for seat in seat_layout:
                                        print(f"{seat[0]}({seat[1]})", end="\t")
                                        count+=1
                                        if count % 5 == 0:
                                            print()
                                    print()
                                    print("A = Available    B = Booked")
                                    seat_number = input("\nEnter Seat Number : ").upper()
                                    found = False
                                    for seat in seat_layout:
                                        if seat[0]==seat_number:
                                            found=True
                                            if seat[1]=="A":
                                                seat[1]="B"
                                                bookings.append([
                                                    User_Name_Authentication,
                                                    mm,
                                                    selected_show[1],
                                                    seat_number
                                                ])
                                                print("\nBooking Successful")
                                            else:
                                                print("Seat Already Booked")
                                            break
                                    if found==False:
                                        print("Invalid Seat Number")
                            else:
                                print("Invalid Show Selection")                            

                    elif user_selection==2:
                            print("="*70)
                            print("Your Bookings")
                            print("="*70)
                            found=False
                            for booking in bookings:
                                if booking[0]==User_Name_Authentication:
                                    found = True
                                    print(f"""
                        Movie : {booking[1]}
                        Show  : {booking[2]}
                        Seat  : {booking[3]}
                        -----------------------------------
                        """)
                            if found==False:
                                print("No Bookings Found")
                    elif user_selection==3:
                        print("Logging out.........")
                        break
                    else:
                        print("Invalid option") 
        if login_success == False:
            print("Invalid Username or Password")
#-------------------------------------------------------------------------------------------------------
    elif Authentication_option==3:
        print("Thank you For Using VCube Movie Booking System")
        break
    else:
        print("Invalid option")

    

    

    
    
    
    
