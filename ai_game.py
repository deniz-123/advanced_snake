import pygame
import random
import math
import numpy as np

class Node:
    def __init__(self,  height, width, color, position):
        self.height = height
        self.width = width
        self.color = color
        self.nodes = []
        self.position = [position[0]*height,position[1]*width]

    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.position[0], self.position[1], self.width, self.height))

class Snake(Node):
    def __init__(self, height, width, color, position):
        Node.__init__(self, height, width, color, position)
        self.direction = [-1,0]
        for i in range(1,3):
            temp_node = Node(height,width,color,[position[0] + i,position[1]])
            self.nodes.append(temp_node)

    def change_direction(self, directions):
        if directions[0] != (-1)*self.direction[0] or directions[1] != (-1)*self.direction[1]:
            self.direction = directions

    def move(self, HEIGHT, WIDTH, action):
        for i in range(0,len(self.nodes)):
            if i == len(self.nodes) - 1:
                self.nodes[len(self.nodes) - i - 1].position = [self.position[0],self.position[1]]
            else:
                self.nodes[len(self.nodes) - i - 1].position = [self.nodes[len(self.nodes) - i - 2].position[0],self.nodes[len(self.nodes) - i - 2].position[1]]

        if np.array_equal(action, [1,0,0]):
            # no change at direction
            self.position[0] += self.direction[0]*self.width
            self.position[1] += self.direction[1]*self.height

            if self.position[0]+self.width == 0:
                self.position[0] = WIDTH
            elif self.position[0] == WIDTH:
                self.position[0] = 0
            elif self.position[1]+self.height == 0:
                self.position[1] = HEIGHT
            elif self.position[1] == HEIGHT:
                self.position[1] = 0
        elif np.array_equal(action, [0,1,0]):
            # turn right / set direction
            if self.direction == [1,0]:
                self.direction = [0,1]
            elif self.direction == [0,1]:
                self.direction = [-1,0]
            elif self.direction == [-1,0]:
                self.direction = [0,-1]
            elif self.direction == [0,-1]:
                self.direction = [1,0]

            # move
            self.position[0] += self.direction[0]*self.width
            self.position[1] += self.direction[1]*self.height

            if self.position[0]+self.width == 0:
                self.position[0] = WIDTH
            elif self.position[0] == WIDTH:
                self.position[0] = 0
            elif self.position[1]+self.height == 0:
                self.position[1] = HEIGHT
            elif self.position[1] == HEIGHT:
                self.position[1] = 0
        elif np.array_equal(action,[0,0,1]):
            # turn left / set direction
            if self.direction == [1,0]:
                self.direction = [0,-1]
            elif self.direction == [0,-1]:
                self.direction = [-1,0]
            elif self.direction == [-1,0]:
                self.direction = [0,1]
            elif self.direction == [0,1]:
                self.direction = [1,0]

            # move
            self.position[0] += self.direction[0]*self.width
            self.position[1] += self.direction[1]*self.height

            if self.position[0]+self.width == 0:
                self.position[0] = WIDTH
            elif self.position[0] == WIDTH:
                self.position[0] = 0
            elif self.position[1]+self.height == 0:
                self.position[1] = HEIGHT
            elif self.position[1] == HEIGHT:
                self.position[1] = 0
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.position[0], self.position[1], self.width, self.height))
        for node in self.nodes:
            node.draw(window)


