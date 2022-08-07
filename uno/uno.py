from random import choice
from itertools import product
from copy import deepcopy

class Card:
    def __init__(self,card: tuple):
        self.type = card[0]
        self.color = card[1]

CARD_COLOR = ["red","blue","yellow","green"]
INT_CARD = list(product([str(int_card) for int_card in range(10) if int_card != 0],CARD_COLOR))
SPECIAL_CARD = list(product(["skip","reverse","draw_two"],CARD_COLOR))
ZERO_CARD = [("0",color) for color in CARD_COLOR]
NONE_COLORS = [("draw_four","black"),("wild","black")]
CARD_POOL = ZERO_CARD + INT_CARD*2 + SPECIAL_CARD*2 + NONE_COLORS*4

def draw(amount: int) -> list:
    draw_cards = []
    i = 0
    while i < amount:
        draw_cards.append(Card(choice(CARD_POOL)))
        i += 1
    return draw_cards

class Uno:
    def __init__(self,*players):
        self.MAX_PLAYER = len(players)
        self.PLAYERS = players
        self.direction = 1
        self.pointer = 0
        self.now_player = self.PLAYERS[self.pointer]
        self.top_card = Card(choice(ZERO_CARD+INT_CARD*2+SPECIAL_CARD*2))
        self.penalty_pool = 0
        self.is_penalty = False
    
    def advance_turn(self):
        self.pointer += self.direction
        if self.pointer >= self.MAX_PLAYER:
            self.pointer -= self.MAX_PLAYER
        elif self.pointer < 0:
            self.pointer += self.MAX_PLAYER
        self.now_player = self.PLAYERS[self.pointer]


    def player_action(self,card=None,penalty_return=True,request_color=None) -> bool:
        #前にドローペナルティ系カードが出ていたら
        if self.is_penalty:
            if not penalty_return:
                print(self.penalty_pool)
                self.now_player.hand += draw(self.penalty_pool)
                self.penalty_pool = 0
                self.is_penalty = False
                self.advance_turn()
                return False

        self.top_card = card
        self.now_player.hand.remove(card)
        if len(self.now_player.hand) == 0 and card.color != "black":
            return True
        elif len(self.now_player.hand) == 0 and card.color == "black":
            self.now_player.hand += draw(2)
            return False
        
        #ナンバーカードだった場合
        if card.type in [str(i) for i in range(10)]:
            self.advance_turn()
            return False

        #出されたものがスキップだったら
        if card.type == "skip":
            dir = deepcopy(self.direction)
            self.direction *= 2
            self.advance_turn()
            self.direction = dir
            return False
        #リバースだったら
        elif card.type == "reverse":
            self.direction *= -1
            self.advance_turn()
            return False
        #色替えだったら
        elif card.color == "black":
            self.top_card.color = request_color
            #ドロー4じゃなければ終了
            if card.type != "draw_four":
                self.advance_turn()
                return False

        #ドロー4の色替え後orドロー2の時
        if card.type.startswith("draw"):
            if card.type == "draw_four":
                self.penalty_pool += 4
            elif card.type == "draw_two":
                self.penalty_pool += 2
            self.is_penalty = True
            self.advance_turn()
            return False

class Player:
    def __init__(self,tag=None):
        self.tag = tag
        self.hand = draw(7)
    
    def allow_cards(self,game: Uno) -> list:
        top_card = game.top_card
        if game.is_penalty:
            if top_card.type == "draw_four":
                return [card for card in self.hand if card.type == "draw_four"]
            elif top_card.type == "draw_two":
                return [card for card in self.hand if card.type in ["draw_two","draw_four"]]
        return [card for card in self.hand if card.type == top_card.type or card.color == top_card.color or card.color == "black"]