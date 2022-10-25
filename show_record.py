import sqlite3
from ursina import *

def show_record():
    win = 0
    defeat = 0
    window.borderless = False
    window.color = color._30

    # 폰트 설정하는 곳
    Text.default_font = 'NanumGothicCoding.ttf'

    print_score = Text(text="score", scale=2, position=(-0.735, 0.25))
    print_user_ID = Text(text="user_ID", scale=2, position=(-0.335, 0.25))
    print_win = Text(text="win", scale=2, position=(0.065, 0.25))
    print_defeat = Text(text="defeat", scale=2, position=(0.465, 0.25))

    # DB 생성(오토 커밋)
    conn = sqlite3.connect('test9.db', isolation_level=None)

    # 커서 획득
    c = conn.cursor()

    # 테이블에 있는 내용을 tuple 형태로 가져온다.
    c.execute("SELECT * FROM score ORDER BY score DESC")

    player = c.fetchall()

    def show_detail(win, defeat):
        global text1
        global text2
        global text3
        global text4
        x = 0
        for i in range(len(player)):
            if x < 7 :
                win += player[i][2]
                defeat += player[i][3]

                text1 = Text(text=str(player[i][0]), scale=2, position=(-0.735, (0.15 - i / 14)))
                text2 = Text(text=str(player[i][1]), scale=2, position=(-0.335, (0.15 - i / 14)))
                text3 = Text(text=str(player[i][2]), scale=2, position=(0.065, (0.15 - i / 14)))
                text4 = Text(text=str(player[i][3]), scale=2, position=(0.465, (0.15 - i / 14)))
                x = x +1


        if win + defeat == 0:
            Text(text="평균 승률 = 0", scale=2, position=(-0.745, (0.35)))
        else:
            Text(text="평균 승률 = " + str(round((win / (win + defeat)) * 100, 2)), scale=2, position=(-0.745, (0.35)))

    show_detail(win, defeat)