class Food(Node):
    def __init__(self, height, width, color, position):
        Node.__init__(self,height, width, color, position)

    def place(self, player, enemy, max_width, max_height):
        can_place = True
        self.position[0] = random.randint(0,max_width//self.width - 1)*self.width
        self.position[1] = random.randint(0,max_height//self.height - 1)*self.height

        if self.position == player.position or self.position == enemy.position:
            self.place(player, enemy, max_width, max_height)
        else:
            for player_tail in player.nodes:
               if self.position == player_tail.position:
                    can_place = False
                    break
            if can_place:
                for enemy_tail in enemy.nodes:
                    if self.position == enemy_tail.position:
                        self.place(player, enemy, max_width, max_height)
                        break
                    


class Enemy(Node):
    def __init__(self, height, width, color, position):
        Node.__init__(self,height, width, color, position)
        self.direction = [-1,0]
        for i in range(1,3):
            temp_node = Node(height,width,color,[position[0] + i,position[1]])
            self.nodes.append(temp_node)

    def chase(self,head, max_height, max_width, move):
        
        if move == True:
            for i in range(0,len(self.nodes)):
                if i == len(self.nodes) - 1:
                    self.nodes[len(self.nodes) - i - 1].position = [self.position[0],self.position[1]]
                else:
                    self.nodes[len(self.nodes) - i - 1].position = [self.nodes[len(self.nodes) - i - 2].position[0],self.nodes[len(self.nodes) - i - 2].position[1]]
                min_distance = heuristic(self.position, head.position)
                
            for tail in head.nodes:
                temp = heuristic(self.position, tail.position)
                if(temp[2] < min_distance[2]):
                    min_distance = temp

            if self.position[0] - min_distance[0] < 0 and self.position[1] - min_distance[1] == 0:
                if self.direction[0] == -1 and self.direction[1] == 0:
                    if self.position[1] <= max_height//2:
                        self.direction = [0,-1]
                    else:
                        self.direction = [0,1]
                else:
                    self.direction = [1,0]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
            elif self.position[0] - min_distance[0] > 0 and self.position[1] - min_distance[1] == 0:
                if self.direction[0] == 1 and self.direction[1] == 0:
                    if self.position[1] <= max_height//2:
                        self.direction = [0,-1]
                    else:
                        self.direction = [0,1]
                else:
                    self.direction = [-1,0]
                #self.direction = [-1,0]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
            elif self.position[0] - min_distance[0] == 0 and self.position[1] - min_distance[1] < 0:
                if self.direction[0] == 0 and self.direction[1] == -1:
                    if self.position[0] <= max_width//2:
                        self.direction = [1,0]
                    else:
                        self.direction = [-1,0]
                else:
                    self.direction = [0,1]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
            elif self.position[0] - min_distance[0] == 0 and self.position[1] - min_distance[1] > 0:
                if self.direction[0] == 0 and self.direction[1] == 1:
                    if self.position[0] <= max_width//2:
                        self.direction = [1,0]
                    else:
                        self.direction = [-1,0]
                else:
                    self.direction = [0,-1]
                
                #self.direction = [0,-1]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
            elif self.position[0] - min_distance[0] < 0 and self.position[1] - min_distance[1] > 0:
                if abs(min_distance[0] - self.position[0]) < abs(min_distance[1] - self.position[1]):
                    if self.direction[0] == -1 and self.direction[1] == 0:
                        if self.position[1] <= max_height//2:
                            self.direction = [0,-1]
                        else:
                            self.direction = [0,1]
                    else:
                        self.direction = [1,0]
                    self.position[0] += self.direction[0]*self.width
                    self.position[1] += self.direction[1]*self.height
                else:
                    if self.direction[0] == 0 and self.direction[1] == 1:
                        if self.position[0] <= max_width//2:
                            self.direction = [1,0]
                        else:
                            self.direction = [-1,0]
                    else:
                        self.direction = [0,-1]
                    self.position[0] += self.direction[0]*self.width
                    self.position[1] += self.direction[1]*self.height
            elif self.position[0] - min_distance[0] < 0 and self.position[1] - min_distance[1] < 0:
                if abs(min_distance[0] - self.position[0]) < abs(min_distance[1] - self.position[1]):
                    if self.direction[0] == -1 and self.direction[1] == 0:
                        if self.position[1] <= max_height//2:
                            self.direction = [0,-1]
                        else:
                            self.direction = [0,1]
                    else:
                        self.direction = [1,0]
                    self.position[0] += self.direction[0]*self.width
                    self.position[1] += self.direction[1]*self.height
                else:
                    if self.direction[0] == 0 and self.direction[1] == -1:
                        if self.position[0] <= max_width//2:
                            self.direction = [1,0]
                        else:
                            self.direction = [-1,0]
                    else:
                        self.direction = [0,1]
                    self.position[0] += self.direction[0]*self.width
                    self.position[1] += self.direction[1]*self.height
            elif self.position[0] - min_distance[0] > 0 and self.position[1] - min_distance[1] < 0:
                if abs(min_distance[0] - self.position[0]) < abs(min_distance[1] - self.position[1]):
                    if self.direction[0] == 1 and self.direction[1] == 0:
                        if self.position[1] <= max_height//2:
                            self.direction = [0,-1]
                        else:
                            self.direction = [0,1]
                    else:
                        self.direction = [-1,0]
                    self.position[0] += self.direction[0]*self.width
                    self.position[1] += self.direction[1]*self.height
                else:
                    if self.direction[0] == 0 and self.direction[1] == -1:
                        if self.position[0] <= max_width//2:
                            self.direction = [1,0]
                        else:
                            self.direction = [-1,0]
                    else:
                        self.direction = [0,1]
                    self.position[0] += self.direction[0]*self.width
                    self.position[1] += self.direction[1]*self.height
            elif self.position[0] - min_distance[0] > 0 and self.position[1] - min_distance[1] > 0:
                if abs(min_distance[0] - self.position[0]) < abs(min_distance[1] - self.position[1]):
                    if self.direction[0] == 1 and self.direction[1] == 0:
                        if self.position[1] <= max_height//2:
                            self.direction = [0,-1]
                        else:
                            self.direction = [0,1]
                    else:
                        self.direction = [-1,0]
                    self.position[0] += self.direction[0]*self.width
                    self.position[1] += self.direction[1]*self.height
                else:
                    if self.direction[0] == 0 and self.direction[1] == 1:
                        if self.position[0] <= max_width//2:
                            self.direction = [1,0]
                        else:
                            self.direction = [-1,0]
                    else:
                        self.direction = [0,-1]
                    self.position[0] += self.direction[0]*self.width
                    self.position[1] += self.direction[1]*self.height
                
    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.position[0], self.position[1], self.width, self.height))
        for node in self.nodes:
            node.draw(window)

