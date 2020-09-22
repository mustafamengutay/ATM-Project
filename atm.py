from random import choice   # to create a random Card Number
import sqlite3              # to store customer informations
import time
import sys

# create a database object
conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# create a table
cursor.execute(''' CREATE TABLE IF NOT EXISTS customers
(cardNumber INT PRIMARY KEY, name TEXT, surname TEXT, pin INT, mail TEXT, money REAL)''')
conn.commit()

print("\n", "-"*20, "Welcome to our ATM", "-"*20, "\n\n")

# This function provides to convert a tuple to a string
def tupleToStr(tup): 
    string =  ''.join(tup) 
    return string

# This function provides to exit the program
def exitProgram():
    print("Logging Out...")
    time.sleep(1)
    sys.exit(0)

# ATM Main Menu
def mainMenu(cardNumber):
    cardNum = cardNumber
    print('''
    #############################################################
    #                                                           #
    # *  Select the bank transaction you want to make. (1-6)    #
    #                                                           #
    # 1. View account information                               #
    # 2. Change your pin                                        #
    # 3. Cash withdrawal                                        #                
    # 4. Deposit your cash                                      #
    # 5. Transfer funds between linked bank accounts            #
    # 6. Quit                                                   #
    #                                                           #
    #############################################################
    ''')
    select = int(input("Select: "))

    if select <= 6:
        if select == 1:
            viewAccount(cardNum) # new
        elif select == 2:
            changePin(cardNum)
        elif select == 3:
            withdraw(cardNum)
        elif select == 4:
            deposit(cardNum)
        elif select == 5:
            transfer(cardNum)
        elif select == 6:
            exitProgram()
    else:
        print("Please enter an integer (1-6)")
        mainMenu(cardNumber)

# This function provides to write amount of money.
def amountOfMoney(cardNumber):
    amountOfMoney = cursor.execute("SELECT money FROM customers WHERE cardNumber=?", (cardNumber,))
    myIter = next(iter(amountOfMoney))
    money = float('.'.join(str(myIt) for myIt in myIter))
    print("\nAmount of current balance:", money)

# This function shows customer informations
def viewAccount(cardNumber):
    infoCustomer = tuple(cursor.execute("SELECT * FROM customers WHERE cardNumber=?", (cardNumber,)))
    print("\nPersonal Information")
    print("----------------------------------")
    print("\nCard Number:", infoCustomer[0][0])
    print("Name:", infoCustomer[0][1])
    print("Surname:", infoCustomer[0][2])
    print("PIN:", infoCustomer[0][3])
    print("Mail:", infoCustomer[0][4])
    print("Money:", infoCustomer[0][5])
    print("----------------------------------\n")
    mainMenu(cardNumber)

# This function provides to send money to other bank account.
def transfer(cardNumber):
    amountOfMoney(cardNumber)
    transferCardNumber = input("\nEnter the card number of the account you will send money to: ")
    if transferCardNumber.isdigit() == True:
        transferCardNumber = int(transferCardNumber)
        cursor.execute("SELECT * FROM customers WHERE cardNumber=?", (transferCardNumber,))
        if cursor.fetchone() is not None:
            question = input("\nAre you sure you have entered the correct Card Number? (yes: y / no: n): ").lower()
            if question == "y":
                transferMoney = input("\nEnter an amount of money to send: ")
                if transferMoney.isdigit() or transferMoney.isdecimal() == True:                 
                    cursor.execute("UPDATE customers SET money = money + (?) WHERE cardNumber = ?", (transferMoney, transferCardNumber))
                    cursor.execute("UPDATE customers SET money = money - (?) WHERE cardNumber = ?", (transferMoney, cardNumber))
                    conn.commit()
                    print("\nTransaction Successful!\n")
                    mainMenu(cardNumber)
                else:
                    print("Please enter INTEGER or DECIMAL numbers")
                    transfer(cardNumber)
            elif question == "n":
                transfer(cardNumber)
            else:
                print("Invalid Answer. Try Again.")
                transfer(cardNumber)
        else:
            print("Invalid Card Number, Please Try Again.")
            transfer(cardNumber)
    else:
        print("WRONG Card Number. Please enter the INTEGER Card Number!")
        transfer(cardNumber)

