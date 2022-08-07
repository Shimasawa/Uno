#インポート
import uno
#プレイヤー毎にインスタンスを生成
tarou = uno.Player("tarou")
hanako = uno.Player("hanako")
kouta = uno.Player("kouta")
#ゲームのインスタンスを生成
game = uno.Uno(tarou,hanako,kouta)

#ゲームを行うループ
while(1):
    player: uno.Player
    #このターンのプレイヤー
    player = game.now_player

    print(f"{player.tag}さんの番です")

    print("【場のカード】")
    print(f"{game.top_card.type},{game.top_card.color}")

    print("【手札】")
    for card in player.hand:
        print(f"{card.type},{card.color}")

    count = 0
    #プレイヤーの手札の内出せるカード
    allows = player.allow_cards(game)
    #出せるカードがなかった場合
    if len(allows) == 0:
        #かつ、場のドローペナルティが有効
        if game.is_penalty:
            #現在のペナルティを受けてターン終了
            game.player_action(penalty_return=False)
            print("ドローペナルティを受けました")
            continue
        #ドローペナルティがなければ一枚引いて手札に加え、再度出せるカードを求める
        add_draw = uno.draw(1)
        player.hand += add_draw
        print(f"出せるカードがなかったので一枚引き、{add_draw[0].type},{add_draw[0].color}を追加しました")
        allows = player.allow_cards(game)
        #それでもなかった場合、ターン終了
        if len(allows) == 0:
            print("出せるカードがありません")
            continue
    print("【出せるカード】")
    for card in allows:
        print(f"{count}:{card.type},{card.color}")
        count += 1
    #場に有効なペナルティがあるが、手札に受け流せるカードがある場合
    if game.is_penalty:
        yorn = input("ドローペナルティを受け流しますか(y/n)")
        #敢えて受け流さなかった場合、ペナルティを受けてターン終了
        if yorn == "n":
            game.player_action(penalty_return=False)
            continue
    
    put = input("出すカードの番号を入力")
    #場に出すカードの選択
    select_card = allows[int(put)]
    color = None
    #色変更があるカードの場合、色を選択し引数へ
    if select_card.color == "black":
        color = input("変更したい色(red,green,blue,yellow)を英語で入力:")
        is_end = game.player_action(select_card,request_color=color)
    #それ以外の場合、そのまま行動を確定
    else:
        is_end = game.player_action(card=select_card)
    #is_endにあがりの結果を受け取り、手札がゼロであればゲーム終了
    if is_end:
        print(f"{player.tag}さんの勝ち")
        break
    #そうでなければ、次の手番(ループへ)
    continue