import pygame
import random
import sys

# Constants
RES = 5
DIMS = (200, 200)
SCREEN = (RES * DIMS[0], RES * DIMS[1])
clock=pygame.time.Clock()


display = pygame.display.set_mode(SCREEN)


# Direction vectors: Right, Down, Left, Up
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Tile:
    def __init__(self, c, r):
        self.c = c
        self.r = r
        self.x = self.c * RES
        self.y = self.r * RES
        self.rect = pygame.Rect(self.x, self.y, RES, RES)
        self.state = 0  # 0 = white, 1 = black
        self.pheromone = None  # Track pheromone type ('A' or 'B')
    
    def draw(self):
        color = "black" if self.state else "white"
        pygame.draw.rect(display, color, self.rect)

grid = [[Tile(c, r) for c in range(DIMS[0])] for r in range(DIMS[1])]

class Ant:
    def __init__(self, id):
        self.r = random.randint(0, DIMS[1] - 1)
        self.c = random.randint(0, DIMS[0] - 1)
        #self.c=DIMS[0]//2
        #self.r=DIMS[1]//2
        self.direction_index = 0  # Start facing right
        self.id = id
        self.pheromone = 'A' if id == 1 else 'B'
    
    def move(self):
        tile = grid[self.r][self.c]
        if tile.pheromone == self.pheromone:
            if random.random() < 0.8:
                dx, dy = directions[self.direction_index]
            else:
                self.direction_index = (self.direction_index + 1) % 4 if tile.state == 0 else (self.direction_index - 1) % 4
                dx, dy = directions[self.direction_index]
        elif tile.pheromone is not None:
            if random.random() < 0.2:
                dx, dy = directions[self.direction_index]
            else:
                self.direction_index = (self.direction_index + 1) % 4 if tile.state == 0 else (self.direction_index - 1) % 4
                dx, dy = directions[self.direction_index]
        else:
            self.direction_index = (self.direction_index + 1) % 4 if tile.state == 0 else (self.direction_index - 1) % 4
            dx, dy = directions[self.direction_index]
        
        tile.state = 1 - tile.state  # Flip state
        tile.pheromone = self.pheromone  # Leave pheromone
        
        self.c = (self.c + dx) % DIMS[0]
        self.r = (self.r + dy) % DIMS[1]

ants = [Ant(1), Ant(2)]

def draw():
    display.fill("white")  # Background color
    for row in grid:
        for tile in row:
            tile.draw()
    pygame.display.flip()

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for ant in ants:
        ant.move()

while True:
    draw()
    update()
    clock.tick(100)
