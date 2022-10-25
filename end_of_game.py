import sqlite3
from numpy import true_divide
from ursina import *
import show_record
import winsound

def recording(game_score ,record_button, check_victory):
    # 폰트 설정하는 곳
    winsound.PlaySound('sounds\\click.wav', winsound.SND_ASYNC)
    Text.default_font = 'NanumGothicCoding.ttf'
    destroy(record_button)
    score = game_score
    user_ID = ""
    win = 0
    defeat =0
    db_list = []
    global username_field
    global text1
    global button2

    username_field = InputField(position=(-0.05, -0.03), max_width=1)
    text1 = Text(text="이름을 입력해주세요", x=-0.15, y=0.05, color=color.black)


    # DB 생성(오토 커밋)
    conn = sqlite3.connect('test9.db', isolation_level=None)

    # 커서 획득
    c = conn.cursor()

    # 테이블 생성 ()
    c.execute("CREATE TABLE IF NOT EXISTS score (score integer, user_ID text, win integer, defeat integer)")

    # 입력한 id들의 리스트
    li = []

    # 테이블에 있는 내용을 tuple 형태로 가져온다.
    c.execute("SELECT * FROM score")
    player = c.fetchall()

    # 플레그
    k = True

    def submit():
        global k
        global button2
        global db_list
        user_ID = username_field.text

        winsound.PlaySound('sounds\\click.wav', winsound.SND_ASYNC)
        # DB의 모든 열들(user_id)의 집합을 li에 모음
        for u_score in player:
            li.append(u_score[1])

        # 입력한 user_ID가 있는지 확인 후 객체를 읽어서 None 형태로 entry에 넣는다.
        c.execute("SELECT * FROM score WHERE user_ID = ?", (user_ID,))
        entry = c.fetchone()

        if(entry):
            db_list = list(entry)
        else:
            db_list=[0,"",0,0]

        # DB에 값 넣기, 중복된것은 들어가지 않는다.
        if entry is None:
            # 중복 안됬을 때 DB에 들어감
            c.execute("INSERT INTO score VALUES(?, ?, ?, ?)", (score, user_ID, 0, 0))


        #Plyaer가 이겼을 때
        if(check_victory is True):
            db_list[2] += 1
            c.execute("UPDATE score SET score=?, win=? , defeat=? WHERE user_ID=?",(score, db_list[2], db_list[3],  user_ID))
            
        else:
            db_list[3] += 1
            c.execute("UPDATE score SET score=?, win=? , defeat=? WHERE user_ID=?",(score, db_list[2], db_list[3],  user_ID))
            

        

        Save_Text = Text(text= '저장 완료', position=(-0.13, -0.15), color=color.black)
        button2.disabled = True

    button2 = Button(text="확인", scale=(0.1, 0.05), position=(0.26, -0.03), on_click=submit)

