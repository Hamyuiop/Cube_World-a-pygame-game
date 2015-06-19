#! /usr/bin/python

import pygame
import time
from pygame import *

WIN_WIDTH = 1000
WIN_HEIGHT = 720
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
grey = (150,150,150)
dark_grey = (50,50,50)

grass = pygame.image.load("grass_texture.png")
dirt = pygame.image.load("dirt_tecture.png")
w1_bg = pygame.image.load("world_1 bg texture.png")
sprite_1 = pygame.image.load("sprite_1.png")
flower = pygame.image.load('flower.png')
intro_pic = pygame.image.load('game_artwork.png')
intro_pic = pygame.transform.scale(intro_pic,(1000,720))
opic = pygame.image.load('background.png')
opic = pygame.transform.scale(opic,(1000,720))

pygame.init()
screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.display.set_caption("Cube_World 1.5")
time = pygame.time.Clock()
time.tick(60)

def main_menu():
    level = 0
    end_it=False
    while (end_it==False):
        screen.blit(intro_pic,(0,0))
        myfont=pygame.font.SysFont("Britannic Bold", 100)
        nlabel=myfont.render("Welcome To Cube World", 1, (100,150,175))
        blabel=myfont.render("Click to play!", 1, (100,150,175))
        for event in pygame.event.get():
            if event.type==MOUSEBUTTONDOWN:
                end_it=True
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                quit()
        screen.blit(nlabel,(85,500))
        screen.blit(blabel,(275,600))
        pygame.display.flip()

