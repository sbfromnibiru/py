import pygame
from random import randint

def tuple_to_str(t):
        return str(t[0]) + ', ' + str(t[1])

class Snake:
    def __init__(self, win, divide):
        self.win = win
        self.divide = divide
        self.matrix = {}
        for rcw in range(int(self.win.get_size()[0]/self.divide)):
            for rch in range(int(self.win.get_size()[1]/self.divide)):
                self.matrix[str(rcw) + ', ' + str(rch)] = 0
        self.dir = (-1, 0)
        self.apple_count = 0
        self.start_on = (int(self.win.get_size()[0]/self.divide/2), int(self.win.get_size()[1]/self.divide/2))
        self.length = [self.start_on]
        self.last_l = [self.start_on]

    def update_length(self):
        for pixel in self.length:
            self.matrix[tuple_to_str(pixel)] = 1

    def draw(self):
        self.update_length()
        for col in self.matrix:
            if self.matrix[col] == 1:
                x, y = col.split(', ')
                x, y = int(x), int(y)
                t_col = (x, y)
                if t_col in self.length:
                    pygame.draw.rect(self.win, (0, 255, 0), (x*self.divide, y*self.divide, self.divide, self.divide))
                else:
                    pygame.draw.rect(self.win, (0, 0, 0), (x*self.divide, y*self.divide, self.divide, self.divide))

            if self.matrix[col] == 0:
                x, y = col.split(', ')
                x, y = int(x), int(y)
                pygame.draw.rect(self.win, (0, 0, 0), (x*self.divide, y*self.divide, self.divide, self.divide))


    def check_if_snake_died(self):
        for item in self.length:
            if self.length.count(item) == 2:
                return True
        if self.length[0][0] >= self.win.get_size()[0]/self.divide or self.length[0][0] < 0 or self.length[0][1] < 0 or self.length[0][1] >= self.win.get_size()[1]/self.divide:
            return True

    def move(self):
        self.last_l.append(self.length[-1])
        del self.last_l[0]
        for p in reversed(range(len(self.length))):
            if p != 0:
                self.length[p] = self.length[p-1]

        if self.dir[0] == 1 and self.dir[1] == 0:
            self.length[0] = (self.length[0][0]+1, self.length[0][1])

        elif self.dir[0] == -1 and self.dir[1] == 0:
            self.length[0] = (self.length[0][0]-1, self.length[0][1])

        elif self.dir[0] == 0 and self.dir[1] == 1:
            self.length[0] = (self.length[0][0], self.length[0][1]-1)

        elif self.dir[0] == 0 and self.dir[1] == -1:
            self.length[0] = (self.length[0][0], self.length[0][1]+1)

class Apple:
    def __init__(self, win, pos, divide):
        self.win = win
        self.pos = pos
        self.divide = divide

    def draw(self):
        pygame.draw.rect(self.win, (255, 0, 0), (self.pos[0]*self.divide, self.pos[1]*self.divide, self.divide, self.divide))

class Game:
    def __init__(self):
        self.width = 675
        self.height = 675
        self.divide = 15
        self.win = pygame.display.set_mode((self.width, self.height))
        self.snake = Snake(self.win, self.divide)
        self.apple = Apple(self.win, (randint(0, self.width/self.divide-1), randint(0, self.height/self.divide-1)), self.divide)
        self.point = 0
        self.velocity = 0
        self.acceleration = 1
        self.start_velocity = 50
        self.move_que = []

    def run(self):
        run = True

        movevent = pygame.USEREVENT + 1

        pygame.time.set_timer(movevent, self.start_velocity)

        clock = pygame.time.Clock()

        while run:
            clock.tick()

            if self.apple.pos in self.snake.length:
                self.snake.length.append(self.snake.last_l[0])
                self.apple = Apple(self.win, (randint(0, self.width/self.divide-1), randint(0, self.height/self.divide-1)), self.divide)
                self.point += 1
                self.velocity = self.point*self.acceleration
                pygame.time.set_timer(movevent, self.start_velocity-self.velocity)

            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if self.snake.dir[1] != -1 and self.snake.dir[1] != 1:
                            self.move_que.append((0, 1))
                    if event.key == pygame.K_a:
                        if self.snake.dir[0] != -1 and self.snake.dir[0] != 1:
                            self.move_que.append((-1, 0))
                    if event.key == pygame.K_s:
                        if self.snake.dir[1] != -1 and self.snake.dir[1] != 1:
                            self.move_que.append((0, -1))
                    if event.key == pygame.K_d:
                        if self.snake.dir[0] != -1 and self.snake.dir[0] != 1:
                            self.move_que.append((1, 0))

                if event.type == movevent:
                    if len(self.move_que) != 0:
                        self.snake.dir = self.move_que[0]
                        del self.move_que[0]
                    self.snake.move()

            if self.snake.check_if_snake_died():
                print(self.point)
                print()
                run = False

        pygame.quit()

    def draw(self):
        self.snake.draw()
        self.apple.draw()
        pygame.display.flip()


a = Game()

a.run()