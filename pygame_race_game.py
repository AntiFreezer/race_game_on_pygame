import pygame as py
from random import choice, randint

py.init()

clock = py.time.Clock()

FrameHeight = 870
FrameWidth = 840

py.display.set_caption("Car race")
screen = py.display.set_mode((FrameWidth,
                              FrameHeight))
FPS = 35


class Traffic(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        img1 = "/home/linuxlite/Templates/pygame car game/car traffic1.svg"
        img2 = "/home/linuxlite/Templates/pygame car game/car traffic2.svg"
        cars = [img1, img2]
        self.image = py.image.load(choice(cars))
        self.image.set_colorkey((0, 0, 0))
        self.image = py.transform.rotate(self.image, 270)
        self.image = py.transform.scale(self.image, (90, 180))
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.center = (self.rect.center[0], self.rect.center[1] + self.speed)
        if self.rect.center[1] - self.rect.height / 2 > FrameHeight:
            all_sprites.remove(self)
            enemies.remove(self)
            pool.add(self)
            self.reset()

    def reset(self):
        self.speed = randint(7, 12)
        lanes = [230, 360, 480, 615]
        self.rect.center = (choice(lanes), - self.rect.height / 2)


class Backgound:
    def __init__(self):
        self.image = py.image.load("/home/linuxlite/Templates/pygame car game/background-1.png").convert()
        self.scroll = 0
        self.tiles = FrameHeight // self.image.get_height()
        self.starty = self.tiles * self.image.get_height()

    def update(self, screen):
        for i in range(self.tiles + 2):
            screen.blit(self.image, (0, self.starty - self.image.get_height() * i
                             - self.scroll))

        self.scroll -= 5

        if abs(self.scroll) > self.image.get_height():
            self.scroll = 0


class Player(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image = py.image.load("/home/linuxlite/Templates/pygame car game/player car.svg")
        self.image.set_colorkey((0, 0, 0))
        self.image = py.transform.rotate(self.image, 90)
        self.image = py.transform.scale(self.image, (80, 160))
        self.rect = self.image.get_rect()
        self.rect.center = (FrameWidth / 2, FrameHeight - self.rect.height / 2)
        self.stepvup = 7
        self.stepvdown = 9
        self.stepgor = 6
        self.blink = 0
        self.health = 6

    def update(self):
        leftborder = 140
        rightborder = FrameWidth - 136
        x = self.rect.center[0]
        y = self.rect.center[1]
        pk = py.key.get_pressed()
        if pk[py.K_UP]:
            if y - self.rect.height / 2 - self.stepvup > 0:
                self.rect.center = (x, y - self.stepvup)
            else:
                self.rect.center = (x, self.rect.height / 2)
        if pk[py.K_DOWN]:
            if y + self.rect.height / 2 + self.stepvdown < FrameHeight:
                self.rect.center = (x, y + self.stepvdown)
            else:
                self.rect.center = (x, FrameHeight - self.rect.height / 2)
        if pk[py.K_LEFT]:
            if x - self.rect.width / 2 - self.stepgor > leftborder:
                self.rect.center = (x - self.stepgor, y)
            else:
                self.rect.center = (self.rect.width / 2 + leftborder, y)
        if pk[py.K_RIGHT]:
            if x + self.rect.width / 2 + self.stepgor < rightborder:
                self.rect.center = (x + self.stepgor, y)
            else:
                self.rect.center = (rightborder - self.rect.width / 2, y)
        print(self.blink)
        if self.blink > 0:
            self.blink -= 1
            if self.blink % 3 == 0:
                self.image.set_alpha(0)
            if self.blink % 6 == 0:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def crash(self):
        if self.blink > 0:
            return
        self.blink = 2 * FPS
        self.health -= 1


def end_game():
    pass

traffic = Traffic()
enemies = py.sprite.Group()
enemies.add(traffic)

all_sprites = py.sprite.Group()
player = Player()
all_sprites.add(player, traffic)

#reserve
pool = py.sprite.Group()
for _ in range(10):
    pool.add(Traffic())

timecnt = 0

bg = Backgound()
while 1:
    if player.health == 0:
        end_game()
    clock.tick(FPS)
    timecnt += 1
    for event in py.event.get():
        if event.type == py.QUIT:
            quit()
        if event.type == py.KEYDOWN:
            player.update()

    # print(py.sprite.spritecollide(player, enemies, False, py.sprite.collide_rect_ratio(0.87)))
    for i in range(len(enemies)):
        for j in range(i, len(enemies)):
            if enemies.sprites()[i].rect.colliderect(enemies.sprites()[j].rect):
                enemies.sprites()[j].speed = enemies.sprites()[i].speed

    if len(enemies.sprites()) < 4 and timecnt % FPS == 0:
        tr = pool.sprites()[randint(0, len(pool.sprites()) - 1)]
        pool.remove(tr)
        all_sprites.add(tr)
        enemies.add(tr)

    playercrash = py.sprite.spritecollide(player, enemies, False, py.sprite.collide_rect_ratio(0.82))
    if playercrash:
        player.crash()


    bg.update(screen)

    all_sprites.update()
    all_sprites.draw(screen)

    py.display.flip()

py.quit()