def world_1_lvl_1():
    level = 1
    class Player(Entity):
        def __init__(self, x, y):
            Entity.__init__(self)
            self.xvel = 0
            self.yvel = 0
            self.onGround = False
            self.image = Surface((32,32))
            self.image.blit(sprite_1,(0,0))
            self.image.convert()
            self.rect = Rect(x, y, 32, 32)

        def update(self, up, down, left, right, fast_left, fast_right, running, platforms):
            if up:
                # only jump if on the ground
                if self.onGround: self.yvel -= 10
            if down:
                pass
            if running:
                self.xvel = 12
            if left:
                self.xvel = -8
            if right:
                self.xvel = 8
            if fast_left:
                self.xvel = -12
            if fast_right:
                self.xvel = 12
            if not self.onGround:
                # only accelerate with gravity if in the air
                self.yvel += 0.3
                if down:
                    self.yvel += 0.3
                # max falling speed
                if self.yvel > 30:
                    world_1_lvl_2()
                    num = 2
                    pygame.display.update()
            if not(left or right or fast_left or fast_right):
                self.xvel = 0
            # increment in x direction
            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0, platforms)
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False;
            # do y-axis collisions
            self.collide(0, self.yvel, platforms)
    global cameraX, cameraY

    up = down = left = right = running = fast_left = fast_right = False
    bg = Surface((32,32))
    bg.convert()
    bg.blit(w1_bg,(0,0))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []
    x = y = 0
    num = 1
    if num == 1:
        level = [
            "P PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                               ",
            "EPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "C":
                c = Checkpoint(x, y)
                platforms.append(c)
                entities.add(c)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    while 1:
        time.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_DOWN or e.type == KEYDOWN and e.key == K_s:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT or e.type == KEYDOWN and e.key == K_d:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_UP or e.type == KEYDOWN and e.key == K_w:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT and e.type == KEYDOWN and e.key == K_s:
                fast_left = True
            if e.type == KEYDOWN and e.key == K_RIGHT and e.type == KEYDOWN and e.key == K_s:
                fast_right = True
            if e.type == KEYDOWN and e.key == K_r:
                level = 1
                world_1_lvl_1()
            if e.type == KEYDOWN and e.key == K_p:
                pause_menu()
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
                fast_right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
                fast_left = False
            if e.type == KEYUP and e.key == K_w:
                up = False
            if e.type == KEYUP and e.key == K_s:
                down = False
            if e.type == KEYUP and e.key == K_d:
                right = False
                fast_right = False
            if e.type == KEYUP and e.key == K_a:
                left = False
                fast_left = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, fast_left, fast_right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

def world_1_lvl_2():
    level = 2
    class Player(Entity):
        def __init__(self, x, y):
            Entity.__init__(self)
            self.xvel = 0
            self.yvel = 0
            self.onGround = False
            self.image = Surface((32,32))
            self.image.blit(sprite_1,(0,0))
            self.image.convert()
            self.rect = Rect(x, y, 32, 32)

        def update(self, up, down, left, right, fast_left, fast_right, running, platforms):
            if up:
                # only jump if on the ground
                if self.onGround: self.yvel -= 10
            if down:
                pass
            if running:
                self.xvel = 12
            if left:
                self.xvel = -8
            if right:
                self.xvel = 8
            if fast_left:
                self.xvel = -12
            if fast_right:
                self.xvel = 12
            if not self.onGround:
                # only accelerate with gravity if in the air
                self.yvel += 0.3
                if down:
                    self.yvel += 0.3
                # max falling speed
                if self.yvel > 30:
                    world_1_lvl_3()
                    num = 2
                    pygame.display.update()
            if not(left or right or fast_left or fast_right):
                self.xvel = 0
            # increment in x direction
            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0, platforms)
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False;
            # do y-axis collisions
            self.collide(0, self.yvel, platforms)
    global cameraX, cameraY

    up = down = left = right = running = fast_left = fast_right = False
    bg = Surface((32,32))
    bg.convert()
    bg.blit(w1_bg,(0,0))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []
    x = y = 0
    num = 1
    if num == 1:
        level = [
            "P PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                               ",
            "E                              P",
            "E                              E",
            "E                      PPPP    E",
            "E                              E",
            "E                              E",
            "E           PPPPPPP            E",
            "E                              E",
            "E                              E",
            "EPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "C":
                c = Checkpoint(x, y)
                platforms.append(c)
                entities.add(c)
            if col == "A":
                a = Enemy(x, y)
                platforms.append(c)
                entities.add(c)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    while 1:
        time.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_a:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_p:
                pause_menu()
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT and e.type == KEYDOWN and e.key == K_s:
                fast_left = True
            if e.type == KEYDOWN and e.key == K_RIGHT and e.type == KEYDOWN and e.key == K_s:
                fast_right = True
            if e.type == KEYDOWN and e.key == K_r:
                level = 1
                world_1_lvl_1()
            if e.type == KEYUP and e.key == K_a:
                up = False
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_s:
                fast_left = False
                fast_right = False
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
                fast_right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
                fast_left = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, fast_left, fast_right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

def world_1_lvl_3():
    level = 3
    class Player(Entity):
        def __init__(self, x, y):
            Entity.__init__(self)
            self.xvel = 0
            self.yvel = 0
            self.onGround = False
            self.image = Surface((32,32))
            self.image.blit(sprite_1,(0,0))
            self.image.convert()
            self.rect = Rect(x, y, 32, 32)

        def update(self, up, down, left, right, fast_left, fast_right, running, platforms):
            if up:
                # only jump if on the ground
                if self.onGround: self.yvel -= 10
            if down:
                pass
            if running:
                self.xvel = 12
            if left:
                self.xvel = -8
            if right:
                self.xvel = 8
            if fast_left:
                self.xvel = -12
            if fast_right:
                self.xvel = 12
            if not self.onGround:
                # only accelerate with gravity if in the air
                self.yvel += 0.3
                if down:
                    self.yvel += 0.3
                # max falling speed
                if self.yvel > 30:
                    world_1_lvl_4()
                    num = 2
                    pygame.display.update()
            if not(left or right or fast_left or fast_right):
                self.xvel = 0
            # increment in x direction
            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0, platforms)
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False;
            # do y-axis collisions
            self.collide(0, self.yvel, platforms)
    global cameraX, cameraY

    up = down = left = right = running = fast_left = fast_right = False
    bg = Surface((32,32))
    bg.convert()
    bg.blit(w1_bg,(0,0))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []
    x = y = 0
    num = 1
    if num == 1:
        level = [
            "P PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            "E                               ",
            "E                     PPPP     E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                             PE",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                    PPPPPP    E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                              E",
            "E                      PPPP    E",
            "E                              E",
            "E                              E",
            "E           PPPPPPP            E",
            "E                              E",
            "E                              E",
            "EPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "C":
                c = Checkpoint(x, y)
                platforms.append(c)
                entities.add(c)
            if col == "A":
                a = Enemy(x, y)
                platforms.append(c)
                entities.add(c)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    while 1:
        time.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_a:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_p:
                pause_menu()
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT and e.type == KEYDOWN and e.key == K_s:
                fast_left = True
            if e.type == KEYDOWN and e.key == K_RIGHT and e.type == KEYDOWN and e.key == K_s:
                fast_right = True
            if e.type == KEYDOWN and e.key == K_r:
                level = 1
                world_1_lvl_1()
            if e.type == KEYUP and e.key == K_a:
                up = False
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_s:
                fast_left = False
                fast_right = False
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
                fast_right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
                fast_left = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, fast_left, fast_right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

def world_1_lvl_4():
    level = 4
    class Player(Entity):
        def __init__(self, x, y):
            Entity.__init__(self)
            self.xvel = 0
            self.yvel = 0
            self.onGround = False
            self.image = Surface((32,32))
            self.image.blit(sprite_1,(0,0))
            self.image.convert()
            self.rect = Rect(x, y, 32, 32)

        def update(self, up, down, left, right, fast_left, fast_right, running, platforms):
            if up:
                # only jump if on the ground
                if self.onGround: self.yvel -= 10
            if down:
                pass
            if running:
                self.xvel = 12
            if left:
                self.xvel = -8
            if right:
                self.xvel = 8
            if fast_left:
                self.xvel = -12
            if fast_right:
                self.xvel = 12
            if not self.onGround:
                # only accelerate with gravity if in the air
                self.yvel += 0.3
                if down:
                    self.yvel += 0.3
                # max falling speed
                if self.yvel > 30:
                    world_1_lvl_5()
                    num = 2
                    pygame.display.update()
            if not(left or right or fast_left or fast_right):
                self.xvel = 0
            # increment in x direction
            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0, platforms)
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False;
            # do y-axis collisions
            self.collide(0, self.yvel, platforms)
    global cameraX, cameraY

    up = down = left = right = running = fast_left = fast_right = False
    bg = Surface((32,32))
    bg.convert()
    bg.blit(w1_bg,(0,0))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []
    x = y = 0
    num = 1
    if num == 1:
        level = [
            "P PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            "E                                           ",
            "E                                          E",
            "E                                          E",
            "E                                       P  E",
            "E                                          E",
            "E                                          E",
            "E                                          E",
            "E                                          E",
            "E                          PP              E",
            "E                           E              E",
            "E                     PPPPP E              E",
            "E                     E     E              E",
            "E                     E     E              E",
            "E                     EPPPP E              E",
            "E                     E     E              E",
            "E                     EPPPP E              E",
            "E          PPPPPP     E     E              E",
            "E          E    E     E PPPPE              E",
            "E   PPPP   E    E     E     E              E",
            "E   E  E   E    E     E     E              E",
            "E   E  E   E    E           E              E",
            "EPPPEPPEPPPEPPPPEPPPPPPPPPPPEPPPPPPPPPPPPPPP",]
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "C":
                c = Checkpoint(x, y)
                platforms.append(c)
                entities.add(c)
            if col == "A":
                a = Enemy(x, y)
                platforms.append(c)
                entities.add(c)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    while 1:
        time.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_a:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_r:
                level = 1
                world_1_lvl_1()
            if e.type == KEYDOWN and e.key == K_p:
                pause_menu()
            if e.type == KEYUP and e.key == K_a:
                up = False
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_s:
                fast_left = False
                fast_right = False
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
                fast_right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
                fast_left = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, fast_left, fast_right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