# This function provides to change your PIN
def changePin(cardNumber):
    try:
        newPin = int(input("Enter your new PIN: "))
        cursor.execute("UPDATE customers SET pin = ? WHERE cardNumber=?", (newPin, cardNumber))
        print("\n#############################")
        print("Your new pin:", newPin)
        print("#############################\n")
        conn.commit()
    except:
        print("\nPlease enter integer PIN\n")
        changePin(cardNumber)
    else:
        mainMenu(cardNumber)

# This function provides to deposit your cash
def deposit(cardNumber):
    amountOfMoney(cardNumber)
    try:
        addMoney = float(input("\nHow much money do you want to deposit into your account?: "))
        print("\nThe money is deposited into your account...\n")
        time.sleep(2)
        
        cursor.execute("UPDATE customers SET money = money + (?) WHERE cardNumber=?", (addMoney, cardNumber))
        conn.commit()
        amountOfMoney(cardNumber)
    except:
        print("\nInvalid Value. Please Try Again.")
        deposit(cardNumber)
    else:
        mainMenu(cardNumber)

# This function provides to withdraw from your account
def withdraw(cardNumber):
    amountOfMoney(cardNumber)
    try:
        addMoney = float(input("\nHow much money do you want to withdraw from your account?: "))
        print("\nThe money is being drawn ...\n")
        time.sleep(2)

        cursor.execute("UPDATE customers SET money = money - (?) WHERE cardNumber=?", (addMoney, cardNumber))
        amountOfMoney(cardNumber)
        conn.commit()
    except:
        print("\nInvalid Value. Please Try Again.")
        deposit(cardNumber)
    else:
        mainMenu(cardNumber)

# This function creates an account for customer
def signUp():
    try:
        cardNumber = choice(range(1000, 10000))
        name = input("Enter your name: ").capitalize()
        surname = input("Enter your surname: ").capitalize()
        pin = int(input("Enter a pin: "))
        while True:
            mail = input("Enter a mail (gmail): ")
            if "@gmail.com" in mail:
                break
            else:
                print("\nYou should use Gmail ('@gmail.com') account.\n")
        money = float(input("Enter the amount of money: "))
        cursor.execute(''' INSERT INTO customers VALUES 
        (?, ?, ?, ?, ?, ?)''', (cardNumber, name, surname, pin, mail, money))
        conn.commit()
        infoCustomer = tuple(cursor.execute("SELECT * FROM customers WHERE cardNumber=?", (cardNumber,)))
        print("\nRegistration Successful!\n")
        viewAccount(infoCustomer[0][0])
    except:
        print("Invalid Value. Please Try Again.")
        signUp()
    else:
        mainMenu(cardNumber)

# This function provides to sign in to your account. 
def signIn():
    cardNumber = int(input("Enter your Card Number: "))
    pin = int(input("Enter your PIN: "))
    cursor.execute("SELECT * FROM customers WHERE cardNumber=? AND pin=?", (cardNumber, pin))
    if cursor.fetchone() is not None:
        welcomeName = cursor.execute("SELECT name FROM customers WHERE cardNumber=?",(cardNumber,))
        myIter = iter(welcomeName)
        print("\nWelcome Dear,", tupleToStr(next(myIter)))
        mainMenu(cardNumber)
    else:
        print("\nWRONG Card Number or PIN, Please Try Again.\n")
        signIn()

while True:
    print('''
    ###################################################
    #                                                 #
    #  Sign In (enter 'i')        Sign Up (enter 'u') # 
    #                                                 #
    #                 Exit (enter 'e')                #
    #                                                 #
    ###################################################
    '''.lower())
        
    question = input("Select: ").lower()
    if question == "i":
        signIn()
        break
    elif question == "u":
        signUp()
        break
    elif question == 'e':
        exitProgram()
    else:
        print("Invalid Keyword, Please Try Again.")