print(r'''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\ ` . "-._ /_______________|_______
|                   | |o ;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
''')
print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.")

print("You come to a fork on the road. Which way should you go?")
direction = input("      Type \"left\" or \"right\".\n").lower()
if direction == "left":
    print("You've come to a small lake. You see an island in the middle of the lake.")
    decision = input("      Type \"wait\" to wait for a boat. Type \"swim\" to swim to the island.\n").lower()
    if decision == "wait":
        print("You made it to the island and come across a house with 3 doors.")
        door = input("      One \"red\", one \"yellow\", and one \"blue\". Which color do you choose?\n").lower()
        if door == "yellow":
            print("You enter the room full of treasure! YOU WIN!!!")
        elif door == "red":
            print("You enter the room of fire! GAME OVER!!!")
        elif door == "blue":
            print("You enter the room of beasts! GAME OVER!!!")
        else:
            print("You fall into a trap door! GAME OVER!!!")
    else:
        print("You get eaten by a giant trout! GAME OVER!!!")
else:
    print("Your partner betrays you, steals the map and stabs you in the back! GAME OVER!!!")
