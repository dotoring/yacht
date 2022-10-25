from ursina import *
import sqlite3
import Player_vs_AI_ver5
import Player_vs_AI_ver3Final
import show_record
import tutorial_play
import rulebook
import winsound
import random

app = Ursina()

Text.default_font = 'NanumGothicCoding.ttf'

title = Text(text='YACHT', scale=6, position=(-0.235, 0.4))
play_button = Button(text='play', color=color.salmon, scale=0.2, position=(-0.6, 0))
tutorial_button = Button(text='tutorial', color=color.salmon, scale=0.2, position=(-0.2, 0))
rule_button = Button(text='rule', color=color.salmon, scale=0.2, position=(0.2, 0))
recode_button = Button(text='record', color=color.salmon, scale=0.2, position=(0.6, 0))

window.borderless = False
window.color = color._30


def main_menu():
    scene.clear()
    winsound.PlaySound('sounds\\click.wav', winsound.SND_ASYNC)
    global title
    global play_button
    global tutorial_button
    global rule_button
    global recode_button

    title = Text(text='YACHT', scale=6, position=(-0.235, 0.4))
    play_button = Button(text='play', color=color.salmon, scale=0.2, position=(-0.6, 0))
    tutorial_button = Button(text='tutorial', color=color.salmon, scale=0.2, position=(-0.2, 0))
    rule_button = Button(text='rule', color=color.salmon, scale=0.2, position=(0.2, 0))
    recode_button = Button(text='record', color=color.salmon, scale=0.2, position=(0.6, 0))

    play_button.on_click = game_play
    tutorial_button.on_click = tutorial
    rule_button.on_click = rule
    recode_button.on_click = recoding

def HighLevelAI():
    scene.clear()
    winsound.PlaySound('sounds\\click.wav', winsound.SND_ASYNC)
    global box_1
    global box_2
    global quit_button

    box_1 = Entity(model=Quad(scale=(8, 1.2), thickness=5, segments=2, mode='line'), color=color.orange, y=-2.5, x=-1.5)
    box_2 = Entity(model=Quad(scale=(8, 1.2), thickness=5, segments=2, mode='line'), color=color.orange, y=2.5, x=-1.5)
    quit_button = Button(text='quit', color=color.orange, x=0.61, y=-0.45, scale=(0.37, 0.08))

    Player_vs_AI_ver5.play()

    quit_button.on_click = main_menu

def LowLevelAI():
    
    scene.clear()
    winsound.PlaySound('sounds\\click.wav', winsound.SND_ASYNC)
    global box_1
    global box_2
    global quit_button

    box_1 = Entity(model=Quad(scale=(8, 1.2), thickness=5, segments=2, mode='line'), color=color.orange, y=-2.5, x=-1.5)
    box_2 = Entity(model=Quad(scale=(8, 1.2), thickness=5, segments=2, mode='line'), color=color.orange, y=2.5, x=-1.5)
    quit_button = Button(text='quit', color=color.orange, x=0.61, y=-0.45, scale=(0.37, 0.08))

    Player_vs_AI_ver3Final.play()

    quit_button.on_click = main_menu    

def game_play():
    scene.clear()
    winsound.PlaySound('sounds\\click.wav', winsound.SND_ASYNC)
    title = Text(text='YACHT', scale=6, position=(-0.235, 0.4))
    HighLevelAI_button = Button(text='HighLevel AI', color=color.salmon, scale=0.2, position=(0.2, 0))
    HighLevelAI_button.on_click = HighLevelAI
    LowLevelAI_button = Button(text='LowLevel AI', color=color.salmon, scale=0.2, position=(-0.2, 0))
    LowLevelAI_button.on_click  = LowLevelAI
    
    quit_button = Button(text='quit', color=color.orange, x=0.61, y=-0.45, scale=(0.37, 0.08))
    quit_button.on_click = main_menu

def tutorial():
    scene.clear()
    winsound.PlaySound('sounds\\click.wav', winsound.SND_ASYNC)
    global box_1
    global box_2
    global quit_button

    box_1 = Entity(model=Quad(scale=(8, 1.2), thickness=5, segments=2, mode='line'), color=color.orange, y=-2.5, x=-1.5)
    box_2 = Entity(model=Quad(scale=(8, 1.2), thickness=5, segments=2, mode='line'), color=color.orange, y=2.5, x=-1.5)
    quit_button = Button(text='quit', color=color.orange, x=0.61, y=-0.45, scale=(0.37, 0.08))

    tutorial_play.play()
    quit_button.on_click = main_menu

def rule():
    scene.clear()
    winsound.PlaySound('sounds\\click.wav', winsound.SND_ASYNC)
    global title
    global quit_button
    global text

    title = Text(text='YACHT', scale=6, position=(-0.235, 0.4))
    quit_button = Button(text='quit', color=color.orange, x=0.61, y=-0.45, scale=(0.37, 0.08))

    rulebook.rulebook()

    quit_button.on_click = main_menu

def recoding():
    scene.clear()
    winsound.PlaySound('sounds\\click.wav', winsound.SND_ASYNC)
    global title
    global quit_button
    global text

    title = Text(text='YACHT', scale=6, position=(-0.235, 0.4))
    quit_button = Button(text='quit', color=color.orange, x=0.61, y=-0.45, scale=(0.37, 0.08))
    show_record.show_record()

    def delete():
        conn = sqlite3.connect('test9.db', isolation_level=None)
        winsound.PlaySound('sounds\\click.wav', winsound.SND_ASYNC)
        c = conn.cursor()
        # 삭제할 때
        c.execute("DELETE FROM score ")
        scene.clear()
        recoding()

    Button(text="삭제", scale=(0.37, 0.08), x= -0.1, y=-0.45, on_click=delete, color=color.orange )
    quit_button.on_click = main_menu


play_button.on_click = game_play
tutorial_button.on_click = tutorial
rule_button.on_click = rule
recode_button.on_click = recoding



app.run()