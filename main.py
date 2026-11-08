import pygame
from pygame.locals import *
import sys
import random

pygame.init()

height = 600
width = 400

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
orange = (255, 165, 0)
score = 0


class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - 50)
        self.normal_speed = 5
        self.speed = 5
        self.slow_until = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    def slow_down(self):
        self.speed = 2
        self.slow_until = max(
            pygame.time.get_ticks(),
            self.slow_until
        ) + 3000

    def updateSpeed(self):
        if pygame.time.get_ticks() >= self.slow_until:
            self.speed = self.normal_speed


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, brick_width):
        super().__init__()
        self.image = pygame.Surface((brick_width, 20))
        self.image.fill(color)
        brickX = random.randint(0, width - brick_width)
        self.rect = self.image.get_rect()
        self.rect.x = brickX
        self.rect.y = -20
        self.speed = random.randint(3, 6)

    def update(self):
        global score
        self.rect.y += self.speed
        if self.rect.top > height:
            self.kill()
            score += 1


class poisonBrick(Brick):
    def __init__(self):
        super().__init__(red, random.randint(50, 100))


class slowBrick(Brick):
    def __init__(self):
        super().__init__(orange, random.randint(50, 100))


player1 = player()
poison_bricks = pygame.sprite.Group()
slow_bricks = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player1)


brick_timer = 0
brick_interval = 30

game_over = False

font = pygame.font.SysFont(None, 50)


def main():
    global brick_timer, game_over
    game = True
    while game:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            global score
            player1.move()
            player1.updateSpeed()
            brick_timer += 1
            if brick_timer >= brick_interval:
                if random.random() < 0.20:
                    new_brick = slowBrick()
                    slow_bricks.add(new_brick)
                else:
                    new_brick = poisonBrick()
                    poison_bricks.add(new_brick)

                all_sprites.add(new_brick)
                brick_timer = 0

            all_sprites.update()

            poison_hits = pygame.sprite.spritecollide(
                player1, poison_bricks, False)
            if poison_hits:
                game_over = True

            slow_hits = pygame.sprite.spritecollide(
                player1, slow_bricks, True)
            if slow_hits:
                player1.slow_down()

        screen.fill(white)

        if not game_over:
            all_sprites.draw(screen)
        else:
            text = font.render("GAME OVER", True, red)
            text_rect = text.get_rect(
                center=(width // 2, height // 2)
            )

            screen.blit(text, text_rect)
        text = font.render(f"Score: {score}", True, blue)
        screen.blit(text, (10, 10))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
