from hooman import Hooman
import pygame
import terrain

screen_size = (800, 600)

hapi = Hooman(*screen_size)

class player:
    def __init__(self):
        self.w = 20
        self.h = 40
        self.x = screen_size[0]//2
        self.y = Map.get_ground_from_pixel(self.x).positon[1]
        self.surf = pygame.Surface((self.w, self.h)).convert()
        self.surf.fill((255, 0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.falling = False
    
    def blit(self):
        hapi.screen.blit(self.surf, (self.x, self.y))
        hapi.rect(self.rect.centerx - Map.offset, self.rect.centery, 5, 5)
    
    def check_for_collisions(self):
        """
        loop through a grid of 20x20 blocks around the player with the player being in the middle,
        do any collision testing and calculate light level for surounding blocks
        """
        self.rect.topleft = (self.x + Map.offset, self.y)
        index = Map.get_index_from_pixel((self.x, self.y))
        collided = False
        for x in range(-10, 11, 1):
            for y in range(-10, 11, 1):
                b = Map.get_block_from_index((index[0] + x, index[1] + y))
                # print((index[0] + x, index[1] + y))
                if b == None:
                    # print("None")
                    continue
                # calculate light level based on how far from player
                l = (abs(x)**2 + abs(y)**2)**(1/2)
                l = 20/(l*l) if l != 0 else l
                l = 0.2 if abs(x) > 9 or abs(y) > 9 else l
                b.light = min(max(l, 0.2), 1)
                b.draw()
                if y == 4 and abs(x) < 2: #check to see if standing on ground
                    collided = b.slope == 0
                    if b.slope == 0:
                        hapi.rect(b.rect.x - Map.offset, b.rect.y, 5, 5)
                        print(x, b.rect)
                if abs(x) < 2 or abs(y) < 3:
                    if b.slope == 0:
                        if self.rect.colliderect(b.rect):
                            self.rect.bottom = b.rect.top
                            self.y = self.rect.y
        self.falling = not collided
        print(self.falling, self.rect)

        if self.falling:
            self.y += Map.block_size

hapi.set_background((0, 0, 155))

Map = terrain.terrain((1000, 1000), hapi)
Map.generate()

Player = player()

clock = pygame.time.Clock()


while hapi.is_running:

    clock.tick(60)
    hapi.text(str(clock.get_fps()), 30, 30)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        Map.move(3)
    if keys[pygame.K_LEFT]:
        Map.move(-3)

    if pygame.mouse.get_pressed()[0]:
        print("Clicked on",Map.get_index_from_pixel(pygame.mouse.get_pos()))

    Map.blit()
    Player.check_for_collisions()
    Player.blit()
    hapi.flip_display()
    hapi.event_loop()