class SnakeGameAI():
    def __init__(self):
        # variables
        self.snake = None
        self.enemy = None
        self.food = None
        self.clock = None
        self.objects = None
        self.text = None
        self.frame_iteration = None
        self.score = None
        self.enemy_move = None
        self.fps = 120
        # constants
        self.WIDTH = 800
        self.HEIGHT = 600
        self.NODE_HEIGHT = 20
        self.NODE_WIDTH = 20
        self.UP = [0,-1]
        self.RIGHT = [1,0]
        self.DOWN = [0,1]
        self.LEFT = [-1,0]
        # colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.ORANGE = (255,165,0)
        self.YELLOW = (255,255,0)
        self.RED = (255,0,0)
        # init pygame
        pygame.init()
        self.font = pygame.font.SysFont('arial', 25)
        self.window = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.window.fill(self.BLACK)
        pygame.display.set_caption("Advanced Snake Game With AI")
        # init game
        self.restart()

    def draw_grid(self, width, height, n_width, n_height, window, color):
        rows = height // n_height
        columns = width // n_width
        width_gap = n_width
        height_gap = n_height
        for i in range(int(columns)):
            pygame.draw.line(window, color, (i*width_gap,0), (i*width_gap, height))
            for j in range(int(rows)):
                pygame.draw.line(window, color, (0,j*height_gap), (width,j*height_gap))

    def update(self, objects, width, height, n_width, n_height, window, color_lines, color_grid):
        # update grid and positions of objects
        window.fill(color_grid)
        for node in objects:
            node.draw(window)
        self.draw_grid(width, height, n_width, n_height, window, color_lines)
        self.text = self.font.render("Score: " + str(self.score), True, self.WHITE)
        self.window.blit(self.text, [0, 0])
        pygame.display.update()

    def restart(self):
        # 0 = snake, 1 = enemy, 2 = food
        self.snake = Snake(self.NODE_HEIGHT, self.NODE_WIDTH, self.YELLOW, [int(self.WIDTH//self.NODE_WIDTH)//2,int(self.HEIGHT//self.NODE_HEIGHT)//2])
        self.food = Food(self.NODE_HEIGHT, self.NODE_WIDTH, self.RED, [random.randint(0,self.WIDTH//self.NODE_WIDTH - self.NODE_WIDTH),random.randint(0,self.HEIGHT//self.NODE_HEIGHT - self.NODE_HEIGHT)])
        self.enemy = Enemy(self.NODE_HEIGHT, self.NODE_WIDTH, self.ORANGE, [self.WIDTH//self.NODE_WIDTH-3,0])
        self.objects = [self.snake,self.enemy,self.food]
        self.clock = pygame.time.Clock()
        self.score = 0
        self.frame_iteration = 0
        self.enemy_move = 0

    def collision(self, addx = 0, addy = 0):
        # directions
        right = [1,0]
        down = [0,1]
        left = [-1,0]
        up = [0,-1]
        # snake and enemy
        snake = self.snake
        enemy = self.enemy
        # positions
        snake_pos = snake.position
        enemy_pos = enemy.position
        # directions
        snake_dir = snake.direction
        enemy_dir = enemy.direction

        if addx != 0 or addy != 0:
            s_length = len(snake.nodes) + 1
            for tail in enemy.nodes:
                if ((snake_pos[1] == tail.position[1] and  snake_pos[0] == self.WIDTH - snake.width and tail.position[0] >= self.WIDTH - (s_length-1)*(snake.width)) or (snake_pos[1] == tail.position[1] and snake_pos[0] == snake.width and tail.position[0] <= (s_length-1)*(snake.width)) or (snake_pos[0] == tail.position[0] and snake_pos[1] == self.HEIGHT - snake.height and tail.position[1] >= self.HEIGHT - (s_length-1)*(snake.height)) or (snake_pos[0] == tail.position[0] and snake_pos[1] == snake.height and tail.position[1] <= (s_length-1)*(snake.height))):
                    return True
            
            # head collisions
            if ((snake_pos[1] == enemy_pos[1] and  snake_pos[0] == self.WIDTH - snake.width and enemy_pos[0] >= self.WIDTH - (s_length-1)*(snake.width)) or (snake_pos[1] == enemy_pos[1] and snake_pos[0] == snake.width and enemy_pos[0] <= (s_length-1)*(snake.width)) or (snake_pos[0] == enemy_pos[0] and snake_pos[1] == self.HEIGHT - snake.height and enemy_pos[1] >= self.HEIGHT - (s_length-1)*(snake.height)) or (snake_pos[0] == enemy_pos[0] and snake_pos[1] == snake.height and enemy_pos[1] <= (s_length-1)*(snake.height))):
                return True
            else: # snake_dir[0] == -enemy_dir[0] and snake_dir[1] == -enemy_dir[1]:
                if (snake_pos[0] <= enemy_pos[0] + s_length*addx and snake_pos[1] == enemy_pos[1]) or (snake_pos[0] >= enemy_pos[0] - s_length*addx and snake_pos[1] == enemy_pos[1]) or (snake_pos[1] >= enemy_pos[1] - s_length*addy and snake_pos[0] == enemy_pos[0]) or (snake_pos[1] <= enemy_pos[1] + s_length*addy and snake_pos[0] == enemy_pos[0]):
                    True

            # snake head in snake body
            for tail in snake.nodes:
                if snake_pos[0] == tail.position[0] + addx and snake_pos[1] == tail.position[1] + addy:
                    return True

            # enemy head in snake body
            k = len(snake.nodes)
            for tail in snake.nodes:
                if ((enemy_pos[1] == tail.position[1] and enemy_pos[0] == self.WIDTH - snake.width and tail.position[0] >= self.WIDTH - (k)*(snake.width)) or (enemy_pos[1] == tail.position[1] and enemy_pos[0] == snake.width and tail.position[0] <= (k)*(snake.width)) or (enemy_pos[0] == tail.position[0] and enemy_pos[1] == self.HEIGHT - snake.height and tail.position[1] >= self.HEIGHT - (k)*(snake.height)) or (enemy_pos[0] == tail.position[0] and enemy_pos[1] == snake.height and tail.position[1] <= (k)*(snake.height))):
                    return True
                k -= 1

            # snake head in enemy body
            k = len(enemy.nodes)
            for tail in enemy.nodes:
                if ((snake_pos[1] == tail.position[1] and snake_pos[0] == self.WIDTH - snake.width and tail.position[0] >= self.WIDTH - (k)*(snake.width)) or (snake_pos[1] == tail.position[1] and snake_pos[0] == snake.width and tail.position[0] <= (k)*(snake.width)) or (snake_pos[0] == tail.position[0] and snake_pos[1] == self.HEIGHT - snake.height and tail.position[1] >= self.HEIGHT - (k)*(snake.height)) or (snake_pos[0] == tail.position[0] and snake_pos[1] == snake.height and tail.position[1] <= (k)*(snake.height))):
                    return True
                k -= 1

            return False
        else:
            # snake head in snake body
            for tail in snake.nodes:
                if snake_pos[0] == tail.position[0] and snake_pos[1] == tail.position[1]:
                    return True
            
            # snake head in enemy body
            for tail in enemy.nodes:
                if snake_pos[0] == tail.position[0] and snake_pos[1] == tail.position[1]:
                    return True

            # enemy head in snake body
            for tail in snake.nodes:
                if enemy_pos[0] == tail.position[0] and enemy_pos[1] == tail.position[1]:
                    return True
            
            # heads united
            if enemy_pos == snake_pos:
                return True

            return False

    def play(self, action):
        self.frame_iteration += 1
        self.enemy_move += 1
        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.fps == 120:
                        self.fps = 20
                    elif self.fps == 20:
                        self.fps = 5
                    else:
                        self.fps = 120

        
        # move
        self.snake.move(self.HEIGHT,self.WIDTH, action)
        enemy_can_chase = self.enemy_move % 2 == 0 or self.enemy_move == 0
        self.enemy.chase(self.snake,self.HEIGHT,self.WIDTH, enemy_can_chase)

        # game over?
        reward = 0
        game_over = False

        if self.collision() or self.frame_iteration > 100*(len(self.snake.nodes) + 1):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # place new food
        if self.snake.position == self.food.position:
            self.score += 1
            reward = 10
            self.food.place(self.snake, self.enemy, self.WIDTH,self.HEIGHT)
            self.snake.nodes.append(Food(self.NODE_HEIGHT,self.NODE_WIDTH,self.YELLOW,[self.snake.position[0] + len(self.snake.nodes),self.snake.position[1]]))
            if self.score % 10 == 0:
                self.enemy.nodes.append(Food(self.NODE_HEIGHT,self.NODE_WIDTH,self.ORANGE,[self.snake.position[0] + len(self.snake.nodes),self.snake.position[1]]))
        
        # update ui
        self.update(self.objects,self.WIDTH,self.HEIGHT,self.NODE_WIDTH,self.NODE_HEIGHT,self.window,self.BLACK,self.BLACK)
        if self.fps == 20 or self.fps == 5:
            self.clock.tick(self.fps)
        return reward, game_over, self.score


def heuristic(position_1, position_2):
    return [position_2[0], position_2[1], abs((position_1[0]-position_2[0])**2 + (position_1[1]-position_2[1])**2)]
