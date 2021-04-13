import pygame
import random

# Global Vars
FLAT = 0
SLOPE_DOWN = -1
SLOPE_UP = 1

"""
Terrain class holds surface that gets blit to screen every frame, the camera does not move,
the background moves to make that effect, this also generates a random world by choosing a random direction
up, down or straight to determine the height of each column
"""
class terrain:
    def __init__(self, size, hapi):
        self.size = size
        self.block_size = 10
        self.surface = pygame.Surface(
            [x*self.block_size for x in self.size], pygame.SRCALPHA).convert_alpha()
        self.blocks = []
        self.hapi = hapi
        self.offset = self.size[0] // 2 * self.block_size

    # move the background by an amount = change, line 23 stops the background moving off screen   
    def move(self, change):
        self.offset += change
        self.offset = max(min(self.offset, self.size[1]*self.block_size), 0)

    def blit(self):
        self.hapi.screen.blit(self.surface, (-self.offset, 0))

    def generate(self):
        offset = 0
        last_rnd = 0
        for x in range(self.size[0]):
            x_pos = x*self.block_size
            y_pos = 400 + offset*self.block_size
            rnd = random.randint(-1, 1)
            offset += rnd
            # pygame.draw.rect(self.surface, (40, 255, 40), (x_pos, y_pos, self.block_size, self.block_size*2))
            # pygame.draw.rect(self.surface, (139, 69, 19),
            #                  (x_pos, y_pos + self.block_size*2, self.block_size, self.size[1] - y_pos - self.block_size*2))
            temp = []
            for y in range(0, self.size[1], self.block_size):
                if y >= y_pos:
                    if y < y_pos + 2*self.block_size:
                        name = "grass"
                        col = (40, 255, 40)
                    elif y < y_pos + 8*self.block_size:
                        name = "dirt"
                        col = (139, 69, 19)
                    else:
                        name = "stone"
                        col = (128, 128, 128)
                    b = block(name, col, (x_pos, y), 0, self.surface)
                    b.draw()
                    temp.append(b)
                elif y == y_pos - self.block_size:
                    if rnd == -1 and last_rnd == 1:
                        b = block("grass", (40, 255, 40),
                                  (x_pos, y), 0, self.surface)
                        b.draw()
                        temp.append(b)
                    elif rnd == -1:
                        b = block("grass", (40, 255, 40),
                            (x_pos, y), 1, self.surface)
                        b.draw()
                        temp.append(b)
                    elif last_rnd == 1:
                        b = block("grass", (40, 255, 40), (x_pos, y), -1, self.surface)
                        b.draw()
                        temp.append(b)
                    else:
                        temp.append(None)
                else:
                    temp.append(None)

            last_rnd = rnd
            self.blocks.append(temp)
        
    
    def get_block_from_index(self, index):
        return self.blocks[index[0]][index[1]]
    
    def get_block_from_pixel(self, pixel):
        x, y = self.get_index_from_pixel(pixel)
        return self.blocks[x][y]
    
    def get_index_from_pixel(self, pixel):
        return ((pixel[0] + self.offset) // self.block_size, pixel[1] // self.block_size)

    def get_ground_from_pixel(self, x):
        x = (x + self.offset) // self.block_size
        block = self.get_block_from_index((x, 0))
        y = 1
        while block is None:
            block = self.get_block_from_index((x, y))
            y += 1
        return block


class block:

    block_size = 10

    def __init__(self, name, color, positon, slope, surf):
        self.name = name
        self.color = color
        self.light = 0.2
        self.surf = surf
        self.slope = slope
        self.positon = positon
        if self.slope == FLAT:
            self.rect = pygame.Rect(*positon, self.block_size, self.block_size)
        else:
            self.rect = [
                (positon[0], positon[1] + self.block_size),
                (positon[0] + self.block_size, positon[1] + self.block_size),
                (positon[0] + self.block_size//2 + (self.block_size//2 * self.slope), positon[1])
                ]

    def draw(self):
        color = [x * self.light for x in self.color]
        if self.slope == FLAT:
            pygame.draw.rect(self.surf, color, self.rect)
        else:
            pygame.draw.polygon(self.surf, color, self.rect)
