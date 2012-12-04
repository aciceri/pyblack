class carta:
	lvalori = [None, 'Uno', 'Due', 'Tre', 'Quattro', 'Cinque', 'Sei', 'Sette', 'Otto', 'Nove', 'Dieci', 'Jack', 'Donna', 'Re']
	lsemi = ['Cuori', 'Quadri', 'Fiori', 'Picche']
	
	def __init__(self, valore = 0, seme = 0):
		self.valore = valore
		self.seme = seme
	
	def __str__(self):
		return str(self.lvalori[self.valore]) + ' di ' + str(self.lsemi[self.seme])
		
	def __add__(self, altracarta): #la somma di due carte da sempre una carta di cuori
		return carta(self.valore + altracarta.valore, 1)
		
	def __cmp__(self, altracarta):
		if self.valore > altracarta.valore:
			return 1
		elif self.valore < altracarta.valore:
			return -1
		else:
			return 0
			
	def ritornavalore(self):
		if self.valore <= 10:
			return self.valore
		elif self.valore >= 11:
			return 10
		else:
			return 0
	
class mazzo:
	carte = []
	
	def __init__(self, nmazzi = 2):
		for n in range(nmazzi):
			for i in range(0, 4):
				for j in range(1, 14):
					self.carte.append(carta(j, i))
				
	def __str__(self):
		s = ''
		for i in self.carte:
			s += str(i) + '\n'
		return s
	
	def mescola(self, volte = 10):
		import random
		ncarte = len(self.carte)
		for n in range(volte):
			for i in range(0, ncarte):
				j = random.randrange(i, ncarte)
				self.carte[i], self.carte[j] = self.carte[j], self.carte[i]
	
	def vuoto(self):
		if self.carte == []:
			return True
		else:
			return False
	
	def pesca(self):
		return self.carte.pop()
		
	def distribuisci(self, mano, ncarte):
		for i in range(ncarte):
			mano.aggiungi(self.pesca())
			

class mano:
	
	def __init__(self):
		self.carte = []
	
	def __str__(self):
		s = ''
		for i in self.carte:
			s += str(i) + '\n'
		return s
	
	def aggiungi(self, carta):
		self.carte.append(carta)
		
	def valore(self):
		s = 0
		for carta in self.carte:
			s += carta.ritornavalore()
		return s
	
	def svuota(self):
		self.carte = []	
		
class giocatore:

	def __init__(self, nome, soldi):
		self.nome = nome
		self.soldi = soldi
		self.mano = mano()
		
	def __str__(self):
		return str(self.nome) + ' con fondo di ' + str(self.soldi) + '$'
	
	def scommetti(self, scommessa):
		if scommessa > self.soldi:
			return False
		else:
			self.scommessa = scommessa
			self.soldi -= scommessa
			return scommessa
		
		
class blackjack:
	
	def __init__(self):
		self.giocatore = giocatore(raw_input('Come ti chiami? '), input('Con quanti soldi vuoi iniziare? '))
		self.banco = giocatore('Banco', 0)
		self.mazzo = mazzo()
		self.mazzo.mescola()
		
	def gioca(self):
		self.giocatore.mano.svuota() #viene svuotata la mano del giocatore
		self.banco.mano.svuota() #viene svuotata la mano del banco
		self.giocatore.scommetti(input('Quanto vuoi scommettere? ')) #il giocatore sceglie quanto scommettere
		self.mazzo.distribuisci(self.giocatore.mano, 2) #vengono date due carte al giocatore
		self.mazzo.distribuisci(self.banco.mano, 1) #viene dato una carta al banco
		self.situazione() #stampa situazione attuale
		self.scegli()
		

	def scegli(self):
		scelta = raw_input('Hit or stand? ')
		if scelta == 'h':
			self.hit()
		elif scelta == 's':
			self.stand()
		
	def hit(self):
		while self.giocatore.mano.valore() <= 21:
			self.mazzo.distribuisci(self.giocatore.mano, 1)
			if self.giocatore.mano.valore() >= 21:
				self.perso()
			else:
				self.situazione()
				self.scegli()
		
	def stand(self):
		self.regolabanco()
		if self.giocatore.mano.valore() == 21:
			self.vinto()
		else:
			if self.banco.mano.valore() > 21:
				self.vinto()
			elif self.giocatore.mano.valore() > self.banco.mano.valore():
				self.vinto()
			elif self.giocatore.mano.valore() == self.banco.mano.valore():
				self.pareggio()
			else:
				self.perso()
		
	def regolabanco(self):
		while self.banco.mano.valore() < 17:
			self.mazzo.distribuisci(self.banco.mano, 1)
		
	def vinto(self):
		print('---Hai vinto---')
		self.giocatore.soldi += self.giocatore.scommessa * 1.5
		self.giocatore.scommessa = 0
		self.situazione()
		print('\n\n\n')
		self.gioca()
		
	def perso(self):
		print('----Hai perso----')
		self.giocatore.scommessa = 0
		self.situazione()
		print('\n\n\n')
		self.gioca()
		
	def pareggio(self):
		print('----Hai pareggiato----')
		self.giocatore.soldi += self.giocatore.scommessa
		self.giocatore.scommessa = 0
		self.situazione()
		print('\n\n\n')
		self.gioca()
				
	def situazione(self):
		print('\nHai ' + str(self.giocatore.soldi) + '$ ed hai scommesso ' + str(self.giocatore.scommessa) + '$')
		print('Tue carte:  (somma: ' + str(self.giocatore.mano.valore()) + ')')
		print(self.giocatore.mano)
		print('Carte del banco:  (somma: ' + str(self.banco.mano.valore()) + ')')
		print(self.banco.mano)
		


partita = blackjack()
partita.gioca()
