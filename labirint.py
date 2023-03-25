# Разработай свою игру в этом файле!
from pygame import*
#Переменные для картинок
img_back = 'ship.jpg'
img_hero = 'doomBRO.png'
img_enemy = 'imp.png'
img_final = 'tenge.png'
img_bullet = 'bullet.png'
'''Музыка'''
mixer.init()
mixer.music.load('Music.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
'''Шрифт'''
font.init()
font = font.SysFont('Cosmic Sans MS',50)
win = font.render('VICTORY!',True,(255,255,0))
lose = font.render('WASTED', True,(255,255,255))
'''Классы'''
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Enemy(GameSprite):
    side = "left"
    def update(self):
        if self.rect.x <= 470:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side =="left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Enemy2(GameSprite):
    side = "up"
    def update(self):
        if self.rect.x <= 10:
            self.side = "right"
        if self.rect.x >= win_width - 600:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Enemy3(GameSprite):
    side = "up"
    def update(self):
        if self.rect.y <= 190:
            self.side = "up"
        if self.rect.y >= win_height - 150:
            self.side = "down"
        if self.side == "down":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
class Wall(sprite.Sprite):
    def __init__(self, red, green, blue, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.red = red
        self.green = green
        self.blue = blue
        self.w = wall_width
        self.h = wall_height
        self.image = Surface((self.w, self.h))
        self.image.fill((red, green, blue))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill()

'''Окно игры'''
#Окнооооо
win_width = 700
win_height = 500
display.set_caption('Лабиринт DOOMец')
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load(img_back),(win_width,win_height))
'''Персонажи'''
#self, player_image, player_x, player_y, width, height, player_speed)
hero = Player(img_hero, 5, win_height - 80, 40,40,10)
monster = Enemy(img_enemy, win_width - 100,400,65,65,4)
final = GameSprite(img_final, win_width - 120, win_height - 80,65,65, 0)
monster2 = Enemy2(img_enemy, win_width - 600, 60,65,65, 2)
monster3 = Enemy3(img_enemy, win_width - 200, 200,65,65, 2)
'''Стены'''
#self,   red,green,blue,wall_x,wall_y, wall_width, wall_height
w1 = Wall(154, 205, 50, 355, 201, 450, 10)
w2 = Wall(154, 205, 100, 480, 350, 10, 200)
w3 = Wall(154, 205, 50, 150, 315, 10, 480)
w4 = Wall(154, 205, 100, 150, 50, 10, 400)
w5 = Wall(154, 205, 100, 150, 105, 250, 10)
w6 = Wall(154, 205, 100, 150, 400, 250, 10)
'''группы спруйтов'''
bullets = sprite.Group()
walls = sprite.Group()
monsters = sprite.Group()
'''Группа спрайтов'''
monsters.add(monster)
monsters.add(monster2)
monsters.add(monster3)
walls.add(w1)
walls.add(w2)
walls.add(w3)
walls.add(w4)
walls.add(w5)
walls.add(w6)
'''Счет очков'''
points = 0
'''Игровой цикл'''
game = True
finish = False
clock = time.Clock()
FPS = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
                fire.play()
    if finish != True:
        window.blit(back, (0,0))

        walls.draw(window)
        monsters.update()
        monsters.draw(window)
        hero.reset()
        hero.update()
        final.reset()
        bullets.draw(window)
        bullets.update()
        sprite.groupcollide(bullets, walls, True, False)
        if sprite.groupcollide(bullets, monsters, True, True):
            points+=1
        x = font.render(str(points), True, (255, 255, 255))
        window.blit(x, (20, 20))

    if sprite.spritecollide(hero, monsters, walls, False):
        finish = True
        window.blit(lose, (200, 200))
    
    if sprite.collide_rect(hero,final):
        finish = True
        window.blit(win, (200, 200))

    display.update()
    clock.tick(FPS)