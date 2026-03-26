import pygame
pygame.init()
width = 800
height = 800

clock = pygame.time.Clock()
fps = 60

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('hero')

bg_image = pygame.image.load('game/tło.png')
bg_rect = bg_image.get_rect()

class Hero:
    def __init__(self):
        self.counter = 0
        self.direction = 0
        for num in range(1, 5):
            img_right = pygame.image.load((f'game/player{num}.png'))
            img_right = pygame.transform.scale(img_right, (90, 120))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.image = pygame.image.load('game/player4.png')
        self.image = pygame.transform.scale(self.image, (90, 120))
        self.rect = self.image.get_rect()

    def update (self):
        x = 0
        y = 0
        if key[pygame.K_a]:
            x -= 5
        if key[pygame.K_d]:
            x += 5

hero = Hero()

run = True
while run:
    clock.tick(fps)
    display.blit(bg_image, bg_rect)
    hero.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()