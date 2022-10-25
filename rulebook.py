
from ursina import *

def rulebook():
    window.borderless = False
    window.color = color._30

    # 폰트 설정하는 곳
    Text.default_font = 'NanumGothicCoding.ttf'

    i = 0.28
    Text(text="Aces                 1이 나온 주사위 눈의 총합. 최대 5점", scale=1, position=(-0.735, 0.5 - i))
    Text(text="Deuce                2가 나온 주사위 눈의 총합. 최대 10점", scale=1, position=(-0.735, 0.45 - i))
    Text(text="Threes               3이 나온 주사위 눈의 총합. 최대 15점", scale=1, position=(-0.735, 0.4 - i))
    Text(text="Fours                4가 나온 주사위 눈의 총합. 최대 20점", scale=1, position=(-0.735, 0.35 - i))
    Text(text="Fives                5가 나온 주사위 눈의 총합. 최대 25점", scale=1, position=(-0.735, 0.3 - i))
    Text(text="Sixes                6이 나온 주사위 눈의 총합. 최대 30점", scale=1, position=(-0.735, 0.25 - i))
    Text(text="Bonus                상단 항목의 점수 합계까 63점 이상일 때 35점을 추가로 얻는다.", scale=1, position=(-0.735, 0.2 - i))
    Text(text="Choice               주사위 눈 5개의 총합. 최대 30점", scale=1, position=(-0.735, 0.15 - i))
    Text(text="4 of a kind          동일한 주사위 눈이 4개 이상일 때, 주사위 눈 5개의 종합. 최대 30점", scale=1, position=(-0.735, 0.1 - i))
    Text(text="Full House           동일한 주사위 눈이 각각 3개, 2개일 때, 주사위 눈 5개의 종합. 최대 30점", scale=1, position=(-0.735, 0.05 - i))
    Text(text="Small Straight       이어지는 주사위 눈이 4개 이상일 때. 고정 15점", scale=1, position=(-0.735, 0 - i))
    Text(text="Large Straight       이어지는 주사위 눈이 5개 이상일 때. 고정 30점", scale=1, position=(-0.735, -0.05 - i))
    Text(text="Yacht                동일한 주사위 눈이 5개 일 때 고정 50점", scale=1, position=(-0.735, -0.1 - i))


    # Text(text=, scale=1, position=(-0.735, (0.15 - i / 14)))
    # Text(text=, scale=1, position=(-0.335, (0.15 - i / 14)))

