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

            """if self.position[0]+self.width == 0:
                self.position[0] = WIDTH
            elif self.position[0] == WIDTH:
                self.position[0] = 0
            elif self.position[1]+self.height == 0:
                self.position[1] = HEIGHT
            elif self.position[1] == HEIGHT:
                self.position[1] = 0"""
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

            """if self.position[0]+self.width == 0:
                self.position[0] = WIDTH
            elif self.position[0] == WIDTH:
                self.position[0] = 0
            elif self.position[1]+self.height == 0:
                self.position[1] = HEIGHT
            elif self.position[1] == HEIGHT:
                self.position[1] = 0"""
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

            """if self.position[0]+self.width == 0:
                self.position[0] = WIDTH
            elif self.position[0] == WIDTH:
                self.position[0] = 0
            elif self.position[1]+self.height == 0:
                self.position[1] = HEIGHT
            elif self.position[1] == HEIGHT:
                self.position[1] = 0"""
    
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

            min_distance = head.position

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
        self.LEFT_UP = [-1,-1]
        self.LEFT_DOWN = [-1,1]
        self.RIGHT_UP = [1,-1]
        self.RIGHT_DOWN = [1,1]
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

    def collision(self, get_danger = False, danger_dir = [0,0], k = 0):
        # snake and enemy
        snake = self.snake
        enemy = self.enemy
        # positions
        snake_pos = snake.position
        enemy_pos = enemy.position
        # directions
        snake_dir = snake.direction
        enemy_dir = enemy.direction


        if get_danger:
            if danger_dir == snake_dir:   # STRAIGHT
                if snake_dir == self.UP:  # Snake going UP
                    min_x = snake_pos[0]
                    max_x = snake_pos[0] + snake.width
                    min_y = snake_pos[1] - (k)*snake.height
                    max_y = snake_pos[1]

                    # check if snake head is on edge
                    if min_y == 0 or max_y == 0:    
                        return True
                    # check if body is in front
                    for tail in snake.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == min_y:
                            return True
                    # check if enemy snake is in front
                    if (enemy_pos[0] >= min_x and enemy_pos[0] <= max_x) and enemy_pos[1] == min_y:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == min_y:
                            return True
                elif snake_dir == self.RIGHT:  # Snake going RIGHT
                    min_x = snake_pos[0] + snake.width
                    max_x = snake_pos[0] + (1+k)*snake.width
                    min_y = snake_pos[1] 
                    max_y = snake_pos[1] + snake.height

                    # check if snake head is on edge
                    if min_x == self.WIDTH or max_x == self.WIDTH:    
                        return True
                    # check if body is in front
                    for tail in snake.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == max_x:
                            return True
                    # check if enemy snake is in front
                    if (enemy_pos[1] >= min_y and enemy_pos[1] <= max_y) and enemy_pos[0] == max_x:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == max_x:
                            return True
                elif snake_dir == self.DOWN:  # Snake going DOWN
                    min_x = snake_pos[0]
                    max_x = snake_pos[0] + snake.width
                    min_y = snake_pos[1] + snake.height
                    max_y = snake_pos[1] + (1+k)*snake.height

                    # check if snake head is on edge
                    if min_y == self.HEIGHT or max_y == self.HEIGHT:    
                        return True
                    # check if body is in front
                    for tail in snake.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == max_y:
                            return True
                    # check if enemy snake is in front
                    if (enemy_pos[0] >= min_x and enemy_pos[0] <= max_x) and enemy_pos[1] == max_y:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == max_y:
                            return True
                elif snake_dir == self.LEFT:  # Snake going LEFT
                    min_x = snake_pos[0] - (k)*snake.width
                    max_x = snake_pos[0]
                    min_y = snake_pos[1] 
                    max_y = snake_pos[1] + snake.height

                    # check if snake head is on edge
                    if min_x == 0 or max_x == 0:    
                        return True
                    # check if body is in front
                    for tail in snake.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == min_x:
                            return True
                    # check if enemy snake is in front
                    if (enemy_pos[1] >= min_y and enemy_pos[1] <= max_y) and enemy_pos[0] == min_x:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == min_x:
                            return True
            elif (danger_dir == self.LEFT and snake_dir == self.DOWN) or (danger_dir == self.RIGHT and snake_dir == self.UP) or (danger_dir == self.UP and snake_dir == self.LEFT) or (danger_dir == self.DOWN and snake_dir == self.RIGHT):      # Right
                #######################
                #######################
                # DANGER IS ON THE RIGHT
                #######################
                #######################
                if danger_dir == self.LEFT and snake_dir == self.DOWN:  # Snake going DOWN
                    min_x = snake_pos[0] - (k)*snake.width
                    max_x = snake_pos[0]
                    min_y = snake_pos[1] - (k)*snake.height
                    max_y = snake_pos[1] + snake.height

                    # check if snake head is on edge
                    if min_x == 0 or max_x == 0:
                        return True
                    # check if body is in down
                    for tail in snake.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == min_x:
                            return True
                    # check if enemy snake is in down
                    if (enemy_pos[1] >= min_y and enemy_pos[1] <= max_y) and enemy_pos[0] == min_x:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == min_x:
                            return True
                elif danger_dir == self.RIGHT and snake_dir == self.UP: # Snake going UP
                    min_x = snake_pos[0] + snake.width
                    max_x = snake_pos[0] + (1+k)*snake.width
                    min_y = snake_pos[1]
                    max_y = snake_pos[1] - (k)*snake.height

                    # check if snake head is on edge
                    if min_x == self.WIDTH or max_x == self.WIDTH:
                        return True
                    # check if body is in up
                    for tail in snake.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == max_x:
                            return True
                    # check if enemy snake is in up
                    if (enemy_pos[1] >= min_y and enemy_pos[1] <= max_y) and enemy_pos[0] == max_x:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == max_x:
                            return True
                elif danger_dir == self.UP and snake_dir == self.LEFT:  # Snake going LEFT
                    min_x = snake_pos[0]
                    max_x = snake_pos[0] - (k)*snake.width
                    min_y = snake_pos[1]
                    max_y = snake_pos[1] - (k)*snake.height

                    # check if snake head is on edge
                    if min_y == 0 or max_y == 0:
                        return True
                    # check if body is in left
                    for tail in snake.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == min_y:
                            return True
                    # check if enemy snake is in left
                    if (enemy_pos[0] >= min_x and enemy_pos[0] <= max_x) and enemy_pos[1] == min_y:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == min_y:
                            return True
                elif danger_dir == self.DOWN and snake_dir == self.RIGHT:  # Snake going RIGHT
                    min_x = snake_pos[0] - (k)*snake.width
                    max_x = snake_pos[0] + snake.width
                    min_y = snake_pos[1] + snake.height
                    max_y = snake_pos[1] + (1+k)*snake.height

                    # check if snake head is on edge
                    if min_y == self.WIDTH or max_y == self.WIDTH:
                        return True
                    # check if body is in left
                    for tail in snake.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == max_y:
                            return True
                    # check if enemy snake is in left
                    if (enemy_pos[0] >= min_x and enemy_pos[0] <= max_x) and enemy_pos[1] == max_y:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == max_y:
                            return True
            elif (danger_dir == self.LEFT and snake_dir == self.UP) or (danger_dir == self.RIGHT and snake_dir == self.DOWN) or (danger_dir == self.UP and snake_dir == self.RIGHT) or (danger_dir == self.DOWN and snake_dir == self.LEFT):      # Left
                #######################
                #######################
                # DANGER IS ON THE LEFT
                #######################
                #######################
                if danger_dir == self.LEFT and snake_dir == self.UP:  # Snake going UP
                    min_x = snake_pos[0] - (k)*snake.width
                    max_x = snake_pos[0]
                    min_y = snake_pos[1] 
                    max_y = snake_pos[1] + (k)*snake.height

                    # check if snake head is on edge
                    if min_x == 0 or max_x == 0:
                        return True
                    # check if body is in down
                    for tail in snake.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == min_x:
                            return True
                    # check if enemy snake is in down
                    if (enemy_pos[1] >= min_y and enemy_pos[1] <= max_y) and enemy_pos[0] == min_x:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == min_x:
                            return True
                elif danger_dir == self.RIGHT and snake_dir == self.DOWN: # Snake going DOWN
                    min_x = snake_pos[0] + snake.width
                    max_x = snake_pos[0] + (1+k)*snake.width
                    min_y = snake_pos[1] - (k)*snake.height
                    max_y = snake_pos[1] + snake.height

                    # check if snake head is on edge
                    if min_x == self.WIDTH or max_x == self.WIDTH:
                        return True
                    # check if body is in up
                    for tail in snake.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == max_x:
                            return True
                    # check if enemy snake is in up
                    if (enemy_pos[1] >= min_y and enemy_pos[1] <= max_y) and enemy_pos[0] == max_x:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[1] >= min_y and tail.position[1] <= max_y) and tail.position[0] == max_x:
                            return True
                elif danger_dir == self.UP and snake_dir == self.RIGHT:  # Snake going RIGHT
                    min_x = snake_pos[0] - (k)*snake.width
                    max_x = snake_pos[0] + snake.width
                    min_y = snake_pos[1] - (k)*snake.height
                    max_y = snake_pos[1] 

                    # check if snake head is on edge
                    if min_y == 0 or max_y == 0:
                        return True
                    # check if body is in left
                    for tail in snake.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == min_y:
                            return True
                    # check if enemy snake is in left
                    if (enemy_pos[0] >= min_x and enemy_pos[0] <= max_x) and enemy_pos[1] == min_y:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == min_y:
                            return True
                elif danger_dir == self.DOWN and snake_dir == self.LEFT:  # Snake going LEFT
                    min_x = snake_pos[0] 
                    max_x = snake_pos[0] + (k)*snake.width
                    min_y = snake_pos[1] + snake.height
                    max_y = snake_pos[1] + (1+k)*snake.height

                    # check if snake head is on edge
                    if min_y == self.WIDTH or max_y == self.WIDTH:
                        return True
                    # check if body is in left
                    for tail in snake.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == max_y:
                            return True
                    # check if enemy snake is in left
                    if (enemy_pos[0] >= min_x and enemy_pos[0] <= max_x) and enemy_pos[1] == max_y:
                        return True
                    for tail in enemy.nodes:
                        if (tail.position[0] >= min_x and tail.position[0] <= max_x) and tail.position[1] == max_y:
                            return True
            elif (danger_dir == self.RIGHT_UP and snake_dir == self.UP) or (danger_dir == self.RIGHT_DOWN and snake_dir == self.RIGHT) or (danger_dir == self.LEFT_DOWN and snake_dir == self.DOWN) or (danger_dir == self.LEFT_UP and snake_dir == self.LEFT):  # Straight-Right
                #################################
                #################################
                # DANGER IS ON THE STRAIGHT-RIGHT
                #################################
                #################################
                if danger_dir == self.RIGHT_UP and snake_dir == self.UP: # Snake going UP
                    min_x = snake_pos[0] + snake.width
                    max_x = snake_pos[0] + (1+k)*snake.width
                    min_y = snake_pos[1] - (k)*snake.height
                    max_y = snake_pos[1]

                    # check if any body inside the area
                    for tail in snake.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                    # check if enemy inside the area
                    if min_x <= enemy_pos[0] <= max_x and min_y <= enemy_pos[1] <= max_y:
                        return True
                    for tail in enemy.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                elif danger_dir == self.RIGHT_DOWN and snake_dir == self.RIGHT: # Snake going RIGHT
                    min_x = snake_pos[0] + snake.width
                    max_x = snake_pos[0] + (1+k)*snake.width
                    min_y = snake_pos[1] + snake.height
                    max_y = snake_pos[1] + (1+k)*snake.height

                    # check if any body inside the area
                    for tail in snake.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                    # check if enemy inside the area
                    if min_x <= enemy_pos[0] <= max_x and min_y <= enemy_pos[1] <= max_y:
                        return True
                    for tail in enemy.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                elif danger_dir == self.LEFT_DOWN and snake_dir == self.DOWN: # Snake going DOWN
                    min_x = snake_pos[0]
                    max_x = snake_pos[0] - (k)*snake.width
                    min_y = snake_pos[1] + snake.height
                    max_y = snake_pos[1] + (1+k)*snake.height

                    # check if any body inside the area
                    for tail in snake.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                    # check if enemy inside the area
                    if min_x <= enemy_pos[0] <= max_x and min_y <= enemy_pos[1] <= max_y:
                        return True
                    for tail in enemy.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                elif danger_dir == self.LEFT_UP and snake_dir == self.LEFT: # Snake going LEFT
                    min_x = snake_pos[0] - (k)*snake.width
                    max_x = snake_pos[0]
                    min_y = snake_pos[1] - (k)*snake.height
                    max_y = snake_pos[1] 

                    # check if any body inside the area
                    for tail in snake.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                    # check if enemy inside the area
                    if min_x <= enemy_pos[0] <= max_x and min_y <= enemy_pos[1] <= max_y:
                        return True
                    for tail in enemy.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
            elif (danger_dir == self.LEFT_UP and snake_dir == self.UP) or (danger_dir == self.RIGHT_UP and snake_dir == self.RIGHT) or (danger_dir == self.RIGHT_DOWN and snake_dir == self.DOWN) or (danger_dir == self.LEFT_DOWN and snake_dir == self.LEFT):  # Straight-Left
                #################################
                #################################
                # DANGER IS ON THE STRAIGHT-LEFT
                #################################
                #################################
                if danger_dir == self.LEFT_UP and snake_dir == self.UP: # Snake going UP
                    min_x = snake_pos[0] - (k)*snake.width
                    max_x = snake_pos[0] 
                    min_y = snake_pos[1] - (k)*snake.height
                    max_y = snake_pos[1]

                    # check if any body inside the area
                    for tail in snake.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                    # check if enemy inside the area
                    if min_x <= enemy_pos[0] <= max_x and min_y <= enemy_pos[1] <= max_y:
                        return True
                    for tail in enemy.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                elif danger_dir == self.RIGHT_UP and snake_dir == self.RIGHT: # Snake going RIGHT
                    min_x = snake_pos[0] + snake.width
                    max_x = snake_pos[0] + (1+k)*snake.width
                    min_y = snake_pos[1] - (k)*snake.height
                    max_y = snake_pos[1] 


                    # check if any body inside the area
                    for tail in snake.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                    # check if enemy inside the area
                    if min_x <= enemy_pos[0] <= max_x and min_y <= enemy_pos[1] <= max_y:
                        return True
                    for tail in enemy.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                elif danger_dir == self.RIGHT_DOWN and snake_dir == self.DOWN: # Snake going DOWN
                    min_x = snake_pos[0] + snake.width
                    max_x = snake_pos[0] + (1+k)*snake.width
                    min_y = snake_pos[1] + snake.height
                    max_y = snake_pos[1] + (1+k)*snake.height

                    # check if any body inside the area
                    for tail in snake.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                    # check if enemy inside the area
                    if min_x <= enemy_pos[0] <= max_x and min_y <= enemy_pos[1] <= max_y:
                        return True
                    for tail in enemy.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                elif danger_dir == self.LEFT_DOWN and snake_dir == self.LEFT: # Snake going LEFT
                    min_x = snake_pos[0] - (k)*snake.width
                    max_x = snake_pos[0]
                    min_y = snake_pos[1] + snake.height
                    max_y = snake_pos[1] + (1+k)*snake.height

                    # check if any body inside the area
                    for tail in snake.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
                    # check if enemy inside the area
                    if min_x <= enemy_pos[0] <= max_x and min_y <= enemy_pos[1] <= max_y:
                        return True
                    for tail in enemy.nodes:
                        if min_x <= tail.position[0] <= max_x and min_y <= tail.position[1] <= max_y:
                            return True
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

            if snake_pos[0] + snake.width == 0:
                return True
            elif snake_pos[0] == self.WIDTH:
                return True
            elif snake_pos[1] + snake.height == 0:
                return True
            elif snake_pos[1] == self.HEIGHT:
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
