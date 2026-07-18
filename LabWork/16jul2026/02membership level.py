'''
2. Write a Python program to determine the *membership level* based on reward points.
   *Input:* Reward Points = 850
   *Output:* Gold Member

   *Conditions:*

   * Below 200 → Bronze
   * 200 to 499 → Silver
   * 500 to 999 → Gold
   * 1000 and above → Platinum
   '''
reward_points=int(input("Enter Reward Points :"))
if reward_points<200:
    print("Bronze Member")
elif reward_points<=499:
    print("Silver Menber")
elif reward_points<=999:
    print("Gold Member")
else:
    print("Platinum Member")
