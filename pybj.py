# -*- coding: utf-8 -*-

from random import shuffle

class Card:
    '''
    This simple class manages single card objects.
    It has not any methods.
    '''
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
            
class Hand:
    '''
    This class manages hands that are lists of card object.
    It has some methods.
    '''
    
    def __init__(self):
        self.cards = [] #The hand is empty
        
    def __str__(self):
        suits = ['♠', '♥', '♦', '♣']
        s = ''
        for card in self.cards:
            s += '- '
            if card.rank <= 10:
                 s += str(card.rank)
            else:
                if card.rank == 11:
                    s += 'J'
                elif card.rank == 12:
                    s += 'Q'
                elif card.rank == 13:
                    s += 'K'
            s += str(suits[card.suit - 1]) + '\n'
        return s
        
    def Add(self, card):
        '''Add a card at the END of the hand'''

        self.cards.append(card)

    def Reset(self):
        '''The hand return to be empty'''
        
        self.cards = []
            
    def Remove(self):
        '''Remove the FIRST card in the hand'''

        if self.cards == []: #If the hand is empty
            return False
        else:
            return self.cards.pop(0)
            
    def Split(self):
        '''Split the hand(if splittable) and return half-hand'''

        if self.cards == []: #If the hand is empty
            return False
        elif len(self.cards) > 2: #If there are more than two cards
            return False
        if self.cards[0].mark == self.cards[1].mark:
            #If there two cards with the same mark
            return self.Remove()
        return False
        
    def Value(self, ace):
        '''Return the value of the deck according to the ace'''
        
        self.value = 0 #The value of the hand is zero at beginning
        for card in self.cards: #For every card in the hand
            if card.rank > 10: #If it is a figure...
                self.value += 10 #...is value is 10
            elif card.rank == 1: #If it is an ace...
                if ace: #...according to the parameter...
                    self.value += 1 #...his value is 1...
                else:
                    self.value += 11 #...or 11
            else:
                self.value += card.rank #Else his value is the mark
        return self.value

class Deck(Hand):
    '''
    This class is inherited from Hand class.
    It manages decks that are like hands.
    It has only a method more.
    '''
    
    def __init__(self):
        self.cards = []
        for mark in range(1, 14): #for every marks
            for suit in range(1, 5): #for every suits
                self.Add(Card(mark, suit)) #Add a card to the deck
                
    def Shuffle(self, times):
        '''Shuffle the deck though it is empty'''
        
        for i in range(times):
            shuffle(self.cards)
        
        
class Player:
    '''
    This simple class manages player objects.
    It allow to have some simple thing with them,
    like bet or win money.
    '''
    
    def __init__(self, money):
        self.money = money
        self.hand = Hand() #Every player has a hand
        
    def Bet(self, bet):
        '''Return true if you can bet'''
        
        if bet > self.money: #If your money is not enough...
            return False #...you can't bet
        else:
            self.bet = bet
            return True
    
    def Win(self):
        '''Win your bet'''
        
        self.money += self.bet * 0.5
        print('You win ' + str(self.bet * 0.5) + '$, so now you have ' + str(self.money) + '$')
    
    def Lose(self):
        '''Lose your bet'''
        
        self.money -= self.bet
        print('You lose ' + str(self.bet) + '$, so now you have ' + str(self.money) + '$')
        
    def Take(self, deck, ncards):
        for i in range(ncards):
            self.hand.Add(deck.Remove())

class Dealer(Player):
    '''
    This is class manages the dealer
    '''

    def __init__(self):
        self.hand = Hand() #Also the dealer has a hand
            
    def Play(self, deck):
        while self.hand.Value(True) < 17:
            self.Take(deck, 1)
 
class Game:
    '''
    This class manages the rules of the game
    '''
    
    def __init__(self):
        self.deck = Deck()
        self.deck.Shuffle(10)
        money = input('How much money do you have? ')
        print('')
        self.player = Player(money)
        self.dealer = Dealer()
        
    def Play(self):
        stillplay = True

        while stillplay: #For every game
            bet = input('What is yout bet? ')
            self.player.Bet(bet)
            self.player.hand.Reset()
            self.dealer.hand.Reset()
            self.player.Take(self.deck, 2)
            self.dealer.Take(self.deck, 1)
            
            print('Value of dealer\'s hand: ' + str(self.dealer.hand.Value(True)))
            print(self.dealer.hand)
            
            stillhit = True
            
            while stillhit:
                print('Value of your hand: ' + str(self.player.hand.Value(True)))
                print(self.player.hand)
                
                hitorstand = raw_input('Do you want Hit or Stand? ')
                
                if hitorstand == 'h':
                    self.player.Take(self.deck, 1)
                    if self.player.hand.Value(True) == 21:
                        print('Value of your hand: ' + str(self.player.hand.Value(True)))
                        print(self.player.hand)
                        print('You make BlackJack')
                        self.player.Win()
                        stillhit = False
                    elif self.player.hand.Value(True) > 21:
                        print('Value of your hand: ' + str(self.player.hand.Value(True)))
                        print(self.player.hand)
                        print('You bust')
                        self.player.Lose()
                        stillhit = False
                elif hitorstand == 's':
                    self.dealer.Play(self.deck)
                    print('Dealer played, the value of his hand is: ' + str(self.dealer.hand.Value(True)))
                    print(self.dealer.hand)
                    if self.dealer.hand.Value(True) > 21:
                        print('The dealer busts')
                        self.player.Win()
                    elif self.dealer.hand.Value(True) > self.player.hand.Value(True):
                        print('The value of dealer\'s hand is higher than your')
                        self.player.Lose()
                    elif self.dealer.hand.Value(True) == self.player.hand.Value(True):
                        print('The value of dealer\'s hand is the same than your')
                        self.player.Lose()
                    elif self.dealer.hand.Value(True) < self.player.hand.Value(True):
                        print('The value of dealer\'s hand is lower than your')
                        self.player.Win()
                    stillhit = False
            
            playagain = raw_input('Do you want play again? ')
            if playagain == 'n':
                #At ththank you for playing with blackjacke end of the game you can play again or not
                print('Thank you for playing')
                stillplay = False
        
        
        
        
        
game = Game()
game.Play()
