import random


class Card: 
	# カードの値と文字列表現のマッピング
	card_values = {2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"10",11:"Jack",12:"Queen", 13:"King", 14:"Ace"}
	suits = ("Clubs", "Diamonds", "Hearts", "Spades")
	
	def __init__(self, value, suit):
		""" value (2-14) and suit(0-3) are ints """
		self.value = value
		self.suit = suit
	
	def get_suit_text(self):
		return Card.suits[self.suit]
		
	def __lt__(self, card):
		# カードの大小比較 (小なり)
		if self.value < card.value:
			return True
		if self.value == card.value:
			if self.suit < card.suit:
				return True
		return False
		
	def __gt__(self, card):
		# カードの大小比較 (大なり)
		if self.value > card.value:
			return True
		if self.value == card.value:
			if self.suit > card.suit:
				return True
		return False	
		
	def __eq__(self, card):
		# カードの等価比較
		return self.value == card.value
			
	def between(self, card1, card2):
		# このカードが2枚のカードの間の値かどうかを判定
		return min(card1, card2) < self < max(card1, card2)
		
	def __str__(self):
		return '{0} of {1}'.format(Card.card_values[self.value], Card.suits[self.suit])
		

class Deck:
	def __init__(self):
		random.seed()
		self.construct()

	def construct(self):
		# デッキの初期化：全てのカードを生成
    		self.cards = [Card(value, suit) for suit in range(4) for value in range(2, 15)]
    		self.discards = []
				
	def shuffle(self):
		# デッキをシャッフル
		self.cards.extend(self.discards)
		self.discards = []
		random.shuffle(self.cards)

	def cut(self):
		# デッキをカット
	    if len(self.cards) < 2:
	        return  # カットするのに十分なカードがない
	
	    middle = len(self.cards) // 2
	    range_limit = min(8, middle)  # 範囲制限
	    cut_point = random.randint(middle - range_limit, middle + range_limit)
	
	    self.cards = self.cards[cut_point:] + self.cards[:cut_point]
		
	def order(self):
		# カードを順番に並べ替え
		self.cards.sort()
		
	def choose_random(self, remove = True):
		# ランダムにカードを選択
		if len(self.cards) == 0:
			return None
		card = random.choice(self.cards)
		if remove:
			self.cards.remove(card)
			self.discards.append(card)
		return card
		
		
	def get_next(self, remove=True, place="bottom"):
		# 次のカードを取得
	        if not self.cards:
	            return None
	
	        card = self.cards.pop(0)  # 一番上のカードを取る
	
	        if not remove:
	            if place == "top":
	                self.cards.insert(0, card)  # 上に戻す
	            elif place == "random":
	                self.cards.insert(random.randint(0, len(self.cards)), card)  # ランダムな位置に
	            else:  # デフォルト：下に置く
	                self.cards.append(card)  
	        else:
	            self.discards.append(card)
	
	        return card
		
	def __len__(self):
		return len(self.cards)
		
	def is_empty(self):
		# デッキが空かどうかを確認
		return len(self.cards) == 0
