from random import randint, choice
import pygame
import sqlite3

pygame.init()

W, H = 500, 500
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Galaga")

rocket_img = pygame.image.load("rocket.png")
rocket_img = pygame.transform.scale(rocket_img, (50, 100))

stones_img = [pygame.image.load(f"rock{i}.png") for i in range(0, 3)]
stones_img = [pygame.transform.scale(elem, (50, 50)) for elem in stones_img]
clock = pygame.time.Clock()


class Rocket(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = rocket_img
        self.rect = rocket_img.get_rect()
        self.rect.y = H * 0.8
        self.rect.x = W * 0.4

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5


player_group = pygame.sprite.Group()
player = Rocket()
player_group.add(player)


class Star():
    def __init__(self):
        self.x = randint(0, W)
        self.y = randint(0, H)
        self.rad = 1
        self.speed = randint(1, 3)

    def draw(self):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.rad)

    def move(self):
        self.y += self.speed
        if self.y >= H:
            self.y = 0


stars = [Star() for i in range(0, 50)]


class Stone(pygame.sprite.Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, W * 0.95)
        self.rect.y = randint(-H, 0)
        self.speed = randint(7, 9)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= H + self.rect.height:
            self.rect.y = 0
            self.rect.x = randint(0, W * 0.95)


stones = pygame.sprite.Group()
for i in range(5):
    Stone(choice(stones_img), stones)


def collision():
    if pygame.sprite.groupcollide(stones, player_group, True, True):
        print(f"Ваш счет: {int(score)}")
        exit()


def move_and_draw_all_sprites():
    player_group.draw(win)
    player_group.update()

    for star in stars:
        star.draw()
        star.move()

    stones.draw(win)
    stones.update()


score = 0


def score_and_background():
    global score
    win.fill(BLACK)

    score_text = pygame.font.SysFont('arial', 36)
    score_text = score_text.render(f'Score: {int(score)}', True, WHITE)
    score += 0.1

    win.blit(score_text, (W // 2, H // 2))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f"Ваш счет: int{score}")
            exit()

    score_and_background()
    move_and_draw_all_sprites()
    collision()
    pygame.display.update()
    clock.tick(FPS)