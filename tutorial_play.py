from ursina import *
import winsound


def play():
    Text.default_font = 'NanumGothicCoding.ttf'

    print_text = Text(text="", x=-0.6, y=0.2)
    player_text = Text(text="Player", x=-0.65, y=-0.29, color=color.black)
    player_text.create_background(radius=0, padding=0.01, color=color.white)
    Score_board = Entity(model='quad', texture='Score_borad_v2.png', scale=(3, 7), x=5.0, y=0.3)
    
    dice_counts = [[1, 1, 1, 1, 1], [1, 1, 1, 2, 2], [1, 2, 3, 4, 5], [4, 4, 4, 4, 5]]


    class Dice():

        tutorial_count = 0
        Dice_Count = 0

        def __init__(self, x):
            self.side = None
            self.x = x - 0.5
            self.y = 0
            self.Dice_Entity = Entity(color=color.white)
            # 다이스 삭제여부 검사

        # 다이스 굴리기
        def roll(self, distance, height):

            if self.Dice_Count < 4 and self.Dice_Entity.color == color.white:
                if Player.n_rounds == 0:
                    self.side = random.randint(1, 6)
                else:
                    self.side = dice_counts[Player.n_rounds - 1][Dice.tutorial_count]

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
                self.move(distance, -height)
            else:
                self.Dice_Entity.color = color.white50
                self.move(distance, height)

        def roll_count(self):
            if Dice.Dice_Count == 1:
                self.count1 = Entity(model='circle', scale=(0.2, 0.2), position=(-1.0, -1.2))
                self.count2 = Entity(model='circle', scale=(0.2, 0.2), position=(-0.5, -1.2))

            if Dice.Dice_Count == 2:
                destroy(self.count1)
            if Dice.Dice_Count == 3:
                destroy(self.count2)

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
                                          , text_color=color.black33, scale=(0.05, 0.05), enabled=False,
                                          name=strategy_name)

                else:
                    Score_Button = Button(text=str(self.Strategy.strategies[strategy_name]['score']),
                                          color=Color(0, 0, 0, 0), position=(
                            self.Strategy.strategies[strategy_name]['position'][0],
                            self.Strategy.strategies[strategy_name]['position'][1])
                                          , text_color=color.black, scale=(0.05, 0.05), enabled=False,
                                          name=strategy_name)

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

        print_text.text = "Roll버튼을 눌러 주사위를 굴릴 수 있습니다."

        def Score_Click(self):
            e = mouse.hovered_entity
            if not (self.Strategy.strategies[e.name]['done']):
                winsound.PlaySound('sounds\\click2.wav', winsound.SND_ASYNC)

                e.text_color = color.black
                # strategy.score_update()
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
                destroy(dice.count1)
                destroy(dice.count2)

                

        def roll_controll(self):
            # 라운드가 12이하라면
            if self.n_rounds < 5:
                winsound.PlaySound('sounds\\dice_roll.wav', winsound.SND_ASYNC)
                # Dice 객체의 count가 1증가
                Dice.Dice_Count += 1
                Dice.tutorial_count = 0

                for i, dice in enumerate(self.Strategy.dices):
                    dice.roll(0, -0.1)
                    Dice.tutorial_count = Dice.tutorial_count + 1

                self.Strategy.calculate()
                self.print_Score_board()
                dice.roll_count()
                if(self.n_rounds == 0):
                    print_text.text  = "주사위는 3번까지 굴릴 수 있습니다. 주사위를 선택하면 저장할 수 있습니다."
                    if(Dice.Dice_Count == 3):
                        print_text.text = "오른쪽 점수를 선택하면 해당하는 점수를 얻습니다."
                if(self.n_rounds == 1):
                    print_text.text  = "같은 수가 5개 나오면 yacht로 50점을 얻을 수 있습니다."
                if(self.n_rounds == 2):
                    print_text.text  = "동일한 주사위 눈이 각각 3개, 2개일 때, 주사위 눈 5개의 총합을 점수로 얻습니다."
                if(self.n_rounds == 3):
                    print_text.text  = "연속된 수가 4개면 S.Straight로 15점 5개면 L.Straight로 30점을 얻을 수 있습니다."
                if(self.n_rounds == 4):
                    print_text.text  = "같은 수가 4개 나오면 4 of a Kind로 모든 주사위 눈의 총합을 점수로 얻습니다."
                print(self.Strategy.sides)

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
    # strategy 객체 만들기
    P_strategy = Strategy(Player_Strategies)

    P_strategy.set_Strategy(0)

    # 다이스들
    dices = []
    # 다이스 위치 선정
    for i in range(5):
        dice = Dice(i * 1.2 - 2.5)
        dices.append(dice)

    # 다이스 저장
    P_strategy.set_dices(dices)

    # 게임 메니저 생성
    Player = Player(P_strategy)

    # 보드판 생성
    Player.Make_Score_Button()

    # 다이스 굴리기 버튼
    button_roll = Button(text='Roll', color=color.orange, x=-0.6, scale=0.2, disabled=False)
    button_roll.on_click = Func(Player.roll_controll)
