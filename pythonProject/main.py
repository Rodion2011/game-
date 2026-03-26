import pygame
import json

pygame.init()
width = 800
height = 800


game_over = 0
score = 0

tile_size = 40

clock = pygame.time.Clock()
fps = 60


display = pygame.display.set_mode((width, height))
pygame.display.set_caption('hard game')

bg_image = pygame.image.load('game/tło.png')
bg_rect = bg_image.get_rect()

sound_jump = pygame.mixer.Sound('music/jump.wav')
sound_game_over = pygame.mixer.Sound('music/game_over.wav')
sound_coin = pygame.mixer.Sound('music/coin.wav')

with open('levels/level1.json', 'r') as file:
    world_data = json.load(file)

level = 1
max_level = 5


def reset_level():
    player.rect.x = 100
    player.rect.y = height - 130
    lava_group.empty()
    exit_group.empty()
    with open(f'levels/level{level}.json','r') as file:
        world_data = json.load(file)
    world = World(world_data)
    return world


def draw_text(text, color, size, x, y):
    font = pygame.font.SysFont('Arial', size)
    img = font.render(text, True, color)
    display.blit(img, (x, y))


class Player:
    def __init__(self):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img_right = pygame.image.load(f'game/player{num}.png')
            img_right = pygame.transform.scale(img_right, (35, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - tile_size - self.image.get_height()
        self.gravity = 0
        self.jumped = False
        self.direction = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        global game_over
        dx = 0
        dy = 0
        walk_speed = 5

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.gravity = -15
                self.jumped = True
                sound_jump.play()
            if key[pygame.K_a]:
                dx -= 5
                self.direction = -1
                self.counter += 1
            if key[pygame.K_d]:
                dx += 5
                self.direction = 1
                self.counter += 1

            if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                else:
                    self.image = self.images_left[self.index]

            self.gravity += 1
            if self.gravity > 10:
                self.gravity = 10
            dy += self.gravity

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.gravity < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    elif self.gravity >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.jumped = False

            if self.rect.y + dy >= height - tile_size - self.height:
                dy = height - tile_size - self.height - self.rect.y
                self.jumped = False

            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > height:
                self.rect.bottom = height

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

        elif game_over == -1:
            print('Game over')

        display.blit(self.image, self.rect)


class World:
    def __init__(self, data):
        dirt_img = pygame.image.load('game/1.png')
        grass_img = pygame.image.load('game/2.png')

        self.tile_list = []
        images = {1: dirt_img, 2: grass_img,}

        for row_index, row in enumerate(data):
            for col_index, tile in enumerate(row):
                if tile in images:
                    img = pygame.transform.scale(images[tile], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_index * tile_size
                    img_rect.y = row_index * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 3:
                    lava = Lava(col_index * tile_size,
                                row_index * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == 5:
                    exit = Exit(col_index * tile_size,
                                row_index * tile_size - (tile_size// 2))
                    exit_group.add(exit)
                elif tile == 6:
                    coin = Coin(col_index * tile_size + (tile_size // 2),
                                row_index * tile_size + (tile_size // 2))
                    coin_group.add(coin)

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('game/3.png')
        self.image = pygame.transform.scale(img,
                                            (tile_size, tile_size //2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


lava_group = pygame.sprite.Group()


class Button:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        display.blit(self.image, self.rect)
        return action


restart_button = Button(width // 2, height // 2 , 'game/restart.png')
start_button = Button(width // 2 - 150, height // 2, 'game/start.png')
exit_button = Button(width // 2 + 150, height // 2, 'game/exit.png')


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('game/5.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


exit_group = pygame.sprite.Group()


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('game/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


coin_group = pygame.sprite.Group()


world = World(world_data)
player = Player()


run = True
mein_menu = True

live = 4

while live:
    clock.tick(fps)
    display.blit(bg_image, bg_rect)
    if mein_menu:
        if start_button.draw():
            mein_menu = False
        if exit_button.draw():
            live = False
            level = 1
            score = 0
            world = reset_level()
    else:
        world.draw()
        lava_group.draw(display)
        player.update()
        lava_group.update()
        exit_group.draw(display)
        coin_group.draw(display)
        draw_text(str(score), (255, 255, 255), 30, 10, 10)

        if pygame.sprite.spritecollide(player, coin_group, True):
            sound_coin.play()
            score += 1
            print(score)
        if game_over == -1:
            sound_game_over.play()
            if restart_button.draw():
                player = Player()
                world = reset_level()
                score -= 1
                game_over = 0
                live -= 1

        if game_over == 1:
            game_over = 0
            if level < max_level:
                level += 1
                world = reset_level()
            else:
                print('that is end?')
                mein_menu = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            live = False

    pygame.display.update()

pygame.quit()