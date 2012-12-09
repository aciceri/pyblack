from random import shuffle

class Card:
    '''
    This simple class manages single card objects.
    It has not any methods.
    '''
    
    def __init__(self, rank, suit):
        self.rank, self.suit = None, None #Mark and suit are None
        if rank in range(1, 14): #Unless it is in range
            self.rang = rank
        if suit in range(1, 5): #Unless it is in range
            self.suit = suit
            
class Hand:
    '''
    This class manages hands that are lists of card object.
    It has some methods.
    '''
    
    def __init__(self):
        self.cards = [] #The hand is empty
        
    def Add(self, card):
        '''Add a card to the hand at the END'''

        self.cards.append(card)
            
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
            if card.mark > 10: #If it is a figure...
                self.value += 10 #...is value is 10
            elif card.mark == 1: #If it is an ace...
                if ace: #...according to the parameter...
                    self.value += 1 #...his value is 1...
                else:
                    self.value += 11 #...or 11
            else:
                self.value += card.mark #Else his value is the mark

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
                
    def Shuffle(self):
        '''Shuffle the deck though it is empty'''
        
        shuffle(self.cards)
        
        
class Player():
    '''
    This simple class manages player objects.
    It allow to have some simple thing with them,
    like bet or win money.
    '''
    
    def __init__(self):
        self.money = 200
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
    
    def Lose(self):
        '''Lose your bet'''
        
        self.money -= self.bet
        
        
        


