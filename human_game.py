import pygame
import random
import math

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

    def move(self, max_height, max_width):
        for i in range(0,len(self.nodes)):
            if i == len(self.nodes) - 1:
                self.nodes[len(self.nodes) - i - 1].position = [self.position[0],self.position[1]]
            else:
                self.nodes[len(self.nodes) - i - 1].position = [self.nodes[len(self.nodes) - i - 2].position[0],self.nodes[len(self.nodes) - i - 2].position[1]]
        self.position[0] += self.direction[0]*self.width
        self.position[1] += self.direction[1]*self.height

    
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

    def chase(self,head, max_height, max_width):
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


def heuristic(position_1, position_2):
    return [position_2[0], position_2[1], abs((position_1[0]-position_2[0])**2 + (position_1[1]-position_2[1])**2)]


def draw_grid(width, height, n_width, n_height, window, color):
    rows = height // n_height
    columns = width // n_width
    width_gap = n_width
    height_gap = n_height
    for i in range(int(columns)):
        pygame.draw.line(window, color, (i*width_gap,0), (i*width_gap, height))
        for j in range(int(rows)):
            pygame.draw.line(window, color, (0,j*height_gap), (width,j*height_gap))


def update(objects, width, height, n_width, n_height, window, color_lines, color_grid):
    # update grid and positions of objects
    window.fill(color_grid)
    for node in objects:
        node.draw(window)
    draw_grid(width, height, n_width, n_height, window, color_lines)
    pygame.display.update()


