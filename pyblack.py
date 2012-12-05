# -*- coding: utf-8 -*-

class Carta:
	'''Classe per la gestione dell''oggetto carta'''
	
	lvalori = [None, 'Uno', 'Due', 'Tre', 'Quattro', 'Cinque', 'Sei', 'Sette', 'Otto', 'Nove', 'Dieci', 'Jack', 'Donna', 'Re']
	lsemi = ['Cuori', 'Quadri', 'Fiori', 'Picche']
	
	def __init__(self, valore = 0, seme = 0): #Crea un oggetto carta(0 di Cuori di default)
		self.valore = valore
		self.seme = seme
	
	def __str__(self): #Ritorna un stringa del tipo 'Tre di Quadri'
		return str(self.lvalori[self.valore]) + ' di ' + str(self.lsemi[self.seme])
			
	def Valore(self): #Ritorna il valore della carta(secondo le regole del BlackJack)
		if self.valore <= 10:
			return self.valore
		elif self.valore > 10:
			return 10
		else:
			return 0
	
class Mazzo:
	'''Classe per la gestione dell'oggetto mazzo'''
	
	def __init__(self, nmazzi = 2): #Popola il mazzo con una sequenza ordinata di oggetti Carta()
		self.carte = []
		for n in range(nmazzi):  #Per il numero di mazzi del sabot
			for i in range(0, 4): #Per ogni seme
				for j in range(1, 14): #Per ogni valore
					self.carte.append(Carta(j, i)) #Aggiungi la carta al mazzo
				
	def __str__(self): #Ritorna un stringa contenente tutte le carte del mazzo(andando a capo)
		s = ''
		for i in self.carte:
			s += str(i) + '\n'
		return s
	
	def Mischia(self, volte = 10): #Riordina casualmente la lista di oggetti Carta()
		import random
		ncarte = len(self.carte)
		for n in range(volte):
			for i in range(0, ncarte):
				j = random.randrange(i, ncarte)
				self.carte[i], self.carte[j] = self.carte[j], self.carte[i]
	
	def Vuoto(self): #Ritorna True se il mazzo è vuoto oppure False se è presente almeno una carta
		if self.carte == []:
			return True
		else:
			return False
	
	def Pesca(self): #Ritorna l'ultimo oggetto Carta() del mazzo e lo rimuove da esso
		return self.carte.pop()
		
	def Distribuisci(self, mano, ncarte): #Aggiunge ad una mano n carte togliendole dal mazzo
		for i in range(ncarte):
			mano.Aggiungi(self.Pesca())
			
class Mano:
	'''Classe per la gestione dell'oggetto mano'''
	
	def __init__(self): #Crea una lista vuota che conterrà le carte
		self.carte = []
	
	def __str__(self): #Ritorna un stringa contenente tutte le carte della mano(andando a capo)
		s = ''
		for i in self.carte:
			s += '-' + str(i) + '\n'
		return s
	
	def Aggiungi(self, carta): #Aggiunge una carta alla mano
		self.carte.append(carta)
		
	def Valore(self): #Ritorna la somma dei valori di tutte le carte della mano
		s = 0
		for carta in self.carte:
			s += carta.Valore()
		return s
	
	def Svuota(self): #Elimina tutte le carte presenti in una mano
		self.carte = []	
		
class Giocatore:
	'''Classe per la gestione dell'oggetto giocatore'''

	def __init__(self, nome = '', soldi = 0): #Attribuisce un nome, dei soldi ed una mano ad un giocatore
		self.nome = nome
		self.soldi = soldi
		self.soldiiniziali = soldi
		self.mano = Mano()
	
	def Scommetti(self, scommessa): #Se si hanno abbastanza soldi scommette e ritorna vero, altrimenti ritorna falso
		if scommessa > self.soldi:
			return False
		else:
			self.scommessa = scommessa
			self.soldi -= scommessa
			return scommessa
	
	def Perdiscommessa(self): #La scommessa va a 0
		self.scommessa = 0
		
	def Vinciscommessa(self): #I soldi vengono aggiornati in base alla scommessa che poi viene azzerata
		self.soldi += self.scommessa * 1.5
		self.scommessa = 0
		
