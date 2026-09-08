import numpy as np
import pygame


WIDTH=800
HEIGHT=600
PARTICLE_COUNT=100
RADIUS=5


pygame.init()

screen=pygame.display.set_mode((WIDTH,HEIGHT))
running=True
clock=pygame.time.Clock()

positions=np.random.uniform(low=[RADIUS,RADIUS],high=[WIDTH-RADIUS,HEIGHT-RADIUS],size=(PARTICLE_COUNT,2))
velocities=np.random.uniform(-400,400,(PARTICLE_COUNT,2))

while running:
    dt = clock.tick(180) / 1000
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    # pygame.draw.circle(surface, color, center, radius)
    screen.fill((255, 255, 255))

    x_wall_mask= (positions[:, 0] >= WIDTH-RADIUS) | (positions[:, 0] <= RADIUS)
    velocities[x_wall_mask, 0] *= -1


    y_wall_mask = (positions[:,1] <= RADIUS) | (positions[:, 1] >=HEIGHT-RADIUS)
    velocities[y_wall_mask, 1] *= -1


    for i in range(PARTICLE_COUNT):
        pygame.draw.circle(screen,(0,0,0),(positions[i,0],positions[i,1]),RADIUS)

    pygame.display.flip()
    positions+=velocities*dt







pygame.quit()

