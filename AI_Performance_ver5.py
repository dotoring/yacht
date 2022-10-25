import random
import numpy as np
class Dice():

    Dice_Count = 0

    def __init__(self):
        self.side = None
        self.Selected = False
    
    def roll(self):

        if self.Dice_Count < 4 and not self.Selected:
            self.side = random.randint(1, 6)


class Strategy():
    def __init__(self, strategies):
        self.strategies = strategies

    def set_dices(self, dices):
        self.dices = dices
    
    def set_Strategy(self):
         for strategy_name in strategies_order:
            self.strategies[strategy_name] = {

                'score': 0,
                'done': False
            
            }
    

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
            
class AI_player:

    def __init__(self, Strategy):
        self.n_rounds = 0
        self.Strategy = Strategy

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
                        
                        if self.restDiceAverage() + self.Strategy.strategies['subtotal']['score'] >= 60:
                            Under_order = [ 'Yacht', '1s', 'Full House', '4-of-a-kind','L. Straight', 'S. Straight' , 
                            'Choice',  '2s', '3s', '4s', '5s', '6s' ]
                        else:
                            Under_order = [ '1s', '2s', '3s',  'Yacht','Full House' , '4-of-a-kind','L. Straight', 'S. Straight' , 
                            'Choice',  '4s', '5s', '6s' ]


                        for i in Under_order:
                          
                            if not self.Strategy.strategies[i]['done']:
                                self.Score_set(i)
                                break     
                else:
                #초이스부터 가장 아래까지 선택            
                        if self.restDiceAverage() + self.Strategy.strategies['subtotal']['score'] >= 60:
                            Under_order = [ 'Yacht', '1s','Full House', '4-of-a-kind','L. Straight', 'S. Straight' , 
                            'Choice', '1s', '2s', '3s', '4s', '5s', '6s' ]
                        else:
                            Under_order = [ '1s', '2s', '3s',  'Yacht','Full House' , '4-of-a-kind','L. Straight', 'S. Straight' , 
                            'Choice',  '4s', '5s', '6s' ]

                        for i in Under_order:
                          
                            if not self.Strategy.strategies[i]['done']:
                                self.Score_set(i)
                                break    

    def Score_set(self, score_name):

        self.n_rounds +=1
        self.Strategy.strategies[score_name]['done'] = True
        
        for dice in dices:
                dice.Selected = False

        self.Strategy.Part_caculate()

        Dice.Dice_Count = 0

    def Under_union_max(self):

        Under_order = ['4-of-a-kind', 'Full House',
                    'S. Straight', 'L. Straight', 'Yacht']
        #아래 조합 수 배열로 만들기
        Under_order_array = [self.Strategy.strategies[x]['score'] if self.Strategy.strategies[x]['done'] == False else 0 for x in Under_order]
        Max = max(Under_order_array)
        for x in Under_order:
            if Max == self.Strategy.strategies[x]['score']:
                return x if Max != 0 else 0 #Noe값이 나오는 경우 생각해보자
        return 0

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

        list_unique = list(self.Strategy.unique)
        list_count = []
        dice_value = []
        for i in range(1,7):
            if  self.Strategy.count(i) > 0:
                list_count.append(self.Strategy.count(i))

        for i in list_unique:
            x = self.Strategy.count(i)
            if not self.Strategy.strategies['%ds' %i]['done']:
                dice_value.append(1.1*x*x +2*i)
                
            else:
                dice_value.append(0.95*x * x + 1.1*i)
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
            if self.Strategy.dices[i].Selected == True:
                self.Strategy.dices[i].Selected = False

        
        if type == 'Stack':

            for i in set_dice:
                for j in range(0,5):
                    if i == self.Strategy.dices[j].side:
                        self.Strategy.dices[j].Selected = True


        elif type == 'Straight':
            
            use = []
            for i in set_dice:
                for j in range(0,5):
                    if i == self.Strategy.dices[j].side and not (i in use):
                        self.Strategy.dices[j].Selected = True
                        use.append(i)

        self.AI_roll_controll()


    def AI_roll_controll(self):
        if self.n_rounds < 12:
            
            Dice.Dice_Count += 1
            for dice in  self.Strategy.dices:
                dice.roll()

            self.Strategy.calculate()
            self.Score_Choice()

 

strategies_order = [ '1s', '2s', '3s', '4s', '5s', '6s', 'subtotal', 'Bonus', 'Choice', '4-of-a-kind', 'Full House',
                    'S. Straight', 'L. Straight', 'Yacht', 'Total' ]

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

dices = []
for i in range(5):

    dice = Dice()
    dices.append(dice)

AI_strategy = Strategy(AI_Strategies)
AI_strategy.set_Strategy()

AI_strategy.set_dices(dices)

AI_player = AI_player(AI_strategy)
x = 0
total=0

for _ in range( 12000 ):
    x += 1
    AI_player.AI_roll_controll()
    if x == 12:
        total += AI_strategy.strategies['Total']['score']
        AI_strategy.reset()
        AI_player.n_rounds = 0
        x = 0
    
print( total / 1000 )
'''
for _ in range(12):
    AI_player.AI_roll_controll()
for name in strategies_order:

    print( name + ": " + str(AI_strategy.strategies[name]['score']))
'''

''' 
1s: 4
2s: 2
3s: 12
4s: 12
5s: 15
6s: 18
subtotal: 63
Bonus: 35
Choice: 28
4-of-a-kind: 0
Full House: 18
S. Straight: 15
L. Straight: 30
Yacht: 0
Total: 189
'''

