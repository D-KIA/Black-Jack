# You need to create a simple text-based BlackJack game
# The game needs to have one player versus an automated dealer.
# The player can stand or hit.
# The player must be able to pick their betting amount.
# You need to keep track of the player's total money.
# You need to alert the player of wins, losses, or busts, etc...
# random to shuffel

# Header files
import os
import random


# For clearing outputs
def clear():
    os.system('cls')


# Pre-defined variables used to define cards
suit = ['clubs', 'diamonds', 'hearts', 'spades']

rank = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']

# value of ace changes for player
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 11,
          'Queen': 12, 'King': 13, 'Ace': 0}


# card class
class card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# Needs to deal 2 cards each and only 1 dealer card need to be face down
class dealer:
    def __init__(self):
        self.cardlist = []
        self.inhand = []

    def deck(self):
        for s in suit:
            for r in rank:
                self.cardlist.append(card(s, r))

    def shuffel(self):
        random.shuffle(self.cardlist)

    def deal(self):
        return self.cardlist.pop(0)

    def in_hand(self):
        self.inhand.append(self.deal())

    def cvalue(self):
        total = []
        for n in range(len(self.inhand)):
            total.append(values[self.inhand[n].rank])
        return sum(total)


# Needs to place bet and get close to 21
class player:
    def __init__(self, name='', balance=0):
        self.name = name
        self.balance = balance
        self.mycards = []

    def add_card(self, card):
        self.mycards.append(card)

    def remove_card(self):
        self.mycards.pop()

    def bet(self, price):
        self.balance = self.balance - price

    def cvalue(self):
        total = []
        for n in range(len(self.mycards)):
            total.append(values[self.mycards[n].rank])
        return sum(total)


# Game logic
n = input('Enter Name: ')
b = 0
# Asking for Balance
while True:
    try:
        b = int(input('Enter your Balance: '))
    except:
        print('Please enter a numeric value')
        continue
    else:
        break

player1 = player(n, b)
bet = 0
game_on = True
while game_on:

    # Setup for game
    black = dealer()
    black.deck()
    black.shuffel()

    # Place a Bet
    clear()
    # Asking for bet input
    while True:
        try:
            bet = abs(int(input('Please place a bet : ')))
        except:
            print('An error occurred!. A bet need to be a numeric amount under your balance.\nPlease try again!')
            continue
        else:
            if bet > player1.balance:
                print('An error occurred!. A bet need to be a numeric amount under your balance.\nPlease try again!')
                continue
            else:
                break

    # 1st deal
    player1.add_card(black.deal())
    black.in_hand()
    print(f'You get {player1.mycards[0]}')            # 1st card of both player and dealer needs to be printed
    print(f'Dealer gets {black.inhand[0]}')           # 0 is for 1st card taken

    # 2nd deal
    player1.add_card(black.deal())                   # Only players card is to be printed, Dealers will be printed later
    black.in_hand()

    # Player turn
    play = ''
    if player1.mycards[0].rank == 'Ace':
        print(f'You get {player1.mycards[1]}')
        # player's choice for ace
        while True:
            try:
                values['Ace'] = int(input('Pick value for Ace (1/11): '))
            except:
                print('An error occurred!.\nPlease choose between 1 and 11.')
                continue
            else:
                if values['Ace'] not in [1, 11]:
                    print('An error occurred!.\nPlease choose between 1 and 11.')
                    continue
                else:
                    break
    while play not in ['s', 'bust']:
        print(f'You get {player1.mycards[-1]}')
        if player1.mycards[-1].rank == 'Ace':

            # player's choice for ace
            while True:
                try:
                    values['Ace'] = int(input('Pick value for Ace (1/11): '))
                except:
                    print('An error occurred!.\nPlease choose between 1 and 11.')
                    continue
                else:
                    if values['Ace'] not in [1, 11]:
                        print('An error occurred!.\nPlease choose between 1 and 11.')
                        continue
                    else:
                        break
        print(f'You have card total of {player1.cvalue()}')
        play = ''
        if player1.cvalue() > 21:
            print('Bust You Lose !!!!')
            play = 'Bust'
            player1.balance -= bet
            print(f'Your new balance : {player1.balance} ')
            break

        # Player Choice
        while play not in ['s', 'h']:
            play = input('Stand(s) OR Hit(h): ')
        if play == 'h':
            player1.add_card(black.deal())
            continue
        else:

            # Dealer's Turn
            values['Ace'] = 11          # Ace for dealer
            print(f'Dealer gets {black.inhand[-1]}')
            print(f"Dealer's Total: {black.cvalue()}")
            print(f'You have card total of {player1.cvalue()}')

            # Keep adding cards till condition is met
            while black.cvalue() < 21 and black.cvalue() <= player1.cvalue():
                black.in_hand()
                print(f'Dealer gets {black.inhand[-1]}')
                print(f"Dealer's Total: {black.cvalue()}")

            # Winning and losing
            if black.cvalue() > 21:
                player1.balance += 2 * bet
                print(f'Dealer is Bust, You WIN !!!.\nYour New Balance: {player1.balance}')
            elif black.cvalue() > player1.cvalue():
                player1.balance -= bet
                print(f'Dealer Wins !!!\nYour New Balance: {player1.balance}')
            else:
                print('Tie (Both have 21)')
        values['Ace'] = 0       # resetting value of Ace
    # Asking if player want to continue
    while True:
        try:
            play_again = input('Wanna Continue (y,n): ')
        except:
            print('Chose Between y or n')
            continue
        else:
            if play_again == 'y':
                break
            else:
                exit()
    player1.mycards.clear()
    black.inhand.clear()
