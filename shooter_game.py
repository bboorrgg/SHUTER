import pygame
from random import randint

pygame.init()

screen_title = 'ШУТЕР'
screen_width = 700
screen_height = 500
screen_color = (0, 0, 0)

class Hitbox():
    def __init__(self, screen, x, y, width, height, color, thickness):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        if thickness < 1:
            thickness = 1
        self.thickness = thickness

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_hitbox(self):
        pygame.draw.rect(self.screen, self.color, self.rect, self.thickness)

class Picture(Hitbox):
    def __init__(self, screen, x, y, width, height, color, thickness, image_path):
        Hitbox.__init__(self, screen, x, y, width, height, color, thickness)
        self.image_path = image_path

        self.image = pygame.transform.scale(pygame.image.load(self.image_path).convert_alpha(), (self.width, self.height))

    def draw_picture(self):
        # отрисоваем изображение и текст (blit)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(Picture):
    def __init__(self, screen, x, y, width, height, color, thickness, image_path, speed):
        Picture.__init__(self, screen, x, y, width, height, color, thickness, image_path)
        self.speed = speed 

        self.dy = 1

    def move(self):
        self.rect.y += self.speed * self.dy
    
    def randomize(self):
        self.rect.x = randint(0, screen_width - self.width)
        self.rect.y = -self.height

    def collide__screen(self):
        if self.rect.top > screen_height:
            self.randomize()
            return 1
        else:
            return 0
        


