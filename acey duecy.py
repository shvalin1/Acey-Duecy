import pgzrun
import pygame  # 新規追加
from pgzero.rect import Rect

from playing_cards import *

WIDTH = 800
HEIGHT = 600

# Player クラスは Deck の初期化のために使用
class Player:
    def __init__(self, money):
        self.deck = Deck()
        self.deck.shuffle()
        self.money = money

# 削除: get_card_image の定義

# 追加: カードを図形描画する関数
def draw_card(card, pos):
    filename = f"cards/{Card.card_values[card.value].lower()}_of_{Card.suits[card.suit].lower()}.png"
    img = pygame.image.load(filename)
    # Scale image to fit window (adjust scale factor as needed)
    scaled_img = pygame.transform.scale(img, (150, 218))
    screen.blit(scaled_img, pos)

# グローバル変数
state = "bet"     # "bet", "result", "over"
message = ""
player = Player(200)
card1 = None
card2 = None
card3 = None
bet_buttons = []   # ベット用ボタンのリスト（amount と Rect）
bet_amount = 10
last_change = 0
bet_adjust_buttons = {}  # ボタン情報を格納する辞書

def start_round():
    global card1, card2, state, message, bet_amount, bet_adjust_buttons
    if len(player.deck) < 3 or player.money < 10:
        state = "over"
        message = "Game Over! Press R to restart"
        return
    card1 = player.deck.get_next()
    card2 = player.deck.get_next()
    if card1 > card2:
        card1, card2 = card2, card1
    state = "bet"
    message = ""
    bet_amount = 10  # Minimum bet
    # 1段目：額調整ボタン（4つ）、2段目：Confirmボタン
    upper_y = 450
    gap = 20
    btn_width = 80
    btn_height = 60
    # 上段：4ボタンの全体幅 = 80*4 + 20*3 = 380, 左端 = WIDTH/2 - 190
    left_boundary = WIDTH/2 - 190
    bet_adjust_buttons = {
        "minus10": {"rect": Rect((left_boundary, upper_y), (btn_width, btn_height)), "label": "-10", "color": "dodgerblue"},
        "minus1":  {"rect": Rect((left_boundary + btn_width + gap, upper_y), (btn_width, btn_height)), "label": "-1", "color": "dodgerblue"},
        "plus1":   {"rect": Rect((left_boundary + 2*(btn_width + gap), upper_y), (btn_width, btn_height)), "label": "+1", "color": "dodgerblue"},
        "plus10":  {"rect": Rect((left_boundary + 3*(btn_width + gap), upper_y), (btn_width, btn_height)), "label": "+10", "color": "dodgerblue"},
        # 下段：Confirmボタンを中央に配置（幅160）
        "confirm": {"rect": Rect((WIDTH/2 - 80, upper_y + btn_height + gap), (160, btn_height)), "label": "Confirm", "color": "orange"}
    }

start_round()

def draw():
    # Apply background image
    screen.blit("background.png", (0,0))
    screen.draw.text(f"Money: ${player.money}", topleft=(20, 20), fontsize=30, color="white")
    screen.draw.text(f"Cards left: {len(player.deck)}", topleft=(20, 60), fontsize=30, color="white")
    # Draw cards using shape drawing
    if card1 and card2:
        # カードの幅を考慮して中央配置 (カード幅は150)
        draw_card(card1, (WIDTH/2 - 170, 100))  # 左のカード
        draw_card(card2, (WIDTH/2 + 20, 100))   # 右のカード
    if state == "bet":
        # Adjusted bet display position
        screen.draw.text(f"Bet: ${bet_amount}", midtop=(WIDTH/2, 340), fontsize=50, color="yellow")
        # ベット調整ボタンの描画
        for btn in bet_adjust_buttons.values():
            screen.draw.filled_rect(btn["rect"], btn["color"])
            screen.draw.rect(btn["rect"], "white")
            screen.draw.text(btn["label"], center=btn["rect"].center, fontsize=40, color="white")
    elif state == "result":
        if card3:
            draw_card(card3, (WIDTH/2 - 75, 200))  # 中央のカード
        screen.draw.text(message, midtop=(WIDTH/2, 450), fontsize=40, color="cyan")
        # 勝敗時の金額増減を表示（正の値は緑、負の値は赤）
        if last_change >= 0:
            change_text = f"Change: +${last_change}"
            change_color = "green"
        else:
            change_text = f"Change: -${abs(last_change)}"
            change_color = "red"
        screen.draw.text(change_text, midtop=(WIDTH/2, 510), fontsize=40, color=change_color)
        screen.draw.text("Next round: SPACE", midtop=(WIDTH/2, 570), fontsize=30, color="white")
    elif state == "over":
        screen.draw.text("Game Over!", center=(WIDTH/2, HEIGHT/2), fontsize=60, color="red")
        screen.draw.text("Restart: Press R", center=(WIDTH/2, HEIGHT/2+60), fontsize=40, color="white")

def on_mouse_down(pos):
    global state, message, bet_amount
    if state == "result":
        start_round()
        return
    if state == "bet":
        for key, btn in bet_adjust_buttons.items():
            if btn["rect"].collidepoint(pos):
                if key == "minus10":
                    bet_amount = max(10, bet_amount - 10)
                elif key == "minus1":
                    bet_amount = max(10, bet_amount - 1)
                elif key == "plus1":
                    bet_amount = min(player.money, bet_amount + 1)
                elif key == "plus10":
                    bet_amount = min(player.money, bet_amount + 10)
                elif key == "confirm":
                    if bet_amount > player.money:
                        message = "Insufficient funds!"
                    else:
                        play_round(bet_amount)

def on_key_down(key):
    global state, player
    if state == "result":
        if key == keys.SPACE:
            start_round()
    elif state == "over":
        if key == keys.R:
            player.money = 200
            player.deck.shuffle()
            start_round()

def play_round(bet):
    global state, message, card3, player, last_change
    card3 = player.deck.get_next()
    if card3.between(card1, card2):
        message = "YOU WIN!"
        player.money += bet
        last_change = bet
    else:
        message = "YOU LOSE!"
        player.money -= bet
        last_change = -bet
    state = "result"

pgzrun.go()