def world_1_lvl_5():
    level = 5
    class Player(Entity):
        def __init__(self, x, y):
            Entity.__init__(self)
            self.xvel = 0
            self.yvel = 0
            self.onGround = False
            self.image = Surface((32,32))
            self.image.blit(sprite_1,(0,0))
            self.image.convert()
            self.rect = Rect(x, y, 32, 32)

        def update(self, up, down, left, right, fast_left, fast_right, running, platforms):
            if up:
                # only jump if on the ground
                if self.onGround: self.yvel -= 10
            if down:
                pass
            if running:
                self.xvel = 12
            if left:
                self.xvel = -8
            if right:
                self.xvel = 8
            if fast_left:
                self.xvel = -12
            if fast_right:
                self.xvel = 12
            if not self.onGround:
                # only accelerate with gravity if in the air
                self.yvel += 0.3
                if down:
                    self.yvel += 0.3
                # max falling speed
                if self.yvel > 30:
                    world_1_lvl_6()
                    num = 2
                    pygame.display.update()
            if not(left or right or fast_left or fast_right):
                self.xvel = 0
            # increment in x direction
            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0, platforms)
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False;
            # do y-axis collisions
            self.collide(0, self.yvel, platforms)
    global cameraX, cameraY

    up = down = left = right = running = fast_left = fast_right = False
    bg = Surface((32,32))
    bg.convert()
    bg.blit(w1_bg,(0,0))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []
    x = y = 0
    num = 1
    if num == 1:
        level = [
            "P PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP PPPPPPPP",
            "E   E                                      E",
            "E   E                        PPPP          E",
            "E   E                                      E",
            "E   E            PPPPPPPP                  E",
            "E   E                                      E",
            "E   E         PPP                          E",
            "E   E                                      E",
            "E   E                            PPPP      E",
            "E   E              PPPPPPPP                E",
            "E   E                                     PE",
            "E   E                                      E",
            "E   E                                      E",
            "E   E                                     PE",
            "E   E                                      E",
            "E   E                                      E",
            "E   E                                      E",
            "E   E                                     PE",
            "E   E                                      E",
            "E   E                                      E",
            "E   E                              PPPP    E",
            "E                                          E",
            "EPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "C":
                c = Checkpoint(x, y)
                platforms.append(c)
                entities.add(c)
            if col == "A":
                a = Enemy(x, y)
                platforms.append(c)
                entities.add(c)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    while 1:
        time.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_a:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT and e.type == KEYDOWN and e.key == K_s:
                fast_left = True
            if e.type == KEYDOWN and e.key == K_RIGHT and e.type == KEYDOWN and e.key == K_s:
                fast_right = True
            if e.type == KEYDOWN and e.key == K_r:
                level = 5
                world_1_lvl_5()
            if e.type == KEYUP and e.key == K_a:
                up = False
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_s:
                fast_left = False
                fast_right = False
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
                fast_right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
                fast_left = False
            if e.type == KEYDOWN and e.key == K_p:
                pause_menu()

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, fast_left, fast_right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

def world_1_lvl_6():
    level = 6
    class Player(Entity):
        def __init__(self, x, y):
            Entity.__init__(self)
            self.xvel = 0
            self.yvel = 0
            self.onGround = False
            self.image = Surface((32,32))
            self.image.blit(sprite_1,(0,0))
            self.image.convert()
            self.rect = Rect(x, y, 32, 32)

        def update(self, up, down, left, right, fast_left, fast_right, running, platforms):
            if up:
                # only jump if on the ground
                if self.onGround: self.yvel -= 10
            if down:
                pass
            if running:
                self.xvel = 12
            if left:
                self.xvel = -8
            if right:
                self.xvel = 8
            if fast_left:
                self.xvel = -12
            if fast_right:
                self.xvel = 12
            if not self.onGround:
                # only accelerate with gravity if in the air
                self.yvel += 0.3
                if down:
                    self.yvel += 0.3
                # max falling speed
                if self.yvel > 30:
                    world_1_lvl_6()
                    num = 2
                    pygame.display.update()
            if not(left or right or fast_left or fast_right):
                self.xvel = 0
            # increment in x direction
            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0, platforms)
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False;
            # do y-axis collisions
            self.collide(0, self.yvel, platforms)
    global cameraX, cameraY

    up = down = left = right = running = fast_left = fast_right = False
    bg = Surface((32,32))
    bg.convert()
    bg.blit(w1_bg,(0,0))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []
    x = y = 0
    num = 1
    if num == 1:
        level = [
            "P PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            "E    E                                                     E",
            "EPPP E      PPP  P  P   P PP   PPPPPPP  PPPP   PPPP P  P P E",
            "E    E      E                                            E E",
            "E    E PPPPPE                                            E E",
            "E PPPE      E                                            E E",
            "E    E      E                                            E E",
            "EPP PEPP PPPE                                            E E",
            "E    E      E                                            E E",
            "E    E      E                                            E E",
            "E    EPPPPP E                                            E E",
            "E PPPE      E                                            E E",
            "E      P    E                                            E E",
            "E      E    E                                            E E",
            "EPPPPPPEPPPPE                                      PPPPPPE E",
            "E                                                  E       E",
            "E                                                  E  PPPPPE",
            "E                                      PPPPPPPPPPPPE  E    E",
            "E                                      E              E    E",
            "E                                      E    PPPPPPPPPPE    E",
            "E                                      E    E              E",
            "E                                      E                    ",
            "EPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPEPPPPPPPPPPPPPPPPPPPP",]
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "C":
                c = Checkpoint(x, y)
                platforms.append(c)
                entities.add(c)
            if col == "A":
                a = Enemy(x, y)
                platforms.append(c)
                entities.add(c)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    while 1:
        time.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_a:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_p:
                pause_menu()
            if e.type == KEYDOWN and e.key == K_LEFT and e.type == KEYDOWN and e.key == K_s:
                fast_left = True
            if e.type == KEYDOWN and e.key == K_RIGHT and e.type == KEYDOWN and e.key == K_s:
                fast_right = True
            if e.type == KEYDOWN and e.key == K_r:
                level = 5
                world_1_lvl_5()
            if e.type == KEYUP and e.key == K_a:
                up = False
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_s:
                fast_left = False
                fast_right = False
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
                fast_right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
                fast_left = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, fast_left, fast_right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