class Blackjack:
	'''Classe per la gestione dell'oggetto blackjack, ossia la partita'''
	
	def __init__(self): #Inzializzazione della partita
		print('Benvenuto in PyBlack, la mia implementazione libera di BlackJack scritta in Python')
		print('Se riscontri errori sentiti libero di scrivermi a questa email: andreaciceri96@gmail.com')
		print('---Avvio partita---')
		print('')
		giocatore = raw_input('Qual è il tuo nome? ')
		soldi = input('Con quanti soldi vuoi cominciare il gioco? ')
		
		self.giocatore = Giocatore(giocatore, soldi) #Instanzia il giocatore tramite i parametri scelti
		self.banco = Giocatore() #Instanzia il banco senza darli nè nome nè soldi
		self.mazzo = Mazzo() #Instanzia il mazzo(un sabot da 2 mazzi di default)
		self.mazzo.Mischia() #Mischia il mazzo(dieci volte di default)
		
	def Gioca(self):
		self.giocatore.mano.Svuota() #Vengono eliminate tutte le carte della mano del giocatore
		self.banco.mano.Svuota() #Vengono eliminate tutte le carte della mano del banco
		print('')
		scommessa = input('Quanto vuoi scommettere? ')
		self.giocatore.Scommetti(scommessa) #Il giocatore scommette
		self.mazzo.Distribuisci(self.giocatore.mano, 2) #Vengono date due carte al giocatore
		self.mazzo.Distribuisci(self.banco.mano, 1) #Viene data una carta al banco
		print('')
		print('Ricevi due carte: (somma: ' + str(self.giocatore.mano.Valore()) + ')')
		print(self.giocatore.mano)
		print('Il banco ha una carta:')
		print(self.banco.mano)
		self.Scegli()
		

	def Scegli(self):
		scelta = raw_input('Vuoi chiedere carta o stare? (digita "c" o "s") ')
		if scelta == 'c':
			self.Chiedi()
		elif scelta == 's':
			self.Stai()
		
	def Chiedi(self):
		while self.giocatore.mano.Valore() <= 21:
			self.mazzo.Distribuisci(self.giocatore.mano, 1)
			print('')
			print('Ricevi una carta, ora le tue carte sono: (somma: ' + str(self.giocatore.mano.Valore()) + ')')
			print(self.giocatore.mano)
			if self.giocatore.mano.Valore() > 21:
				print('Hai perso perché hai sballato')
				self.Perso()
			elif self.giocatore.mano.Valore() == 21:
				print('Hai vinto perché hai fatto 21')
				self.Vinto()
			else:
				self.Scegli()
		
	def Stai(self):
		self.Regolabanco()
		if self.banco.mano.Valore() > 21:
			print('Hai vinto perché il banco ha sballato')
			self.Vinto()
		elif self.giocatore.mano.Valore() > self.banco.mano.Valore():
			print('Hai vinto perché hai fatto un punteggio più alto del banco')
			self.Vinto()
		elif self.giocatore.mano.Valore() == self.banco.mano.Valore():
			print('Hai perso perché hai fatto lo stesso punteggio del banco')
			self.Perso()
		else:
			print('Hai perso perché il banco ha fatto un punteggio più alto del tuo')
			self.Perso()
		
	def Regolabanco(self):
		n = 0
		while self.banco.mano.Valore() < 17:
			self.mazzo.Distribuisci(self.banco.mano, 1)
			n += 1
		print('')
		print('Il banco pesca ' + str(n) + ' carte, ora le sue carte sono: (somma:' + str(self.banco.mano.Valore()) + ')')
		print(self.banco.mano)
		
	def Vinto(self):
		print('Avevi scommesso ' + str(self.giocatore.scommessa) + '$ e hai vinto ' + str(self.giocatore.scommessa * 1.5) + '$, quindi ora hai ' + str(self.giocatore.soldi + self.giocatore.scommessa * 1.5) + '$')
		self.giocatore.soldi += self.giocatore.scommessa * 1.5
		self.giocatore.scommessa = 0
		print('')
		self.Rigioca()
		
	def Perso(self):
		print('Avevi scommesso ' + str(self.giocatore.scommessa) + '$ e hai perso, quindi ora hai ' + str(self.giocatore.soldi) + '$')
		self.giocatore.scommessa = 0
		print('')
		self.Rigioca()
				
	def Rigioca(self):
		print('')
		scelta = raw_input('Vuoi rigiocare? ("s" o "n") ')
		if scelta == 's':
			self.Gioca()
		else:
			print('Quando hai iniziato a giocare avevi ' + str(self.giocatore.soldiiniziali) + '$ e ora hai ' + str(self.giocatore.soldi) + '$')
			exit()
		

partita = Blackjack()
partita.Gioca()
