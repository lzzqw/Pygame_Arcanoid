import pygame
import sys
import random
from os import path


def load_image(name, colorkey=None):
    fullname = path.join('data', name)
    # если файл не существует, то выходим
    if not path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Block(pygame.sprite.Sprite):
    images = [load_image(f'blocks/block_{i}.png') for i in range(0, 4)]

    def __init__(self, level, koord, group, wh):
        super().__init__(*group)
        self.w = wh[0]
        self.h = wh[1]
        self.image = Block.images[random.randint(0, 3)]
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = koord[0]
        self.rect.y = koord[1]

        self.hit = level
        self.koord = koord

    def get_center(self):
        return (self.w // 2 + self.rect.x, self.h // 2 + self.rect.y)

    def update(self):
        pass

    '''def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.koord[0], self.koord[1], 100, 50))'''


class Ball(pygame.sprite.Sprite):
    image = load_image("ball.png")
    bonus = None
    vx_start = 10
    vy_start = 10

    def __init__(self, group, koord=(400, 700)):
        pygame.sprite.Sprite.__init__(self)
        self.w = 30
        self.h = 30
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = koord[0]
        self.rect.y = koord[1]

        self.damage = 1
        self.vx = Ball.vx_start
        self.vy = Ball.vy_start
        self.kx = 1
        self.ky = -1

        self.vx_normal = 5
        self.vy_normal = 5

    def update(self):
        if self.rect.x + self.w < width and self.rect.x > 0:
            self.rect.x = self.rect.x + self.vx * self.kx
        else:
            self.kx *= -1
            self.rect.x = self.rect.x + self.vx * self.kx
        if self.rect.y > 0:
            self.rect.y = self.rect.y + self.vy * self.ky
        else:
            self.ky *= -1
            self.rect.y = self.rect.y + self.vy * self.ky

        if self.rect.y > hidth:
            balls.remove(self)
            list_bals.remove(self)
            all_sprites.remove(self)
            loose_game()

    def set_score(self, resize=False):
        if not Ball.bonus:
            Ball.vy_start *= 0.75
            Ball.vx_start *= 0.75
            for i in balls:
                i.vx *= 0.75
                i.vy *= 0.75
            Ball.bonus = Timer_score([all_sprites])
        if resize:
            Ball.vx_start = self.vx_normal
            Ball.vy_start = self.vy_normal
            for i in balls:
                i.vx = self.vx_normal
                i.vy = self.vy_normal
            all_sprites.remove(Ball.bonus)
            Ball.bonus = None

    def colision(self, hits, platf=False):
        if platf:
            self.ky *= -1
        else:
            bloc = hits[0]
            '''up = bloc.rect.ya
            down = bloc.rect.y + bloc.h
            left = bloc.rect.x
            right = bloc.rect.x + bloc.w'''
            if self.rect.y <= bloc.rect.y + bloc.h and self.rect.y > bloc.rect.y:
                self.ky *= -1
            elif self.rect.x <= bloc.rect.x + bloc.w and self.rect.x > bloc.rect.x:
                self.kx *= -1
            elif self.rect.y + self.h >= bloc.rect.y and self.rect.y + self.h < bloc.rect.y + bloc.h:
                self.ky *= -1
            elif self.rect.x + self.w >= bloc.rect.x and self.rect.x + self.w < bloc.rect.x + bloc.w:
                self.kx *= -1

            bloc.hit -= self.damage
            if bloc.hit <= 0:  # Отдельная функция с разбиением блока
                all_sprites.remove(bloc)
                blocks.remove(bloc)
                crash_block(bloc.get_center())
                check_game()

    '''def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), self.koord, 10)'''


class Platform(pygame.sprite.Sprite):
    image = load_image("platform.png")

    def __init__(self, group):
        super().__init__(*group)
        self.w = 150
        self.h = 25
        self.image = pygame.transform.scale(Platform.image, (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = width// 2
        self.rect.y = hidth - 50

        self.vx = 1
        self.vy = -1
        self.bonus = False
        self.w_normal = self.w

    def left_move(self):
        if self.rect.x > 0:
            self.rect.x -= 15

    def right_move(self):
        if self.rect.x + self.w < width:
            self.rect.x += 15

    def set_size(self, resize=False):
        if not self.bonus:
            self.bonus = Timer_platform([all_sprites])
            self.w *= 1.5
            x = self.rect.x
            y = self.rect.y

            self.image = pygame.transform.scale(Platform.image, (self.w, self.h))
            self.rect = self.image.get_rect()
            self.rect.x = x - self.w * 0.25
            self.rect.y = y
            print(self.w)
        if resize:
            self.w = self.w_normal
            self.image = pygame.transform.scale(Platform.image, (self.w, self.h))
            all_sprites.remove(self.bonus)
            self.bonus = None

            print(self.w)


    def update(self):
        if pressed_keys[pygame.K_a]:
            self.left_move()
        elif pressed_keys[pygame.K_d]:
            self.right_move()

    '''def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.koord, 900, 200, 50))'''

class Timer_score(pygame.sprite.Sprite):
    image = load_image("timer_score.png")
    def __init__(self, group):
        super().__init__(*group)
        self.w = width
        print(00)
        self.add(group)
        print(self)
        self.h = 10
        self.image = pygame.transform.scale(Timer_score.image, (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = hidth - 20

    def update(self):
        self.w -= 1
        if self.w <= 0:
            for i in balls:
                i.set_score(resize=True)
        else:
            self.image = pygame.transform.scale(Timer_score.image, (self.w, self.h))

class Timer_platform(pygame.sprite.Sprite):
    image = load_image("timer_platform.png")
    def __init__(self, group):
        super().__init__(*group)
        self.w = width
        print(00)
        self.add(group)
        self.h = 10
        self.image = pygame.transform.scale(Timer_platform.image, (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = hidth - 10

    def update(self):
        self.w -= 1
        if self.w <= 0:
            platform.set_size(resize=True)
        else:
            self.image = pygame.transform.scale(Timer_platform.image, (self.w, self.h))




class Bonus(pygame.sprite.Sprite):
    def __init__(self, group, img, center):
        super().__init__(*group)
        self.w = 35
        self.h = 35
        self.images = [load_image(f"{img}{i}.png") for i in range(0, 5)]
        self.i = 0
        self.time = 0
        self.image = pygame.transform.scale(self.images[self.i], (self.w, self.h))
        self.rect = self.image.get_rect()

        self.rect.x = center[0]
        self.rect.y = center[1]

    def update(self):
        self.rect.y += 5
        if self.time == 3:
            self.i += 1
            self.i = self.i % 5
            self.image = pygame.transform.scale(self.images[self.i], (self.w, self.h))
        self.time += 1
        self.time = self.time % 4

    def colision(self):
        pass





class Bonus_platf(Bonus):

    def __init__(self, group, center):
        super().__init__(group, 'bonus_platform/bonus_platform_', center)

    def colision(self):
        platform.set_size()



class Bonus_bal(Bonus):
    image = load_image("bonus_2.png")

    def __init__(self, group, center):
        super().__init__(group, 'bonus_ball/bonus_ball_', center)

    def colision(self):
        a = Ball([all_sprites, balls], koord=(platform.rect.x + 50, platform.rect.y - 40))
        a.add([[all_sprites, balls]])
        list_bals.append(a)


class Bonus_score(Bonus):
    image = load_image("bonus_3.png")

    def __init__(self, group, center):
        super().__init__(group, 'bonus_score/bonus_score_', center)

    def colision(self):
        print(list_bals)
        list_bals[0].set_score()




def reset_level(level):
    num_hor = 13
    num_vert = 20
    w = width // num_hor
    h = (hidth // 2) // num_vert

    a = [[random.randint(0, 1) for j in range(num_hor)] for i in range(num_vert)]
    lst = []
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j]:
                koord = 0 + j * w, 0 + i * h
                d = Block(level, koord, all_sprites, (w, h))
                lst.append(d)
    return lst


def check_game():
    if len(blocks) == 0:
        return True

    else:
        return False


def loose_game():
    if len(balls) == 0:
        return True
    else:
        return False


def gen_bonus(center):
    type = random.randint(0, 2)
    if not type:
        return Bonus_platf((bonuses, all_sprites), center)
    elif type == 1:
        return Bonus_bal((bonuses, all_sprites), center)
    else:
        return Bonus_score((bonuses, all_sprites), center)


def crash_block(center):
    if bonus_ver[random.randint(0, 9)]:
        a = gen_bonus(center)
        '''a.add(*[bonuses, all_sprites])
        bonuses.add(a)
        all_sprites.add(a)'''
        print(a)


def check_colision():
    hits = pygame.sprite.groupcollide(balls, blocks, False, False)
    hit_of_platform = pygame.sprite.spritecollide(platform, balls, False)
    hits_bonus = pygame.sprite.spritecollide(platform, bonuses, False)
    if hits:
        for k in hits:
            k.colision(hits[k])


        #bal.colision(hits)
    for i in hit_of_platform:
        i.colision(platform, platf=True)
    for i in hits_bonus:
        i.colision()
        all_sprites.remove(i)
        bonuses.remove(i)


pygame.init()
FPS = 40
game = False
level = 1
com = ''
img_dir = path.join(path.dirname('/ываваава/data'), 'data')
img_ball = load_image('ball.png')
img_platform = load_image('platform.png')
img_block = load_image('block.png')
img_walper_1 = load_image('walper_1.png')

width = 800
hidth = 950
background_1 = pygame.transform.scale(img_walper_1, (width, hidth))
background_1_rect = background_1.get_rect()
clock = pygame.time.Clock()
txxt1 = pygame.font.SysFont('serif', 48)
text_1 = txxt1.render('Вы выиграли!', False, (0, 180, 0))
txxt2 = pygame.font.SysFont('serif', 48)
text_2 = txxt2.render('Вы проиграли!', False, (0, 180, 0))
txxt3 = pygame.font.SysFont('serif', 48)
text_3 = txxt2.render('', False, (0, 180, 0))
txxt4 = pygame.font.SysFont('serif', 30)
text_4 = txxt2.render('Нажмите пробел, чтобы играть', False, (0, 180, 0))
list_bals = []
com = {1: text_1,
       2: text_2,
       3: text_3}
com_id = 3
bonus_ver = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
bonus_ver = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

screen = pygame.display.set_mode((width, hidth))
button = pygame.Surface((400, 100))
button.fill('Black')
screen.blit(button, (200, 600))
# bullet_group = pygame.sprite.Group()


pygame.display.update()

c = 0
# главный цикл
while True:
    screen.fill((255, 255, 255))
    clock.tick(FPS)
    if not game:
        screen.blit(background_1, background_1_rect)
        txxt = pygame.font.SysFont('serif', 48)
        text_1 = txxt.render(f'Ваш уровень: {level}', False, (0, 180, 0))
        screen.blit(com[com_id], (10, 750))
        screen.blit(text_4, (10, 800))
        screen.blit(text_1, (200, 50))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:  # Перенести в начало. Реализовать отчистку групп при проигрыше. Синхронизация сложности с уровнем
                    game = True
                    all_sprites = pygame.sprite.Group()
                    blocks = pygame.sprite.Group()
                    bal = Ball(all_sprites)
                    list_platform = pygame.sprite.Group()
                    bonuses = pygame.sprite.Group()
                    balls = pygame.sprite.Group()
                    balls.add(bal)
                    list_bals.append(bal)

                    # all_sprite.append(bal)
                    blks = reset_level(level)

                    '''for i in blocks:
                        all_sprites.add(i)'''
                    platform = Platform(all_sprites)
                    list_platform.add(platform)
                    all_sprites.add(platform, bal, blks)
                    blocks.add(blks)
                    # all_sprite.append(platform)
    elif game:
        # print(1)
        screen.fill((255, 255, 255))
        screen.blit(background_1, background_1_rect)
        pressed_keys = pygame.key.get_pressed()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()

        '''for i in blocks:
            i.update()
            i.draw(screen)
        platform.update(pressed_keys)
        platform.draw(screen)'''
        all_sprites.draw(screen)
        all_sprites.update()
        check_colision()

        if check_game():
            game = False
            level += 1
            com_id = 1
        elif loose_game():
            game = False
            com_id = 2

    pygame.display.update()