import pgzrun
import pygame
from pgzero.rect import Rect

from playing_cards import *

WIDTH = 800
HEIGHT = 600

class Player:
    def __init__(self, money):
        self.deck = Deck()
        self.deck.shuffle()
        self.money = money

# ゲーム状態を管理するクラス
class Game:
    def __init__(self):
        self.player = Player(200)
        self.state = "bet"  # "bet", "result", "over"
        self.message = ""
        self.bet_amount = 10
        self.last_change = 0
        self.card1 = self.card2 = self.card3 = None
        self.bet_adjust_buttons = {}
        self.start_round()

    def start_round(self):
        if len(self.player.deck) < 3 or self.player.money < 10:
            self.state = "over"
            self.message = "Game Over! Press R to restart"
            return
        self.card1 = self.player.deck.get_next()
        self.card2 = self.player.deck.get_next()
        if self.card1 > self.card2:
            self.card1, self.card2 = self.card2, self.card1
        self.state = "bet"
        self.message = ""
        self.bet_amount = 10  # 最低ベット
        upper_y = 450
        gap = 20
        btn_width = 80
        btn_height = 60
        left_boundary = WIDTH/2 - 190
        self.bet_adjust_buttons = {
            "minus10": {"rect": Rect((left_boundary, upper_y), (btn_width, btn_height)), "label": "-10", "color": "dodgerblue"},
            "minus1":  {"rect": Rect((left_boundary + btn_width + gap, upper_y), (btn_width, btn_height)), "label": "-1", "color": "dodgerblue"},
            "plus1":   {"rect": Rect((left_boundary + 2*(btn_width + gap), upper_y), (btn_width, btn_height)), "label": "+1", "color": "dodgerblue"},
            "plus10":  {"rect": Rect((left_boundary + 3*(btn_width + gap), upper_y), (btn_width, btn_height)), "label": "+10", "color": "dodgerblue"},
            "confirm": {"rect": Rect((WIDTH/2 - 80, upper_y + btn_height + gap), (160, btn_height)), "label": "Confirm", "color": "orange"}
        }

    def draw(self):
        screen.blit("background.png", (0,0))
        screen.draw.text(f"Money: ${self.player.money}", topleft=(20, 20), fontsize=30, color="white")
        screen.draw.text(f"Cards left: {len(self.player.deck)}", topleft=(20, 60), fontsize=30, color="white")
        if self.card1 and self.card2:
            draw_card(self.card1, (WIDTH/2 - 170, 100))
            draw_card(self.card2, (WIDTH/2 + 20, 100))
        if self.state == "bet":
            screen.draw.text(f"Bet: ${self.bet_amount}", midtop=(WIDTH/2, 340), fontsize=50, color="yellow")
            for btn in self.bet_adjust_buttons.values():
                screen.draw.filled_rect(btn["rect"], btn["color"])
                screen.draw.rect(btn["rect"], "white")
                screen.draw.text(btn["label"], center=btn["rect"].center, fontsize=40, color="white")
        elif self.state == "result":
            if self.card3:
                draw_card(self.card3, (WIDTH/2 - 75, 200))
            screen.draw.text(self.message, midtop=(WIDTH/2, 450), fontsize=40, color="cyan")
            if self.last_change >= 0:
                change_text = f"Change: +${self.last_change}"
                change_color = "green"
            else:
                change_text = f"Change: -${abs(self.last_change)}"
                change_color = "red"
            screen.draw.text(change_text, midtop=(WIDTH/2, 510), fontsize=40, color=change_color)
            screen.draw.text("Next round: SPACE", midtop=(WIDTH/2, 570), fontsize=30, color="white")
        elif self.state == "over":
            screen.draw.text("Game Over!", center=(WIDTH/2, HEIGHT/2), fontsize=60, color="red")
            screen.draw.text("Restart: Press R", center=(WIDTH/2, HEIGHT/2+60), fontsize=40, color="white")

    def on_mouse_down(self, pos):
        if self.state == "result":
            self.start_round()
            return
        if self.state == "bet":
            for key, btn in self.bet_adjust_buttons.items():
                if btn["rect"].collidepoint(pos):
                    if key == "minus10":
                        self.bet_amount = max(10, self.bet_amount - 10)
                    elif key == "minus1":
                        self.bet_amount = max(10, self.bet_amount - 1)
                    elif key == "plus1":
                        self.bet_amount = min(self.player.money, self.bet_amount + 1)
                    elif key == "plus10":
                        self.bet_amount = min(self.player.money, self.bet_amount + 10)
                    elif key == "confirm":
                        if self.bet_amount > self.player.money:
                            self.message = "Insufficient funds!"
                        else:
                            self.play_round(self.bet_amount)

    def on_key_down(self, key):
        if self.state == "result":
            if key == keys.SPACE:
                self.start_round()
        elif self.state == "over":
            if key == keys.R:
                self.player.money = 200
                self.player.deck.shuffle()
                self.start_round()

    def play_round(self, bet):
        self.card3 = self.player.deck.get_next()
        if self.card3.between(self.card1, self.card2):
            self.message = "YOU WIN!"
            self.player.money += bet
            self.last_change = bet
        else:
            self.message = "YOU LOSE!"
            self.player.money -= bet
            self.last_change = -bet
        self.state = "result"

# 関数: カード画像を描画する
def draw_card(card, pos):
    filename = f"cards/{Card.card_values[card.value].lower()}_of_{Card.suits[card.suit].lower()}.png"
    img = pygame.image.load(filename)
    scaled_img = pygame.transform.scale(img, (150, 218))
    screen.blit(scaled_img, pos)

game = Game()

def draw():
    game.draw()

def on_mouse_down(pos):
    game.on_mouse_down(pos)

def on_key_down(key):
    game.on_key_down(key)

pgzrun.go()