def world_1_lvl_10():
    level = 10
    class Player(Entity):
        def __init__(self, x, y):
            Entity.__init__(self)
            self.xvel = 0
            self.yvel = 0
            self.onGround = False
            self.image = Surface((32,32))
            self.image.blit(sprite_1,(0,0))
            self.image.convert()
            self.rect = Rect(x, y, 32, 32)

        def update(self, up, down, left, right, fast_left, fast_right, running, platforms):
            if up:
                # only jump if on the ground
                if self.onGround: self.yvel -= 10
            if down:
                pass
            if running:
                self.xvel = 12
            if left:
                self.xvel = -8
            if right:
                self.xvel = 8
            if fast_left:
                self.xvel = -12
            if fast_right:
                self.xvel = 12
            if not self.onGround:
                # only accelerate with gravity if in the air
                self.yvel += 0.3
                if down:
                    self.yvel += 0.3
                # max falling speed
                if self.yvel > 30:
                    world_2_lvl_1()
                    num = 2
                    pygame.display.update()
            if not(left or right or fast_left or fast_right):
                self.xvel = 0
            # increment in x direction
            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0, platforms)
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False;
            # do y-axis collisions
            self.collide(0, self.yvel, platforms)
    global cameraX, cameraY

    up = down = left = right = running = fast_left = fast_right = False
    bg = Surface((32,32))
    bg.convert()
    bg.blit(w1_bg,(0,0))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []
    x = y = 0
    num = 1
    if num == 1:
        level = [
            "P PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            "E   E                                                                          E",
            "E   E                                                                          E",
            "E   E                                      P                                   E",
            "E   E                PPPPPPPPPPP           E                                   E",
            "E   E                                      E                                   E",
            "E   E                                      E        PPPPPCCCCCCCCCCCCCCCCCCCC  E",
            "E   E         PP                           E            E  C        C          E",
            "E   EPPPPPPPP  E                           E            E     C       CCCCCCCC E",
            "E   E          E                           E            E  C  C     C        C E",
            "E   E          E                           EPPPPPPPP    E  C  C     C CCCCCC CCE",
            "E   E          EPPPPPPPPPPPPPPPPPP         E            E  C  C     C          E",
            "E   E                                      E     PPPPPPPE CCCCCCCCCCCCCCCCCCCCCE",
            "E   EPPPPPPPPPPPPP                         E            E                      E",
            "E                                          E            E                      E",
            "E                                          E            E                      E",
            "E                                          E            E                      E",
            "E   PPPPPPPPPPP                            EPPPPPP  PPPPE                      E",
            "E                                          E            E                      E",
            "E                 PPPPPPPPPPP              E            E                      E",
            "E                                          E            E                      E",
            "E                                          E            E                      E",
            "E                                          E            E                      E",
            "E                                          E            C                       ",
            "EPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPEPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "C":
                c = Checkpoint(x, y)
                platforms.append(c)
                entities.add(c)
            if col == "A":
                a = Enemy(x, y)
                platforms.append(c)
                entities.add(c)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    while 1:
        time.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                quit()
            if e.type == KEYDOWN and e.key == K_a:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_p:
                pause_menu()
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT and e.type == KEYDOWN and e.key == K_s:
                fast_left = True
            if e.type == KEYDOWN and e.key == K_RIGHT and e.type == KEYDOWN and e.key == K_s:
                fast_right = True
            if e.type == KEYDOWN and e.key == K_r:
                level = 5
                world_1_lvl_5()
            if e.type == KEYUP and e.key == K_a:
                up = False
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_s:
                fast_left = False
                fast_right = False
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
                fast_right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
                fast_left = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, fast_left, fast_right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()
        
def pause_menu():
    end_it=False
    while (end_it==False):
        screen.blit(opic,(0,0))
        myfont=pygame.font.SysFont("Britannic Bold", 100)
        nlabel=myfont.render("Paused", 1, (100,150,175))
        blabel=myfont.render("Click or press a key to play!", 1, (100,150,175))
        for event in pygame.event.get():
            if event.type==MOUSEBUTTONDOWN:
                end_it=True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                else:
                    end_it=True
        screen.blit(nlabel,(85,500))
        screen.blit(blabel,(275,600))
        pygame.display.flip()

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.blit(grass,(0,0))
        self.rect = Rect(x, y, 32, 32)
class Troll(Entity):
    def __init__(self, x, y):
        self.image = Surface
        self.image.fill(white)
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass
class Checkpoint(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = Surface([32, 32], pygame.SRCALPHA, 32)
    def update(self):
        pass
class Dirt(Entity):
    def _init_(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.blit(dirt,(0,0))
        self.rect = Rect(x, y, 32, 32)
class ExitBlock(Entity):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.blit(dirt,(0,0))
    def update(self):
        pass
class Flower(Entity):
    def _init_(self, x, y):
        Platform._init_(self, x, y)
        self.image.blit(flower,(0,0))
    def update(self):
        pass
        
main_menu()
world_1_lvl_1()
pygame.quit()
quit()
