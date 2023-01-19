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
game_continues = True
endgamestat = False


def start_game():
    global game_continues
    global start_game_but
    start_game_but = Button((0, 255, 255), 155, 400, 515, 100, 'Start the game')
    game_continues = False


class Hud(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.hudmass = []
        self.hearts = 6
        for i in range(7):
            curhud = py.image.load('/home/linuxlite/PycharmProjects/race_game_on_pygame/hud' + str(i) + '.png')
            curhud = py.transform.scale(curhud, (95, 30))
            self.hudmass.append(curhud)
        self.image = self.hudmass[self.hearts]
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width // 2 + 15, self.rect.height // 2 + 20)

    def update(self):
        self.image = self.hudmass[self.hearts]

    def sethealth(self, num):
        if num <= 0 or num > 6:
            self.hearts = 0
            end_game()
            return
        self.hearts = num


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
    def __init__(self, f_hud):
        py.sprite.Sprite.__init__(self)
        self.f_hud = f_hud
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
        if self.f_hud:
            self.f_hud(self.health)


class Button(py.sprite.Sprite):
    def __init__(self, color, x, y, width, height, text=''):
        py.sprite.Sprite.__init__(self)
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = py.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + self.width // 2, self.y + self.height // 2)

    def draw(self, win, outline=None):
        if outline:
            py.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))

        py.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        if self.text != '':
            font = py.font.SysFont('console', 60, bold=True)
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text,
                     (self.x + (self.width / 2 - text.get_width() / 2),
                      self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, color):
        pos = py.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.color = (color[0], color [1] - 100, color[2])
            return True
        else:
            self.color = color

        return False


class EndGameImg(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image = py.image.load('gameoverimg.png').convert()
        self.image = py.transform.scale(self.image, (500, 500))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width // 2 + 150, self.rect.height // 2 + 150)


def end_game():
    global endgamestat
    global endgamegroup
    global endgameimg
    global game_continues
    global button
    endgamestat = True
    game_continues = False
    endgamegroup = py.sprite.Group()
    endgameimg = EndGameImg()
    endgamegroup.add(endgameimg)
    button = Button((255, 255, 0), 195, 650, 450, 100, 'New game')


def new_game():
    global endgamestat
    global health
    global game_continues
    global player
    endgamestat = False
    player.kill()
    health.kill()
    for i in all_sprites.sprites():
        i.reset()
        all_sprites.remove(i)
        enemies.remove(i)
        pool.add(i)
    health = Hud()
    player = Player(health.sethealth)
    all_sprites.add(player, health)
    game_continues = True

start_game()
traffic = Traffic()
enemies = py.sprite.Group()
enemies.add(traffic)
health = Hud()

all_sprites = py.sprite.Group()
player = Player(health.sethealth)
all_sprites.add(player, traffic, health)

#reserve
pool = py.sprite.Group()
for _ in range(10):
    pool.add(Traffic())

timecnt = 0

bg = Backgound()
while 1:
    clock.tick(FPS)
    timecnt += 1
    for event in py.event.get():
        if event.type == py.QUIT:
            quit()
        if event.type == py.KEYDOWN:
            player.update()
        if start_game_but and event.type == py.MOUSEBUTTONDOWN:
            if start_game_but.is_over((0, 255, 255)):
                game_continues = True
                start_game_but = False
        if event.type == py.MOUSEBUTTONDOWN and endgamestat:
            if button.is_over((255, 255, 0)):
                new_game()

    if game_continues:
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
    elif endgamestat:
        button.is_over((255, 255, 0))
        endgameimg.update()
        endgamegroup.draw(screen)
        button.draw(screen, (0, 0, 0))
    else:
        start_game_but.is_over((0, 255, 255))
        start_game_but.draw(screen, (0, 0, 0))
    py.display.flip()

py.quit()