class Player(Picture):
    def __init__(self, screen, x, y, width, height, color, thickness, image_path, speed):
        Picture.__init__(self, screen, x, y, width, height, color, thickness, image_path)
        self.speed = speed 

        self.dx = 0
        self.dy = 0 
        
    def move(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

    def controller(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.dx = -1
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.dx = 1
        else:
            self.dx = 0
        
    def collide_screen(self, screen_height, screen_width):
            
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.right > screen_height:
            self.rect.right = screen_height

class Bullet(Picture):
    def __init__(self, screen, x, y, width, height, color, thickness, image_path, speed):
        Picture.__init__(self, screen, x, y, width, height, color, thickness, image_path)
        self.speed = speed

        self.dx = 0
        self.dy = -1

    def move(self):
        self.rect.y += self.speed * self.dy

            
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption(screen_title)

tickrate = 60
clock = pygame.time.Clock()

player = Player(screen, -0, 450, 100, 50, (0, 0, 0), 2, 'rocket.png', 5)
picture = Picture(screen, 0, 0, 700, 500, (0, 0, 0), 2, 'galaxy.jpg')


enemy_1 = Enemy(screen, 0, -50, 50, 30, (0, 0, 0), 2, 'ufo.png', 1)
enemy_1.randomize()

enemy_2 = Enemy(screen, 0, -50, 50, 30, (0, 0, 0), 2, 'ufo.png', 2.5)
enemy_2.randomize()

enemy_3 = Enemy(screen, 0, -50, 50, 30, (0, 0, 0), 2, 'ufo.png', 2)
enemy_3.randomize()

enemy_4 = Enemy(screen, 0, -50, 50, 30, (0, 0, 0), 2, 'ufo.png', 1.5)
enemy_4.randomize()

enemy_5 = Enemy(screen, 0, -50, 50, 30, (0, 0, 0), 2, 'ufo.png', 2)
enemy_5.randomize()

fire = pygame.mixer.Sound('fire.ogg')
fire.set_volume(0.1)

missed = 0
point = 0

missed_text = pygame.font.SysFont(None, 48).render('Пропушено: ' + str(missed), True, (255, 255, 255))
point_text = pygame.font.SysFont(None, 48).render('Счет: ' + str(point), True, (255, 255, 255))

win_text = False
lose_text = False

win_text = pygame.font.SysFont(None, 48).render('YOU WIN', True, (223, 223, 48))
lose_text = pygame.font.SysFont(None, 48).render('YOU LOSE', True, (255, 0, 0))

bullets = []
game_is_working = True
while game_is_working:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_is_working = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(screen, 0, 0, 8, 32, (0, 0, 0), 2, 'bullet.png', 2)
                bullet.rect.bottom = player.rect.top
                bullet.rect.centerx = player.rect.centerx
                bullets.append(bullet)
                fire.play()



    picture.draw_picture()

    player.draw_picture()
    player.controller()
    player.move()

    enemy_1.draw_picture()
    enemy_1.move()
    missed += enemy_1.collide__screen()

    enemy_2.draw_picture()
    enemy_2.move()
    missed += enemy_2.collide__screen()

    enemy_3.draw_picture()
    enemy_3.move()
    missed += enemy_3.collide__screen()

    enemy_4.draw_picture()
    enemy_4.move()
    missed += enemy_4.collide__screen()

    enemy_5.draw_picture()
    enemy_5.move()
    missed += enemy_5.collide__screen()
    missed_text = pygame.font.SysFont(None, 48).render('Пропушено: ' + str(missed), True, (255, 255, 255))
    
    screen.blit(missed_text, (0, 0))
    screen.blit(point_text, (0, 45))

    for bullet in bullets:
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
            
        bullet.draw_picture()
        bullet.move()

        if bullet.rect.colliderect(enemy_1):
            bullets.remove(bullet)
            enemy_1.randomize()
            point += 1
            point_text = pygame.font.SysFont(None, 48).render('Счет: ' + str(point), True, (255, 255, 255))

        if bullet.rect.colliderect(enemy_2):
            bullets.remove(bullet)
            enemy_2.randomize()
            point += 1
            point_text = pygame.font.SysFont(None, 48).render('Счет: ' + str(point), True, (255, 255, 255))

        if bullet.rect.colliderect(enemy_3):
            bullets.remove(bullet)
            enemy_3.randomize()
            point += 1
            point_text = pygame.font.SysFont(None, 48).render('Счет: ' + str(point), True, (255, 255, 255))

        if bullet.rect.colliderect(enemy_4):
            bullets.remove(bullet)
            enemy_4.randomize()
            point += 1
            point_text = pygame.font.SysFont(None, 48).render('Счет: ' + str(point), True, (255, 255, 255))
        
        if bullet.rect.colliderect(enemy_5):
            bullets.remove(bullet)
            enemy_5.randomize()
            point += 1
            point_text = pygame.font.SysFont(None, 48).render('Счет: ' + str(point), True, (255, 255, 255))

    if player.rect.colliderect(enemy_1):
        screen.blit(lose_text, (350, 250 ))
        player.speed = 0
        enemy_1.speed = 0
        enemy_2.speed = 0
        enemy_3.speed = 0
        enemy_4.speed = 0
        enemy_5.speed = 0

    elif player.rect.colliderect(enemy_2):
        screen.blit(lose_text, (350, 250))
        player.speed = 0
        enemy_1.speed = 0
        enemy_2.speed = 0
        enemy_3.speed = 0
        enemy_4.speed = 0
        enemy_5.speed = 0

    elif player.rect.colliderect(enemy_3):
        screen.blit(lose_text, (350, 250))
        player.speed = 0
        enemy_1.speed = 0
        enemy_2.speed = 0
        enemy_3.speed = 0
        enemy_4.speed = 0
        enemy_5.speed = 0

    elif player.rect.colliderect(enemy_4):
        screen.blit(lose_text, (350, 250))
        player.speed = 0
        enemy_1.speed = 0
        enemy_2.speed = 0
        enemy_3.speed = 0
        enemy_4.speed = 0
        enemy_5.speed = 0

    elif player.rect.colliderect(enemy_5):
        screen.blit(lose_text, (350, 250))
        player.speed = 0
        enemy_1.speed = 0
        enemy_2.speed = 0
        enemy_3.speed = 0
        enemy_4.speed = 0
        enemy_5.speed = 0
        
    elif missed >= 3:
        screen.blit(lose_text, (350, 250))
        player.speed = 0
        enemy_1.speed = 0
        enemy_2.speed = 0
        enemy_3.speed = 0
        enemy_4.speed = 0
        enemy_5.speed = 0

    if point >= 10:
        screen.blit(win_text, (350, 250))
        player.speed = 0
        enemy_1.speed = 0
        enemy_2.speed = 0
        enemy_3.speed = 0
        enemy_4.speed = 0
        enemy_5.speed = 0
        
    


    pygame.display.flip()
    clock.tick(tickrate)
