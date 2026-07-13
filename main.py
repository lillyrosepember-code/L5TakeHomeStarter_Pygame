import pygame
from pygame.locals import *
import sys

pygame.init()

size = (width, height) = (int(pygame.display.Info().current_w), int(pygame.display.Info().current_h))

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
color = (0, 0, 0)

def main():
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            # save game and exit
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                # confirm/ exit restart if triggered
                if event.key == K_ESCAPE:
                    sys.exit()

        screen.fill(color)
        pygame.display.flip()


if __name__ == "__main__":
    main()