def main():
    # constants
    WIDTH = 800
    HEIGHT = 600
    NODE_HEIGHT = 20
    NODE_WIDTH = 20
    # colors
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    ORANGE = (255,165,0)
    YELLOW = (255,255,0)
    RED = (255,0,0)
    # init pygame
    pygame.init()
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    window.fill(BLACK)
    pygame.display.set_caption("Advanced Snake Game")
    # 0 = snake, 1 = enemy, 2 = food
    snake = Snake(NODE_HEIGHT, NODE_WIDTH, YELLOW, [int(WIDTH//NODE_WIDTH)//2,int(HEIGHT//NODE_HEIGHT)//2])
    food = Food(NODE_HEIGHT, NODE_WIDTH, RED, [random.randint(0,WIDTH//NODE_WIDTH - NODE_WIDTH),random.randint(0,HEIGHT//NODE_HEIGHT - NODE_HEIGHT)])
    enemy = Enemy(NODE_HEIGHT, NODE_WIDTH, ORANGE, [WIDTH//NODE_WIDTH-3,0])
    objects = [snake,enemy,food]
    clock = pygame.time.Clock()

    count = 0
    run = True
    while run:
        moved = False
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    # move player
                    objects[0].change_direction([0,-1])
                    objects[0].move(HEIGHT,WIDTH)
                    # chase player
                    enemy.chase(objects[0], HEIGHT, WIDTH)
                    # update
                    update(objects, WIDTH, HEIGHT, NODE_WIDTH, NODE_HEIGHT, window, BLACK, BLACK)
                    moved = True
                elif event.key == pygame.K_d:
                    # move player
                    objects[0].change_direction([1,0])
                    objects[0].move(HEIGHT,WIDTH)
                    # chase player
                    enemy.chase(objects[0], HEIGHT, WIDTH)
                    # update
                    update(objects, WIDTH, HEIGHT, NODE_WIDTH, NODE_HEIGHT, window, BLACK, BLACK)
                    moved = True
                elif event.key == pygame.K_s:
                    # move player
                    objects[0].change_direction([0,1])
                    objects[0].move(HEIGHT,WIDTH)
                    # chase player
                    enemy.chase(objects[0], HEIGHT, WIDTH)
                    # update
                    update(objects, WIDTH, HEIGHT, NODE_WIDTH, NODE_HEIGHT, window, BLACK, BLACK)
                    moved = True
                elif event.key == pygame.K_a:
                    # move player
                    objects[0].change_direction([-1,0])
                    objects[0].move(HEIGHT,WIDTH)
                    # chase player
                    enemy.chase(objects[0], HEIGHT, WIDTH)
                    # update
                    update(objects, WIDTH, HEIGHT, NODE_WIDTH, NODE_HEIGHT, window, BLACK, BLACK)
                    moved = True

                """if event.key == pygame.K_d:
                    # move player
                    if objects[0].direction == [1,0]:
                        objects[0].change_direction([0,1])
                    elif objects[0].direction == [0,1]:
                        objects[0].change_direction([-1,0])
                    elif objects[0].direction == [-1,0]:
                        objects[0].change_direction([0,-1])
                    elif objects[0].direction == [0,-1]:
                        objects[0].change_direction([1,0])
                    objects[0].move(HEIGHT,WIDTH)
                    # chase player
                    enemy.chase(objects[0], HEIGHT, WIDTH)
                    # update
                    update(objects, WIDTH, HEIGHT, NODE_WIDTH, NODE_HEIGHT, window, BLACK, BLACK)
                    moved = True
                elif event.key == pygame.K_a:
                    # move player
                    if objects[0].direction == [1,0]:
                        objects[0].change_direction([0,-1])
                    elif objects[0].direction == [0,-1]:
                        objects[0].change_direction([-1,0])
                    elif objects[0].direction == [-1,0]:
                        objects[0].change_direction([0,1])
                    elif objects[0].direction == [0,1]:
                        objects[0].change_direction([1,0])
                    objects[0].move(HEIGHT,WIDTH)
                    # chase player
                    enemy.chase(objects[0], HEIGHT, WIDTH)
                    # update
                    update(objects, WIDTH, HEIGHT, NODE_WIDTH, NODE_HEIGHT, window, BLACK, BLACK)
                    moved = True"""

        if not moved:
            # move player
            objects[0].move(HEIGHT,WIDTH)
            # chase player
            enemy.chase(objects[0], HEIGHT, WIDTH)
            # update
            update(objects, WIDTH, HEIGHT, NODE_WIDTH, NODE_HEIGHT, window, BLACK, BLACK)
        
        for tail in objects[0].nodes:
            if objects[0].position == tail.position or objects[1].position == tail.position or objects[1].position == objects[0].position:
                run = False
        if objects[0].position == objects[2].position:
            # add to player
            objects[0].nodes.append(Node(NODE_HEIGHT,NODE_WIDTH,YELLOW,[objects[0].position[0] + len(objects[0].nodes),objects[0].position[1]]))
            count += 1
            # add to bot
            if count % 3 == 0:
                objects[1].nodes.append(Node(NODE_HEIGHT,NODE_WIDTH,ORANGE,[objects[1].position[0] + len(objects[1].nodes),objects[1].position[1]]))
            # new food location
            objects[2].place(objects[0],objects[1],WIDTH,HEIGHT)

        if objects[0].position[0]+objects[0].width == 0:
            objects[0].position[0] = WIDTH
        elif objects[0].position[0] == WIDTH:
            objects[0].position[0] = 0
        elif objects[0].position[1]+objects[0].height == 0:
            objects[0].position[1] = HEIGHT
        elif objects[0].position[1] == HEIGHT:
            objects[0].position[1] = 0

        if objects[1].position[0]+objects[1].width == 0:
            objects[1].position[0] = WIDTH
        elif objects[1].position[0] == WIDTH:
            objects[1].position[0] = 0
        elif objects[1].position[1]+objects[1].height == 0:
            objects[1].position[1] = HEIGHT
        elif objects[1].position[1] == HEIGHT:
            objects[1].position[1] = 0
        
        #
        

if __name__ == "__main__":
    main()

"""
if self.position[0] - min_distance[0] < 0 and self.position[1] - min_distance[1] == 0:
            if abs(self.position[0]-min_distance[0]) > max_width // 2 :
                self.direction = [-1,0]
            else:
                self.direction = [1,0]
            self.position[0] += self.direction[0]*self.width
            self.position[1] += self.direction[1]*self.height
        elif self.position[0] - min_distance[0] > 0 and self.position[1] - min_distance[1] == 0:
            if abs(self.position[0]-min_distance[0]) > max_width // 2 :
                self.direction = [1,0]
            else:
                self.direction = [-1,0]
            self.position[0] += self.direction[0]*self.width
            self.position[1] += self.direction[1]*self.height
        elif self.position[0] - min_distance[0] == 0 and self.position[1] - min_distance[1] < 0:
            if abs(self.position[1]-min_distance[1]) > max_height // 2 :
                self.direction = [0,-1]
            else:
                self.direction = [0,1]
            self.position[0] += self.direction[0]*self.width
            self.position[1] += self.direction[1]*self.height
        elif self.position[0] - min_distance[0] == 0 and self.position[1] - min_distance[1] > 0:
            if abs(self.position[1]-min_distance[1]) > max_height // 2 :
                self.direction = [0,1]
            else:
                self.direction = [0,-1]
            self.position[0] += self.direction[0]*self.width
            self.position[1] += self.direction[1]*self.height
            ###################################################################################
        elif self.position[0] - min_distance[0] < 0 and self.position[1] - min_distance[1] > 0:
            if abs(min_distance[0] - self.position[0]) < abs(min_distance[1] - self.position[1]):
                if abs(self.position[0]-min_distance[0]) > max_width // 2 :
                    self.direction = [-1,0]
                else:
                    self.direction = [1,0]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
            else:
                if abs(self.position[1]-min_distance[1]) > max_height // 2 :
                    self.direction = [0,1]
                else:
                    self.direction = [0,-1]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
        elif self.position[0] - min_distance[0] < 0 and self.position[1] - min_distance[1] < 0:
            if abs(min_distance[0] - self.position[0]) < abs(min_distance[1] - self.position[1]):
                if abs(self.position[0]-min_distance[0]) > max_width // 2 :
                    self.direction = [-1,0]
                else:
                    self.direction = [1,0]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
            else:
                if abs(self.position[1]-min_distance[1]) > max_height // 2 :
                    self.direction = [0,-1]
                else:
                    self.direction = [0,1]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
        elif self.position[0] - min_distance[0] > 0 and self.position[1] - min_distance[1] < 0:
            if abs(min_distance[0] - self.position[0]) < abs(min_distance[1] - self.position[1]):
                if abs(self.position[0]-min_distance[0]) > max_width // 2 :
                    self.direction = [1,0]
                else:
                    self.direction = [-1,0]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
            else:
                if abs(self.position[1]-min_distance[1]) > max_height // 2 :
                    self.direction = [0,-1]
                else:
                    self.direction = [0,1]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
        elif self.position[0] - min_distance[0] > 0 and self.position[1] - min_distance[1] > 0:
            if abs(min_distance[0] - self.position[0]) < abs(min_distance[1] - self.position[1]):
                if abs(self.position[0]-min_distance[0]) > max_width // 2 :
                    self.direction = [1,0]
                else:
                    self.direction = [-1,0]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
            else:
                if abs(self.position[1]-min_distance[1]) > max_height // 2 :
                    self.direction = [0,1]
                else:
                    self.direction = [0,-1]
                self.position[0] += self.direction[0]*self.width
                self.position[1] += self.direction[1]*self.height
"""