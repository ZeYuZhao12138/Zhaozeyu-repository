# 2022/03/17 15:37
# have a good day!
import random
import sys
import pygame

def initial_map():
    map = [[1,1,1,0,0,1,1,1,1,1],
           [1,0,1,1,1,1,0,1,1,0],
           [1,0,1,0,0,1,0,0,1,0],
           [1,1,1,1,1,1,1,1,1,0],
           [1,0,1,0,0,1,1,0,1,0],
           [1,1,1,1,0,1,0,0,1,1],
           [0,0,1,1,1,1,1,1,1,0],
           [0,0,1,0,1,0,1,0,1,0],
           [0,1,1,1,1,0,1,1,1,0],
           [1,1,0,0,0,0,0,0,1,1]]
    birth_place = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 1:
                birth_place.append(i*len(map)+j)
    return map, birth_place


def possiblly_choice(options, possibility):
    if not len(options) == len(possibility):
        raise Exception('选项列表的长度与概率的长度不一致！')
    elif max(possibility) > 1:
        raise Exception('概率值应该在0～1之间！')
    elif sum(possibility) > 1:
        raise Exception('所有概率值之和应该小于等于1！')
    else:
        pin = random.uniform(0, 1)
        for n in range(len(possibility)):
            if sum(possibility[:n]) < pin <= sum(possibility[:n + 1]):
                return options[n]
        return None


class agent:
    def __init__(self):
        self.state = random.choice(birth_place)   # random.randint(0, 100)
        self.epuse = 0.3  # 随机行为概率
        self.vision = 0.8

    def move(self, new_state='random'):
        if not new_state == 'random':
            self.state = new_state
        else:
            pin = possiblly_choice(['random', 'most_possible'], [self.epuse, 1 - self.epuse])
            choises = []
            for index in range(len(R[self.state])):
                if not R[self.state][index] == -1:
                    choises.append(index)
                else:
                    pass

            if pin == 'random':
                result = random.choice(choises)
                self.state = (self.state-10 if result == 0 else     # 重新计算移动后的位置
                              self.state+10 if result == 1 else
                              self.state-1 if result == 2 else
                              self.state+1)
            else:
                most_possible_state = []
                MAX = max([Q[self.state][index] for index in choises])

                for index in choises:
                    if Q[self.state][index] == MAX:
                        most_possible_state.append(index)
                result = random.choice(most_possible_state)
                self.state = (self.state - 10 if result == 0 else  # 重新计算移动后的位置
                              self.state + 10 if result == 1 else
                              self.state - 1 if result == 2 else
                              self.state + 1)
            return result



def initial_R():
    options_amount = 4 #  上下左右
    map, birth_place = initial_map()
    R = [[-1 for i in range(options_amount)] for j in range(len(map)*len(map[0]))]
    #  确定通路
    for row in range(len(map)):
        for column in range(len(map[row])):
            # 判断是否为边界
            R[row*len(map)+column][0] = (-1 if row-1 < 0 else
                                         -1 if map[row-1][column] == 0 else
                                         0)
            R[row*len(map)+column][1] = (-1 if row+1 >= len(map) else
                                         -1 if map[row+1][column] == 0 else
                                         0)
            R[row*len(map)+column][2] = (-1 if column-1 < 0 else
                                         -1 if map[row][column-1] == 0 else
                                         0)
            R[row*len(map)+column][3] = (-1 if column+1 >= len(map[row]) else
                                         -1 if map[row][column+1] == 0 else
                                         0)
    # 终点随机化
    end_point = random.choice(birth_place)
    choises = []
    for index in range(len(R[end_point])):
        if not R[end_point][index] == -1:
            choises.append(index)
        else:
            pass
    if 0 in choises:
        R[end_point-10][1] = 100
    if 1 in choises:
        R[end_point+10][0] = 100
    if 2 in choises:
        R[end_point-1][3] = 100
    if 3 in choises:
        R[end_point+1][2] = 100


    # R[1][2] = 100
    # R[10][0] = 100
    # R = [[-1 for i in range(6)] for j in range(6)]
    # R[0][4] = 0
    # R[1][3] = 0
    # R[2][3] = 0
    # R[3][1] = 0
    # R[3][2] = 0
    # R[3][4] = 0
    # R[4][0] = 0
    # R[4][3] = 0
    # R[5][1] = 0
    # R[5][4] = 0
    # R[1][5] = 100
    # R[4][5] = 100
    # R[5][5] = 100
    return R, end_point


def initial_Q():
    Q = [[0 for i in range(4)] for j in range(100)]
    return Q


if __name__ == '__main__':
    R, end_point = initial_R()  # 初始化R table
    for i in range(len(R)):
        print(R[i])

    print('')
    Q = initial_Q()  # 初始化Q table
    for i in range(len(Q)):
        print(Q[i])

    TIMES = 1000
    map, birth_place = initial_map()
    bob = agent()
    for number in range(TIMES):
        bob = agent()  # 初始化一个个体
        end = False
        while not end:
            start = bob.state
            stop = bob.move()

            choises = []
            for index in range(len(R[bob.state])):
                if not R[bob.state][index] == -1:
                    choises.append(index)
                else:
                    pass

            Q[start][stop] = R[start][stop] + bob.vision * max([Q[bob.state][index] for index in choises])

            if bob.state == end_point:
                end = True
    print('')
    for i in range(len(Q)):
        print(Q[i])

    #  可视化处理
    BLOCK = (50, 50)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    WHITE = (233, 233, 233)
    YELLOW = (255, 255, 0)
    SIZE = ((len(map)+2)*50, (len(map[0])+2)*50)

    #  初始化
    pygame.init()
    #  创建游戏窗口
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('bob走迷宫')

    #  生成背景
    screen.fill(BLACK)
    Rects = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            Rects.append(pygame.Rect(((j+1)*50, (i+1)*50), BLOCK))   #  在屏幕上画一堆矩形
    for i in range(len(map)):
        for j in range(len(map[i])):
            pygame.draw.rect(screen, BLACK if map[i][j] == 0 else WHITE, Rects[j+i*len(map[j])])
    pygame.draw.rect(screen, YELLOW, (((end_point%10+1)*50, (end_point//10+1)*50),BLOCK))
    # bob登场
    bob = agent()
    bob.epuse = 0 # bob 乱走的几率
    # 画出bob位置
    pygame.draw.rect(screen, RED, (((bob.state % 10 + 1)*50, (bob.state // 10 + 1)*50), BLOCK))
    #  第一次显示
    pygame.display.flip()

    #  让游戏保持运行的状态
    while True:
        #  检测事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    if bob.state == end_point:
                        bob = agent()
                        bob.epuse = 0
                    else:
                        bob.move()

        screen.fill(BLACK)
        for i in range(len(map)):
            for j in range(len(map[i])):
                pygame.draw.rect(screen, BLACK if map[i][j] == 0 else WHITE, Rects[j + i * len(map[j])])

        pygame.draw.rect(screen, YELLOW, (((end_point % 10 + 1) * 50, (end_point // 10 + 1) * 50), BLOCK))
        pygame.draw.rect(screen, RED, (((bob.state % 10 + 1) * 50, (bob.state // 10 + 1) * 50), BLOCK))
        pygame.display.update()
