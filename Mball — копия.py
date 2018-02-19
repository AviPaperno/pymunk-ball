"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. Not interactive.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys, random

first_stat = True

black = (0,0,0) 
pygame.init()
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 25)

### Physics stuff
space = pymunk.Space()
space.gravity = (0.0, -900.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

## Balls
balls = []

def create_ball(mass,radius = 25):
    global balls
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    x = random.randint(115,350)
    body.position = x, 400
    shape = pymunk.Circle(body, radius, (0,0))
    shape.elasticity = 0.95
    shape.friction = 0.9
    space.add(body, shape)
    balls.append(shape)

def draw_info():
        text = font.render("Описание ",True,black)
        screen.blit(text, [20,30])
        text = font.render("Увеличить гравитацию - u",True,black)
        screen.blit(text, [20,70])
        text = font.render("Уменьшить гравитацию - d",True,black)
        screen.blit(text, [20,90])
        text = font.render("Увеличить массу - m ",True,black)
        screen.blit(text, [20,110])
        text = font.render("Уменьшить массу - l",True,black)
        screen.blit(text, [20,130])
        text = font.render("Создать мяч - n",True,black)
        screen.blit(text, [20,50])

### walls
static_body = space.static_body
static_lines = [pymunk.Segment(static_body, (0.0, 50.0), (700.0, 50.0), 0.0),
                pymunk.Segment(static_body, (0.0, 0.0), (0.0, 700.0), 0.0),
                pymunk.Segment(static_body, (700.0, 0.0), (700.0, 700.0), 0.0),
                ]  
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 0.9
space.add(static_lines)


def update_pos():
    try:
        text = font.render("Координата "+ str(balls[0].body.position),True,black)
        screen.blit(text, [300,50])
        text = font.render("Масса "+ str(balls[0].body.mass),True,black)
        screen.blit(text, [300,70])
        text = font.render("Гравитация "+ str(space.gravity),True,black)
        screen.blit(text, [300,90])
        pygame.display.flip() 
    except:
        pass

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == KEYDOWN and event.key == K_p:
            pygame.image.save(screen, "bouncing_balls.png")
        elif event.type == KEYDOWN and event.key == K_n:
            for ball in balls:
                space.remove(ball, ball.body)
                balls.remove(ball)
            create_ball(10)
        elif event.type == KEYDOWN and event.key == K_u:
            tmp_gravity = (space.gravity[0],space.gravity[1]+100)
            space.gravity = tmp_gravity
        elif event.type == KEYDOWN and event.key == K_d:
            tmp_gravity = (space.gravity[0],space.gravity[1]-100)
            space.gravity = tmp_gravity
        elif event.type == KEYDOWN and event.key == K_m:
            balls[0].body.mass += 10
        elif event.type == KEYDOWN and event.key == K_l:
            balls[0].body.mass -= 10
     
    ### Clear screen
    screen.fill(THECOLORS["white"])
    draw_info()
    ### Draw stuff
    balls_to_remove = []

    for ball in balls_to_remove:
        space.remove(ball, ball.body)
        balls.remove(ball)

    space.debug_draw(draw_options)


    update_pos()
    
    ### Update physics
    dt = 1.0/60.0
    for x in range(1):
        space.step(dt)
    
    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("Моделирование мячика")

pygame.quit()        
