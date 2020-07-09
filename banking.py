import random
import sqlite3
conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
# cur.execute("drop table card;")
# cur.execute('create table card (id integer , number varchar(20) , pin varchar(20) , balance integer default 0 );')
conn.commit()


def put_values(id , number , pin , balance):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    query = f'''insert into card (id , number , pin , balance) values ( {id} , {number} , {pin} , {balance} );'''
    cur.execute(query)
    conn.commit()

def Luhn(number):
    num_list = []
    for x in number:
        num_list.append(int(x))
    num_list1 = num_list[:15]

    for x in range(0, 15, 2):
        num_list1[x] = num_list1[x] * 2

    num_list2 = []
    for x in num_list1:
        if x > 9:
            y = x - 9
            num_list2.append(y)
        else:
            num_list2.append(x)

    sum = num_list[15]
    for x in num_list2:
        sum += x

    return sum % 10 == 0

def card_info():
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    query = f'''select number from card'''
    cur.execute(query)
    list1 = cur.fetchall()
    new = []
    for x in list1:
        new.append(x[0])
    # print(list1)
    return new

def pin_info():
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    query = f'''select pin from card'''
    cur.execute(query)
    list1 = cur.fetchall()
    new = []
    for x in list1:
        new.append(x[0])
    # print(list1)
    return new




def info():
    query = '''select * from card'''
    cur.execute(query)
    list1 = cur.fetchall()
    return list1

def balance(number):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    query = f'''select balance from card where number = {number}'''
    cur.execute(query)
    list1 = cur.fetchall()
    # print(list1)
    new_balance = []
    for x in list1:
        new_balance.append(x[0])
    return new_balance[0]

def add_income(number , amount):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    query = f'''update card set balance = balance +  {amount} where number = {number}'''
    cur.execute(query)
    conn.commit()


def close(number):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    query = f'''delete from card where number = {number}'''
    cur.execute(query)
    conn.commit()

def transfer(card_num , trans_card , amount):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    query = f'''update card set balance = balance + {amount} where number = {trans_card}'''
    cur.execute(query)
    query2 = f'''update card set balance = balance - {amount} where number = {card_num}'''
    cur.execute(query2)
    conn.commit()








k = 1
i = 1
while k != 0:
    print('''1. Create an account
2. Log into account
0. Exit''')
    k = input()
    if k == '1':
        pin_gen = random.randint(1000, 9999)
        l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(l1)
        l1 = [str(x) for x in l1]
        card_gen = '400000' + "".join(l1) + "5"
        card_gen = int(card_gen)
        boo = Luhn(str(card_gen))
        if boo == False:
            l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            random.shuffle(l1)
            l1 = [str(x) for x in l1]
            card_gen = '400000' + "".join(l1) + "5"
            card_gen = int(card_gen)
            k = 0
            while k != 1:
                boo1 = Luhn(str(card_gen))
                if boo1 == True:
                    k = 1
                else:
                    random.shuffle(l1)
                    l1 = [str(x) for x in l1]
                    card_gen = '400000' + "".join(l1) + "5"
                    card_gen = int(card_gen)
                    k = 0
        put_values(i , card_gen , pin_gen , 0)
        print(f'''\nYour card has been created
Your card number:
{card_gen}
Your card PIN:
{pin_gen}\n''')
        i +=1
    elif k == '2':
        card_num = int(input("\nEnter your card Number:\n"))
        pin_num = int(input("Enter your PIN:\n"))
        cards = card_info()
        pins = pin_info()
        # print(cards , pins)
        if str(card_num) in cards and str(pin_num) in pins:
            print("\nYou have successfully logged in!\n")

            m = 1
            while m != 0:
                m = int(input('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit\n'''))
                balance_acc = balance(card_num)
                if m == 1:
                    bal = balance(card_num)
                    print(f"\nBalance: {bal}\n")

                elif m == 2:
                    check = int(balance(card_num))
                    amount = int(input("\nEnter income:\n"))
                    add_income(card_num , amount)
                    print("Income was added!\n")

                elif m == 4:
                    close(card_num)
                    print("The account has been closed!")
                    m = 0

                elif m == 3:
                    trans_card = int(input("Enter card number:\n"))
                    cards = card_info()
                    # print(cards)
                    check_trans = Luhn(str(trans_card))
                    check_balance = balance(card_num)

                    if check_trans == False:
                        print("Probably you made mistake in the card number. Please try again!\n")

                    elif trans_card == card_num:
                        print("You can't transfer money to the same account!\n")

                    elif str(trans_card) in cards:
                        money = int(input("Enter how much money you want to transfer:\n"))
                        amount_in = balance(card_num)
                        if money <= amount_in:
                            transfer(card_num, trans_card, money)
                            print('Success!\n')
                        else:
                            print("Not enough money!\n")


                    elif str(trans_card) not in cards:
                        print("Such a card does not exist.\n")

                    elif check_balance == 0:
                        print("Not enough money!\n")



                    # else:
                    #     print("Such a card does not exist.\n")

                elif m == 5:
                    print("\nYou have successfully logged out!\n")
                    m = 0
                elif m == 0:
                    exit()

                elif balance_acc <= 0:
                    print("Not enough money!\n")



        else:
            print("\nWrong card number or PIN!\n")

    elif k == "0":
        # print(info())
        print("\nBye!")
        exit()
