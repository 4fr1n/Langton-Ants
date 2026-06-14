import pygame
import random
import sys
import numpy as np


RES = 5
DIMS = (200, 200)
SCREEN = (RES * DIMS[0], RES * DIMS[1])
clock = pygame.time.Clock()

display = pygame.display.set_mode(SCREEN)


directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Tile:
    def __init__(self, c, r):
        self.c = c
        self.r = r
        self.x = self.c * RES
        self.y = self.r * RES
        self.rect = pygame.Rect(self.x, self.y, RES, RES)
        self.state = 0  
    
    def draw(self):
        color = "black" if self.state else "white"
        pygame.draw.rect(display, color, self.rect)

grid = [[Tile(c, r) for c in range(DIMS[0])] for r in range(DIMS[1])]

class QLearningAnt:
    def __init__(self):
        self.r = DIMS[1] // 2
        self.c = DIMS[0] // 2
        
        # RL Hyperparameters
        self.alpha = 0.1    # Learning rate
        self.gamma = 0.9    # Discount factor
        self.epsilon = 0.1  # Exploration rate
        
        # Q-Table: 2 states (White=0, Black=1) x 4 actions (Directions)
        self.q_table = np.zeros((2, 4))
        
    def choose_action(self, state):
        
        if random.random() < self.epsilon:
            return random.randint(0, 3)  
        else:
            return np.argmax(self.q_table[state])  
            
    def move(self):
        
        current_tile = grid[self.r][self.c]
        state = current_tile.state
        
        
        action = self.choose_action(state)
        dx, dy = directions[action]
        
        
        if current_tile.state == 0:
            reward = 1.0
            current_tile.state = 1
        else:
            reward = -0.1
            current_tile.state = 0 
            
        
        self.c = (self.c + dx) % DIMS[0]
        self.r = (self.r + dy) % DIMS[1]
        
        next_tile = grid[self.r][self.c]
        next_state = next_tile.state
        
        
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state])
        
        
        self.q_table[state, action] = old_value + self.alpha * (reward + self.gamma * next_max - old_value)


ant = QLearningAnt()

def draw():
    display.fill("white")  
    for row in grid:
        for tile in row:
            tile.draw()
    
    
    agent_rect = pygame.Rect(ant.c * RES, ant.r * RES, RES, RES)
    pygame.draw.rect(display, "red", agent_rect)
    
    pygame.display.flip()

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            print("\nFinal Q-Table:")
            print("Action order: [Right, Down, Left, Up]")
            print(f"State 0 (White): {ant.q_table[0]}")
            print(f"State 1 (Black): {ant.q_table[1]}")
            pygame.quit()
            sys.exit()
            
    ant.move()

while True:
    draw()
    update()
    clock.tick(120) 
