import pygame
import numpy as np
from dotenv import load_dotenv
import os


load_dotenv()

WIDTH=int(os.getenv("WIDTH"))
HEIGHT=int(os.getenv("HEIGHT"))
RADIUS=10
GRAVITY=300
BOUNCY=0.8
STOP_THRESHOLD=20
FRICTION=100

pygame.init()
clock=pygame.time.Clock()

position=np.array([WIDTH/2,HEIGHT/2],dtype=float)
velocity=np.array([500,-500],dtype=float)

screen=pygame.display.set_mode((WIDTH,HEIGHT))
running=True

while running:

    dt=clock.tick(180)/1000

    screen.fill((255,255,255))

    velocity[1]+=GRAVITY*dt
    position += velocity * dt

    if position[1] >= HEIGHT-RADIUS and velocity[1] >= 0:
        print("Touched The Floor")
        position[1]=HEIGHT-RADIUS
        if abs(velocity[1])<STOP_THRESHOLD:
            velocity[1]=0
            if abs(velocity[0])>STOP_THRESHOLD:
                velocity[0] -= np.sign(velocity[0]) * FRICTION * dt
            else:
                velocity[0]=0
        else:
            velocity[1]*= -BOUNCY

    if position[1] <= RADIUS and velocity[1] <= 0:
        print("Touched The Ceil")
        position[1] = RADIUS
        velocity[1] *= -1


    if position[0] >= WIDTH-RADIUS and velocity[0] >= 0:
        print("Touched The Right Wall")
        position[0]=WIDTH-RADIUS
        velocity[0] *= -BOUNCY

    if position[0]<= RADIUS and velocity[0] <= 0:
        print("Touched The Left Wall")
        position[0]=RADIUS
        velocity[0] *= -BOUNCY


    pygame.draw.circle(screen,(0,0,0),position,RADIUS)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

pygame.QUIT