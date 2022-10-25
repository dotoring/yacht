from ursina import *
import random
import numpy as np
import end_of_game
import winsound


def play():

    Text.default_font = 'NanumGothicCoding.ttf'
    print_text = Text(text="", x=-0.7, y=0.2 )
    player_text = Text(text="Player", x=-0.65, y=-0.29, color=color.black)
    print_text.text = "플레이어의 차례입니다. 주사위를 굴려주세요" 
    player_text.create_background(radius=0, padding=0.01, color=color.white)
    AI_text = Text(text="HighLevel AI", x=-0.65, y=0.32, color=color.black)
    AI_text.create_background(radius=0, padding=0.01, color=color.white)
    Score_board = Entity(model='quad', texture='Score_borad_v2.png', scale=(3, 7), x=5.0, y=0.3)


    class Dice():

        Dice_Count = 0


        def __init__(self, x):
            self.side = None
            self.x = x-0.5
            self.y = 0
            self.Dice_Entity = Entity(color=color.white)
            # 다이스 삭제여부 검사


        # 다이스 굴리기
        def roll(self, distance, height):

            if self.Dice_Count < 4 and self.Dice_Entity.color == color.white:
                self.side = random.randint(1, 6)
                # 다이스 삭제
                destroy(self.Dice_Entity)
                # 다이스 생성
                if self.side == 1:
                    self.Dice_Entity = Entity(model='quad', texture='Dice\\Dice1.png', scale=(1, 1), x=self.x, y=self.y,
                                            collider='box', on_click=Func(self.check, distance, height))

                if self.side == 2:
                    self.Dice_Entity = Entity(model='quad', texture='Dice\\Dice2.png', scale=(1, 1), x=self.x, y=self.y,
                                            collider='box', on_click=Func(self.check, distance, height))

                if self.side == 3:
                    self.Dice_Entity = Entity(model='quad', texture='Dice\\Dice3.png', scale=(1, 1), x=self.x, y=self.y,
                                            collider='box', on_click=Func(self.check, distance, height))

                if self.side == 4:
                    self.Dice_Entity = Entity(model='quad', texture='Dice\\Dice4.png', scale=(1, 1), x=self.x, y=self.y,
                                            collider='box', on_click=Func(self.check, distance, height))

                if self.side == 5:
                    self.Dice_Entity = Entity(model='quad', texture='Dice\\Dice5.png', scale=(1, 1), x=self.x, y=self.y,
                                            collider='box', on_click=Func(self.check, distance, height))

                if self.side == 6:
                    self.Dice_Entity = Entity(model='quad', texture='Dice\\Dice6.png', scale=(1, 1), x=self.x, y=self.y,
                                            collider='box', on_click=Func(self.check, distance, height))

        def check(self, distance, height):
    

            if self.Dice_Entity.color == color.white50:
                self.Dice_Entity.color = color.white
                self.move( distance, -height)
            else:
                self.Dice_Entity.color = color.white50
                self.move( distance, height)



        def move(self, distance, height):

            self.Dice_Entity.y += height
            distance += 1
            if distance < 25:
                invoke(Func(self.move, distance, height), delay=0.0001)



    class Strategy():
        def __init__(self, strategies):
            self.strategies = strategies

        def set_dices(self, dices):
            self.dices = dices

        def set_Strategy(self, x): 
            for i, strategy_name in enumerate(strategies_order):
                if not (i >= 9 and i < 14):
                    self.strategies[strategy_name] = {

                        'position': [0.6572 + x, 0.285 - 0.042 * i],
                        'score': 0,
                        'selected': False,
                        'done': False
                    }
                else:
                    self.strategies[strategy_name] = {

                        'position': [0.655 + x, -0.084 - 0.042 * (i - 8)],
                        'score': 0,
                        'selected': False,
                        'done': False
                    }

            self.strategies['Bonus']['position'][1] = -0.003
            self.strategies['Choice']['position'][1] = -0.073
            self.strategies['Total']['position'][1] = -0.356
                

        def calculate(self):
            self.sides = [dice.side for dice in self.dices]
            self.unique = set(self.sides)

            for i in range(1, 7):
                if self.strategies['%ds' % i]['done']:
                    continue

                score = self.sum_of_single(i)
                self.strategies['%ds' % i]['score'] = score         
                    
            if not self.strategies['Choice']['done']:
                self.strategies['Choice']['score'] = sum(self.sides)
            if not self.strategies['4-of-a-kind']['done']:
                self.strategies['4-of-a-kind']['score'] = self.of_a_kind(4)
            if not self.strategies['Full House']['done']:
                self.strategies['Full House']['score'] = self.full_house()
            if not self.strategies['S. Straight']['done']:
                self.strategies['S. Straight']['score'] = self.small_straight()
            if not self.strategies['L. Straight']['done']:
                self.strategies['L. Straight']['score'] = self.large_straight()
            if not self.strategies['Yacht']['done']:
                self.strategies['Yacht']['score'] = self.of_a_kind(5)

            return self.strategies

        def sum_of_single(self, number):
            return sum([x for x in self.sides if x == number])

        def count(self, number):
            return len([side for side in self.sides if side == number])

        # n번이상 반복되는 주사위 눈 뽑기
        def highest_repeated(self, min_repeats):
            repeats = [x for x in self.unique if self.count(x) >= min_repeats]
            return max(repeats) if repeats else 0

        def equal_repeated(self, equal_repeated):
            repeats = [x for x in self.unique if self.count(x) == equal_repeated]
            return repeats if repeats else 0

        def of_a_kind(self, n):
            hr = self.highest_repeated(n)

            if hr == 0:
                return 0

            if n == 5:
                return 50

            rests = [side for side in self.sides if side != hr]

            return hr * n + sum(rests)

        def full_house(self):
            hr = self.highest_repeated(3)
            if hr > 0:
                rests = [side for side in self.sides if side != hr]
                if len(set(rests)) == 1 and len(rests) == 2:
                    return sum(self.sides)
            return 0

        def small_straight(self):
            if set([1, 2, 3, 4]).issubset(self.unique) or set([2, 3, 4, 5]).issubset(self.unique) or set(
                    [3, 4, 5, 6]).issubset(self.unique):
                return 15
            return 0

        def large_straight(self):
            if set([1, 2, 3, 4, 5]).issubset(self.unique) or set([2, 3, 4, 5, 6]).issubset(self.unique):
                return 30
            return 0

        def Part_caculate(self):
            subscore = 0
            for i in range(1, 7):
                if self.strategies['%ds' % i]['done']:
                    subscore = self.strategies['%ds' % i]['score'] + subscore
            self.strategies['subtotal']['score'] = subscore

            self.strategies['Total']['score'] = 0
            if subscore >= 63 and not self.strategies['Bonus']['done']:
                self.strategies['Bonus']['done'] = True
                self.strategies['Bonus']['score'] += 35
            for k, v in self.strategies.items():
                if v['done']:
                    self.strategies['Total']['score'] += v['score']
            

        
        def equal_repeated(self, equal_repeated):
            repeats = [x for x in self.unique if self.count(x) == equal_repeated]
            return repeats if repeats else 0

        def sum_of_single(self, number):
            return sum([x for x in self.sides if x == number])

        def count(self, number):
            return len([side for side in self.sides if side == number])

        # n번이상 반복되는 주사위 눈 뽑기
        def highest_repeated(self, min_repeats):
            repeats = [x for x in self.unique if self.count(x) >= min_repeats]
            return max(repeats) if repeats else 0

        def of_a_kind(self, n):
            hr = self.highest_repeated(n)

            if hr == 0:
                return 0

            if n == 5:
                return 50

            rests = [side for side in self.sides if side != hr]

            return hr * n + sum(rests)

        def full_house(self):
            hr = self.highest_repeated(3)
            if hr > 0:
                rests = [side for side in self.sides if side != hr]
                if len(set(rests)) == 1 and len(rests) == 2:
                    return sum(self.sides)
            return 0

        def small_straight(self):
            if set([1, 2, 3, 4]).issubset(self.unique) or set([2, 3, 4, 5]).issubset(self.unique) or set(
                    [3, 4, 5, 6]).issubset(self.unique):
                return 15
            return 0

        def large_straight(self):
            if set([1, 2, 3, 4, 5]).issubset(self.unique) or set([2, 3, 4, 5, 6]).issubset(self.unique):
                return 30
            return 0

        def Part_caculate(self):
            subscore = 0
            for i in range(1, 7):
                if self.strategies['%ds' % i]['done']:
                    subscore = self.strategies['%ds' % i]['score'] + subscore
            self.strategies['subtotal']['score'] = subscore

            self.strategies['Total']['score'] = 0
            if subscore >= 63 and not self.strategies['Bonus']['done']:
                self.strategies['Bonus']['done'] = True
                self.strategies['Bonus']['score'] += 35
            for k, v in self.strategies.items():
                if v['done']:
                    self.strategies['Total']['score'] += v['score']
        def reset(self):
            for name in strategies_order:
                self.strategies[name]['done'] = False
                self.strategies[name]['score'] = 0

    class GameManager():

        def __init__(self, Strategy):
            self.n_rounds = 0
            self.Score_Button_array = []
            self.Strategy = Strategy

        def Make_Score_Button(self):
            for strategy_name in strategies_order:

                if strategy_name != 'subtotal' and strategy_name != 'Bonus' and strategy_name != 'Total':
                    Score_Button = Button(text=str(self.Strategy.strategies[strategy_name]['score']),
                                        color=Color(0, 0, 0, 0), position=(
                            self.Strategy.strategies[strategy_name]['position'][0],
                            self.Strategy.strategies[strategy_name]['position'][1])
                                        , text_color=color.black33, scale=(0.05, 0.05), enabled=False, name=strategy_name)

                else:
                    Score_Button = Button(text=str(self.Strategy.strategies[strategy_name]['score']),
                                        color=Color(0, 0, 0, 0), position=(
                            self.Strategy.strategies[strategy_name]['position'][0],
                            self.Strategy.strategies[strategy_name]['position'][1])
                                        , text_color=color.black, scale=(0.05, 0.05), enabled=False, name=strategy_name)

                if strategy_name != 'subtotal' and strategy_name != 'Bonus' and strategy_name != 'Total':
                    Score_Button.on_click = self.Score_Click
                self.Score_Button_array.append(Score_Button)

            
            
        def print_Score_board(self):
            for Score_Button in self.Score_Button_array:
                Score_Button.enabled = True
            for i, strategy_name in enumerate(strategies_order):
                self.Score_Button_array[i].text = str(self.Strategy.strategies[strategy_name]['score'])

        def part_print_Score_board(self):
            self.Score_Button_array[6].text = str(self.Strategy.strategies['subtotal']['score'])
            self.Score_Button_array[7].text = str(self.Strategy.strategies['Bonus']['score'])
            self.Score_Button_array[14].text = str(self.Strategy.strategies['Total']['score'])
                
    class Player(GameManager):

    

        def Score_Click(self):
            winsound.PlaySound('sounds\\click2.wav', winsound.SND_ASYNC)
            print_text.text =""
            e = mouse.hovered_entity
      

            if not (self.Strategy.strategies[e.name]['done']):
                e.text_color = color.black
                #strategy.score_update()
                self.n_rounds += 1
                self.Strategy.strategies[e.name]['done'] = True
                Dice.Dice_Count = 0

                for i, strategy_name in enumerate(strategies_order):
                    if self.Strategy.strategies[strategy_name][
                        'done'] == False and strategy_name != 'subtotal' and strategy_name != 'Bonus' and strategy_name != 'Total':
                        self.Score_Button_array[i].enabled = False

                for dice in self.Strategy.dices:
                    dice.Dice_Entity.color = color.white
                    destroy(dice.Dice_Entity)

                self.Strategy.Part_caculate()
                self.part_print_Score_board()
 
                if button_roll.disabled == False: 
                    button_roll.disabled = True
                    button_roll.color = color.gray
                    button_roll.text = "Wait"
                
                invoke(Func(AI_player.AI_roll_controll),delay = 1)

        def roll_controll(self):
            #라운드가 12이하라면
            if self.n_rounds < 12:
                winsound.PlaySound('sounds\\dice_roll.wav', winsound.SND_ASYNC)
                #Dice 객체의 count가 1증가
                Dice.Dice_Count += 1
                
                for dice in self.Strategy.dices:
                    dice.roll(0,-0.1)

                self.Strategy.calculate()
                self.print_Score_board()
                
                if Dice.Dice_Count < 4:
                    print_text.text  = "스코어 보드판에 점수를 입력하세요. 주사위를 " + str(Dice.Dice_Count) +"번 굴렸습니다."                 
                print( self.Strategy.sides)

                            
    class AI_Player(GameManager):

        def Make_Score_Button(self):
            for strategy_name in strategies_order:
                if strategy_name != 'subtotal' and strategy_name != 'Bonus' and strategy_name != 'Total':
                    Score_Button = Button(text=str(self.Strategy.strategies[strategy_name]['score']),
                                        color=Color(0, 0, 0, 0), position=(
                            self.Strategy.strategies[strategy_name]['position'][0],
                            self.Strategy.strategies[strategy_name]['position'][1])
                                        , text_color=color.black33, scale=(0.05, 0.05), enabled=False, name=strategy_name)

                else:
                    Score_Button = Button(text=str(self.Strategy.strategies[strategy_name]['score']),
                                        color=Color(0, 0, 0, 0), position=(
                            self.Strategy.strategies[strategy_name]['position'][0],
                            self.Strategy.strategies[strategy_name]['position'][1])
                                        , text_color=color.black, scale=(0.05, 0.05), enabled=False, name=strategy_name)
                self.Score_Button_array.append(Score_Button)

        '''def Done_repeated_3_more(self):
            for i in range(1, 7):
                if not self.Strategy.strategies['%ds' % i]['done'] and self.Strategy.strategies['%ds' % i]['score'] > i*2:
                    return i
            return 0'''

        def Score_Choice(self):

            
            if self.Strategy.large_straight() and (not self.Strategy.strategies['L. Straight']['done'] or not self.Strategy.strategies['S. Straight']['done']):
                #print("라지 스트레이트")
                if not self.Strategy.strategies['L. Straight']['done']:
                    self.Score_set('L. Straight')
                elif not self.Strategy.strategies['S. Straight']['done']:
                    self.Score_set('S. Straight')

            #스몰 스트레이트
            elif self.Strategy.small_straight() and (not self.Strategy.strategies['L. Straight']['done'] or not self.Strategy.strategies['S. Straight']['done']):
                #print("스몰 스트레이트")
                if not self.Strategy.strategies['L. Straight']['done'] and Dice.Dice_Count < 3:
                    self.selectDice(self.straight_union(), 'Straight')
                elif not self.Strategy.strategies['S. Straight']['done']:
                    self.Score_set('S. Straight')


            #3연속 + 2연속
            elif self.straight_count() == 3 and self.straight_union_count() == 2 :
                #print("3연속 + 2 연속")
                if self.Strategy.strategies['L. Straight']['done'] and self.Strategy.strategies['S. Straight']['done'] and Dice.Dice_Count < 3:
                    self.selectDice()
                elif 4 in self.Strategy.unique and Dice.Dice_Count < 3:
                        self.selectDice({1,2,4,5}, 'Straight')
                elif not 4 in self.Strategy.unique and Dice.Dice_Count < 3:
                        self.selectDice({1,2,3,5}, 'Straight')

            elif self.Strategy.equal_repeated(2):      
                #print("2중복")
                #각각의 중복이 선택되어지고 choice가 없다면?
                repeatArray = self.Strategy.equal_repeated(2)
                if len(self.Strategy.equal_repeated(2))==2 and not self.Strategy.strategies['Full House']['done'] and Dice.Dice_Count < 3:            
                    #repeatArray[0] * 2 + repeatArray[1]*3 >= 25
                    if  ( self.Strategy.strategies['%ds' %repeatArray[0]]['done']  and self.Strategy.strategies['%ds' %repeatArray[1]]['done']) and repeatArray[0] * 2 + repeatArray[1]*2 >= 16 :
                        self.selectDice( repeatArray, 'Stack')
                        
                    else:
                        self.selectDice( [self.calculate_dice()], 'Stack')
                
                elif self.Strategy.full_house() >= 15 and not self.Strategy.strategies['Full House']['done']:
                    self.Score_set('Full House')

                elif Dice.Dice_Count <3:
                    self.selectDice( [self.calculate_dice()], 'Stack')

            #중복 4
            elif self.Strategy.equal_repeated(4):
                #print(" 4중복 ")
                repeatArray = self.Strategy.equal_repeated(4)
                if (not self.Strategy.strategies['Yacht']['done'] or not self.Strategy.strategies['%ds' % repeatArray[0] ]['done']) and Dice.Dice_Count < 3:
                    self.selectDice(repeatArray,'Stack')
                elif self.Strategy.equal_repeated(1)[0] <= 3 and Dice.Dice_Count < 3:
                    self.selectDice([self.Strategy.equal_repeated(1)[0]], 'Stack')
                elif not self.Strategy.strategies['%ds' % repeatArray[0] ]['done'] and self.restDiceAverage() + self.Strategy.strategies['subtotal']['score'] >= 55 :
                    self.Score_set('%ds' % repeatArray[0])
                elif not self.Strategy.strategies['4-of-a-kind']['done'] :
                    self.Score_set('4-of-a-kind')
                #4of a kind가 선택되었을 때 주사위 눈의 조합 선택
                elif not self.Strategy.strategies['%ds' % repeatArray[0] ]['done'] :
                    self.Score_set('%ds' % repeatArray[0])
                elif Dice.Dice_Count < 3:
                    self.selectDice([self.calculate_dice()])
                

            #중복 5
            elif self.Strategy.equal_repeated(5):
                #print(" 5중복 ")
                repeatArray = self.Strategy.equal_repeated(5)
                if self.Strategy.strategies['Yacht']['done'] and not self.Strategy.strategies['%ds' % repeatArray[0] ]['done']:
                    self.Score_set('%ds' % repeatArray[0])
                elif not self.Strategy.strategies['Yacht']['done']:
                    self.Score_set('Yacht')        


            elif Dice.Dice_Count < 3:
                #print("계산")

                self.selectDice([self.calculate_dice()],'Stack')
            
            if Dice.Dice_Count == 3:

                if self.Strategy.strategies['Choice']['score'] >= 24 and self.Strategy.strategies['Choice']['done'] == False :
                    #Choice의 스코어가 20이 넘을 때 Choice 선택
                    self.Score_set('Choice')

                elif self.Strategy.strategies['Choice']['score'] >= 21 and self.Strategy.strategies['Choice']['done'] == False and self.n_rounds >= 4 :
                    #Choice의 스코어가 20이 넘을 때 Choice 선택
                    self.Score_set('Choice')

                elif self.Strategy.strategies['Choice']['score'] >= 18 and self.Strategy.strategies['Choice']['done'] == False and self.n_rounds >= 8 :
                    #Choice의 스코어가 20이 넘을 때 Choice 선택
                    self.Score_set('Choice')

                elif self.Strategy.strategies['Choice']['score'] >= 15 and self.Strategy.strategies['Choice']['done'] == False and self.n_rounds >= 10 :
                    #Choice의 스코어가 20이 넘을 때 Choice 선택
                    self.Score_set('Choice')                
                    #0인 경우 생각......
                else:
                    
                    if len( [i for i in range(1,7) if not self.Strategy.strategies['%ds' % i]['done'] and self.Strategy.count(i) > 0] ):
                    #가장 개수가 많은 주사위 선택
                        Max_dice_number = self.Max_dice_number('less')


                        if (Max_dice_number == 1) and (self.Strategy.count(Max_dice_number)) >=0:
                            self.Score_set(str(Max_dice_number) + 's')

                        elif Max_dice_number == 2 and self.Strategy.count(Max_dice_number) >=1:
                            self.Score_set(str(Max_dice_number) + 's')

                        elif Max_dice_number == 3 and self.Strategy.count(Max_dice_number) >=1:
                            self.Score_set(str(Max_dice_number) + 's')

                        elif Max_dice_number == 4 and self.Strategy.count(Max_dice_number) >=1:
                            self.Score_set(str(Max_dice_number) + 's')

                        elif Max_dice_number == 5 and self.Strategy.count(Max_dice_number) >=2:
                            self.Score_set(str(Max_dice_number) + 's')

                        elif Max_dice_number == 6 and self.Strategy.count(Max_dice_number) >=2:
                            self.Score_set(str(Max_dice_number) + 's')

                        else:
                            
                            if self.restDiceAverage() + self.Strategy.strategies['subtotal']['score'] >= 63:
                                Under_order = [ '1s','Yacht', 'Full House', '4-of-a-kind','L. Straight', 'S. Straight' , 
                                'Choice', '1s', '2s', '3s', '4s', '5s', '6s' ]
                            else:
                                Under_order = [ '1s', '2s', '3s', 'Yacht', 'Full House' , '4-of-a-kind','L. Straight', 'S. Straight' , 
                                'Choice',  '4s', '5s', '6s' ]
                    
                            for i in Under_order:
                            
                                if not self.Strategy.strategies[i]['done']:
                                    self.Score_set(i)
                                    break     
                    else:
                    #초이스부터 가장 아래까지 선택            
                            if self.restDiceAverage() + self.Strategy.strategies['subtotal']['score'] >= 63:
                                Under_order = [ '1s','Yacht', 'Full House', '1s' '4-of-a-kind','L. Straight', 'S. Straight' , 
                                'Choice', '2s', '3s', '4s', '5s', '6s' ]
                            else:
                                Under_order = [ '1s', '2s', '3s',  'Yacht','Full House' , '4-of-a-kind','L. Straight', 'S. Straight' , 
                                'Choice',  '4s', '5s', '6s' ]

                            for i in Under_order:
                            
                                if not self.Strategy.strategies[i]['done']:
                                    self.Score_set(i)
                                    break    

        def Score_set(self, score_name):

            Dice.Dice_Count = 0
            print_text.text  = "조합 "+ score_name +"를 고릅니다."
            invoke(Func( self.Score_record , score_name), delay = 2)

        def Score_record(self, score_name):

            winsound.PlaySound('sounds\\click2.wav', winsound.SND_ASYNC)    
            self.n_rounds +=1
            self.Strategy.strategies[score_name]['done'] = True
            
            for i, strategy_name in enumerate(strategies_order):
                    if self.Strategy.strategies[strategy_name][
                        'done'] == False and strategy_name != 'subtotal' and strategy_name != 'Bonus' and strategy_name != 'Total':
                        self.Score_Button_array[i].enabled = False
                    if strategy_name == score_name:
                        self.Score_Button_array[i].text_color = color.black

            for dice in  self.Strategy.dices:
                    dice.Dice_Entity.color = color.white
                    destroy(dice.Dice_Entity)
            self.Strategy.Part_caculate()
            self.part_print_Score_board()


            #Dice.Dice_Count = 0 ,delay때문에 Score_set에서 실행
            if button_roll.disabled == True:
                    button_roll.disabled = False
                    button_roll.color = color.orange
                    button_roll.text = "Roll"

            print_text.text  = "플레이어의 차례입니다. 주사위를 굴려주세요"
            Game_result(self.n_rounds)           





        def done_falseUp_union(self):
            
            for order in  ['1s', '2s', '3s', '4s', '5s', '6s']:
                if self.Strategy.strategies[order]['done'] == False: #사용되지 않은 경우
                    return False
            return True

        def Max_dice_number(self, option, number = 6):
            
            Count_array = []
            element_array = []
            Max_index = []
            for i in range(1, number + 1):
                if not self.Strategy.strategies['%ds' % i]['done']:        
                    Count_array.append(([self.Strategy.count(i)]))
                    element_array.append(i)
            if Count_array == []:
                return []
            max_count = max(Count_array)
            for idx, val in enumerate(Count_array):
                if val == max_count:
                        Max_index.append(idx)
            #element_array[max(Max_index)] 이것은 같은 주사위 개수중 더 큰 주사위 눈을 고르는 코드
            if option == 'less':
                return element_array[Max_index[0]]
            elif option == 'more':
                return element_array[max(Max_index)]

        def straight_count(self):
            Ulist = list(self.Strategy.unique)
            count = 0
            for i in range(0, len(Ulist)-1):
                if (Ulist[i + 1] - Ulist[i]) == 1: #[1,2,4,5,6]
                    count = count + 1       
            return count

        def straight_union(self):
            oneUnion = []
            Ulist = list(self.Strategy.unique)
            for i in range(0, len(Ulist)-1):
                if Ulist[i + 1] - Ulist[i] == 1:
                    oneUnion.append(Ulist[i])  
                    oneUnion.append(Ulist[i+1])

            return oneUnion

        def straight_union_count(self):
            oneUnion = []
            union_count = 0
            Ulist = list(self.Strategy.unique)
            for i in range(0, len(Ulist)-1):
                if Ulist[i + 1] - Ulist[i] == 1:
                    oneUnion.append(Ulist[i])  
                    oneUnion.append(Ulist[i+1])
            oneUnion = list(set(oneUnion))
            for i in range(0, len(oneUnion)-1):
                union_count = 1
                if oneUnion[i + 1] - oneUnion[i] > 1:
                    union_count = 2
                    return union_count

            return union_count
                
        def calculate_dice(self):

            list_unique = list(self.Strategy.unique) #2,2,4,4
            dice_value = []

            for i in list_unique:
                x = self.Strategy.count(i)
                if not self.Strategy.strategies['%ds' %i]['done']:
                    dice_value.append(1.1*x*x +2*i) 
                    
                else:
                    dice_value.append(1.0*x * x + 1.1*i)
            np_array = np.array(dice_value)

            return list_unique[np.argmax(np_array)]                      

        def restDiceAverage(self):
            average =0
            for i in range(1,7):
                if not self.Strategy.strategies['%ds' %i]['done']:
                    average = average + (i + i * 5)/2
            return average
            


        def selectDice(self, set_dice = [], type = None):

                
            for i in range(0,5):
                if self.Strategy.dices[i].Dice_Entity.color == color.white50:
                    self.Strategy.dices[i].Dice_Entity.color = color.white
                    self.Strategy.dices[i].move(0, -0.1)
            
            if type == 'Stack':

                for i in set_dice:
                    for j in range(0,5):
                        if i == self.Strategy.dices[j].side:
                            self.Strategy.dices[j].Dice_Entity.color = color.white50
                            invoke(Func(self.Strategy.dices[j].move,0,0.1),delay=2)
            elif type == 'Straight':
                
                use = []
                for i in set_dice:
                    for j in range(0,5):
                        if i == self.Strategy.dices[j].side and not (i in use):
                            self.Strategy.dices[j].Dice_Entity.color = color.white50
                            use.append(i)
                            invoke(Func(self.Strategy.dices[j].move,0, 0.1),delay=2)
                   
            
            invoke(Func( self.AI_roll_controll ),delay=3)  





        def AI_roll_controll(self):

            winsound.PlaySound('sounds\\dice_roll.wav', winsound.SND_ASYNC)

            if self.n_rounds < 12:


                Dice.Dice_Count += 1
                for dice in self.Strategy.dices:
                    dice.roll(0,-0.1)
                    dice.Dice_Entity.on_click = None
                self.Strategy.calculate()
                self.print_Score_board()
                print(self.Strategy.sides)
                print_text.text  = "AI가 주사위를 굴리고 있습니다." + str(Dice.Dice_Count) +"번"#나옴
                invoke(Func(self.Score_Choice), delay=2)
    
    def Game_result(round):
        global record_button
        check_victory = True

        if round == 12:
            print_text.visible = False
            print("gameover")
            if P_strategy.strategies['Total']['score'] > AI_strategy.strategies['Total']['score']:
                print("player win")
                result = Entity(model=Quad(scale=(5, 3.5)), color=color.green, z=-1)
                result_text1 = Text(text="당신이 이겼습니다", scale=2.5, x=-0.25, y=0.19, color=color.black)
                result_text2 = Text(text="점수를 기록할까요?", x=-0.15, y=0.1, color=color.black)
                check_victory = True
                record_button = Button(text='점수 기록하기', color=color.salmon, scale=(0.2,0.1), position=(0, -0.15))
                record_button.on_click = Func(end_of_game.recording, P_strategy.strategies['Total']['score'], record_button, check_victory)


            elif P_strategy.strategies['Total']['score'] < AI_strategy.strategies['Total']['score']:
                print("AI win")
                Entity(model=Quad(scale=(5, 3.5)), color=color.green, z=-1)
                Text(text="AI가 이겼습니다", scale=2.5, x=-0.22, y=0.19, color=color.black)
                result_text2 = Text(text="점수를 기록할까요?", x=-0.15, y=0.1, color=color.black)
                check_victory = False
                record_button = Button(text='점수 기록하기', color=color.salmon, scale=(0.2,0.1), position=(0, -0.15))
                record_button.on_click = Func(end_of_game.recording, P_strategy.strategies['Total']['score'], record_button, check_victory)
            
            else: 
                
                Entity(model=Quad(scale=(5, 3.5)), color=color.green, z=-1)
                Text(text="무승부 입니다.", scale=2.5, x=-0.22, y=0.19, color=color.black)
                result_text2 = Text(text="무승부는 기록되지 않습니다.", x=- 0.21, y=0.1, color=color.black)

            

    

    strategies_order = ['1s', '2s', '3s', '4s', '5s', '6s', 'subtotal', 'Bonus', 'Choice', '4-of-a-kind', 'Full House',
                        'S. Straight', 'L. Straight', 'Yacht', 'Total']
    Player_Strategies = {

        '1s': 0,
        '2s': 0,
        '3s': 0,
        '4s': 0,
        '5s': 0,
        '6s': 0,
        'subtotal': 0,
        'Bonus': 0,
        'Choice': 0,
        '4-of-a-kind': 0,
        'Full House': 0,
        'S. Straight': 0,
        'L. Straight': 0,
        'Yacht': 0,
        'Total': 0

    }

    AI_Strategies = {

        '1s': 0,
        '2s': 0,
        '3s': 0,
        '4s': 0,
        '5s': 0,
        '6s': 0,
        'subtotal': 0,
        'Bonus': 0,
        'Choice': 0,
        '4-of-a-kind': 0,
        'Full House': 0,
        'S. Straight': 0,
        'L. Straight': 0,
        'Yacht': 0,
        'Total': 0

    }
    P_strategy = Strategy(Player_Strategies)

    P_strategy.set_Strategy(0)

    AI_strategy = Strategy(AI_Strategies)
    AI_strategy.set_Strategy(0.0888)

    # 다이스들
    dices = []
    # 다이스 위치 선정
    for i in range(5):
        dice = Dice(i * 1.2 - 2.5)
        dices.append(dice)

    

    # 다이스 저장
    P_strategy.set_dices(dices)
    AI_strategy.set_dices(dices)

    # 게임 메니저 생성
    Player = Player(P_strategy)
    AI_player = AI_Player(AI_strategy)

    # 보드판 생성
    Player.Make_Score_Button()
    AI_player.Make_Score_Button()


    # 다이스 굴리기 버튼
    button_roll = Button(text='Roll', color=color.orange, x=-0.6, scale=0.2, disabled=False)
    button_roll.on_click = Func(Player.roll_controll)

