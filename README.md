# Acey Ducey

## 概要
Acey Ducey は Python と pgzero を使用したカードゲームです。プレイヤーはベットを行い、２枚のカードの間に隠れたカードが入るかどうかを予想します。

## 必要な環境
- Python 3.x
- pgzero
- pygame

## インストール
1. Python をインストールしてください。
2. 必要パッケージをインストールします:
    ```
    pip install pgzero pygame
    ```
3. プロジェクトディレクトリに移動します。

## ゲームの実行
1. ターミナルで以下のコマンドを実行:
    ```
    pgzrun acey duecy.py
    ```

## 操作方法
- マウスクリックでベット調整ボタンを操作します。
- `SPACE` キーで次のラウンドに進みます。
- ゲームオーバー時は `R` キーで再スタートできます。

## ディレクトリ構成
- `/home/shvalin/github/Acey-Duecy/playing_cards.py` : カードおよびデッキの実装
- `/home/shvalin/github/Acey-Duecy/acey duecy.py` : ゲームのメインロジックおよび画面描画

## 画像リソース
- カード画像は `cards/` ディレクトリに配置してください。
- 背景画像は `background.png` を用意してください。

