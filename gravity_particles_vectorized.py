import numpy as np
import pygame
from dotenv import load_dotenv
import os

load_dotenv()

WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))

PARTICLE_COUNT=10
RADIUS=10
GRAVITY=300
BOUNCY=0.8
FRICTION=100

THRESHOLD=20

pygame.init()

clock= pygame.time.Clock()

positions = np.random.uniform(
    [RADIUS,RADIUS],
    [WIDTH-RADIUS,HEIGHT-RADIUS],
    (PARTICLE_COUNT,2)
)

velocities = np.random.uniform(
    -100,
    100,
    (PARTICLE_COUNT,2)
)

screen= pygame.display.set_mode((WIDTH,HEIGHT))
running=True

while running:

    dt = clock.tick(180)/1000

    velocities[:,1] += GRAVITY*dt

    positions += velocities*dt

    floor_mask = (
            (positions[:, 1] >= HEIGHT - RADIUS)
            & (velocities[:, 1] > 0)
    )

    ceil_mask =(
        (positions[:,1] <= RADIUS)
        & (velocities[:,1] <0 )
    )

    right_wall_mask = (
            (positions[:, 0] >= WIDTH - RADIUS)
            & (velocities[:, 0] > 0)
    )

    left_wall_mask = (
            (positions[:, 0] <= RADIUS)
            & (velocities[:, 0] < 0)
    )

    stop_x_mask=(
    (abs(positions[:,0]) < THRESHOLD)
    )

    positions[floor_mask, 1] = HEIGHT - RADIUS
    positions[ceil_mask, 1] = RADIUS
    positions[right_wall_mask, 0] = WIDTH - RADIUS
    positions[left_wall_mask, 0] = RADIUS

    # VERTICAL MOTION ON THE FLOOR
    stop_y_mask = floor_mask & (np.abs(velocities[:, 1]) < THRESHOLD)
    bounce_y_mask = floor_mask & ~stop_y_mask

    velocities[stop_y_mask, 1] = 0
    velocities[bounce_y_mask, 1] *= -BOUNCY

    # CEILING AND SIDE WALL COLLISIONS
    velocities[ceil_mask, 1] *= -BOUNCY
    velocities[right_wall_mask, 0] *= -BOUNCY
    velocities[left_wall_mask, 0] *= -BOUNCY

    # HORIZONTAL FRICTION ON THE FLOOR
    stop_x_mask = floor_mask & (np.abs(velocities[:, 0]) < THRESHOLD)
    moving_x_mask = floor_mask & ~stop_x_mask

    velocities[stop_x_mask, 0] = 0

    velocities[moving_x_mask, 0] -= (
            np.sign(velocities[moving_x_mask, 0]) * FRICTION * dt
    )

    screen.fill((255, 255, 255))

    for position in positions:
        pygame.draw.circle(screen, (0, 0, 0), position, RADIUS)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
