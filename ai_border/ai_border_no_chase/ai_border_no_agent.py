import torch
import random
import numpy as np
from collections import deque
from ai_border_no_game import SnakeGameAI
from ai_border_no_model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(13, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        head = game.snake
        c_n = 20
        
        dir_l = head.direction == [-1,0]
        dir_r = head.direction == [1,0]
        dir_u = head.direction == [0,-1]
        dir_d = head.direction == [0,1]
        
        # directions
        d_l = [-1,0]
        d_r = [1,0]
        d_u = [0,-1]
        d_d = [0,1]
        d_l_u = [-1,-1]
        d_l_d = [-1,1]
        d_r_u = [1,-1]
        d_r_d = [1,1]

        state = [
            # Danger straight
            (dir_r and game.collision(get_danger=True,danger_dir=d_r)) or 
            (dir_l and game.collision(get_danger=True,danger_dir=d_l)) or 
            (dir_u and game.collision(get_danger=True,danger_dir=d_u)) or 
            (dir_d and game.collision(get_danger=True,danger_dir=d_d)),

            # Danger right
            (dir_u and game.collision(get_danger=True,danger_dir=d_r)) or 
            (dir_d and game.collision(get_danger=True,danger_dir=d_l)) or 
            (dir_l and game.collision(get_danger=True,danger_dir=d_u)) or 
            (dir_r and game.collision(get_danger=True,danger_dir=d_d)),

            # Danger left
            (dir_d and game.collision(get_danger=True,danger_dir=d_r)) or 
            (dir_u and game.collision(get_danger=True,danger_dir=d_l)) or 
            (dir_r and game.collision(get_danger=True,danger_dir=d_u)) or 
            (dir_l and game.collision(get_danger=True,danger_dir=d_d)),

            # Danger straight-left
            (dir_r and game.collision(get_danger=True,danger_dir=d_r_u)) or 
            (dir_l and game.collision(get_danger=True,danger_dir=d_l_d)) or 
            (dir_u and game.collision(get_danger=True,danger_dir=d_l_u)) or 
            (dir_d and game.collision(get_danger=True,danger_dir=d_r_d)),

            # Danger straight-right
            (dir_r and game.collision(get_danger=True,danger_dir=d_r_d)) or 
            (dir_l and game.collision(get_danger=True,danger_dir=d_l_u)) or 
            (dir_u and game.collision(get_danger=True,danger_dir=d_r_u)) or 
            (dir_d and game.collision(get_danger=True,danger_dir=d_l_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            
            # Food left
            (dir_u and game.food.position[0] < head.position[0]) or 
            (dir_r and game.food.position[1] < head.position[1]) or 
            (dir_d and game.food.position[0] > head.position[0]) or
            (dir_l and game.food.position[1] > head.position[1]),  
            
            # Food right
            (dir_u and game.food.position[0] > head.position[0]) or
            (dir_r and game.food.position[1] > head.position[1]) or
            (dir_d and game.food.position[0] < head.position[0]) or
            (dir_l and game.food.position[1] < head.position[1]),

            # Food straight
            (dir_u and game.food.position[1] < head.position[1]) or 
            (dir_r and game.food.position[0] > head.position[0]) or
            (dir_d and game.food.position[1] > head.position[1]) or
            (dir_l and game.food.position[0] < head.position[0]),  

            # Food back
            (dir_u and game.food.position[1] > head.position[1]) or
            (dir_r and game.food.position[0] < head.position[0]) or
            (dir_d and game.food.position[1] < head.position[1]) or
            (dir_l and game.food.position[0] > head.position[0])
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.restart()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)


if __name__ == '__main__':
    train()