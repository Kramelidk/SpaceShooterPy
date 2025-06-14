#Create your own shooter

from pygame import *
import random

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size, player_size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = sprite.Group()

class Player(GameSprite):
    global bullets
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(("bullet.png"), self.rect.centerx, self.rect.top, 10, 25)
        bullets.add(bullet)

missed = 0

class Enemy(GameSprite):
    def update(self):
        global missed
        if self.rect.y < 450:
            self.rect.y += self.speed
        else:
            self.rect.y -= 500
            self.rect.x = random.randint(80, 700 - 80)
            missed += 1

class Asteroid(GameSprite):
    def update(self):
        if self.rect.y < 450:
            self.rect.y += self.speed
        else:
            self.rect.y -= 500
            self.rect.x = random.randint(80, 700 - 80)

class Explosion(GameSprite):
    def __init__(self, x, y):
        super().__init__("explosion.gif", x, y, 0, 100)
        self.fade_speed = 15
        self.alpha = 255

        self.image = transform.scale(image.load("explosion.gif").convert_alpha(), (100, 100))

    def update(self):
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.kill()
        else:
            faded_image = self.image.copy()
            faded_image.set_alpha(self.alpha)
            self.image = faded_image

window = display.set_mode((700, 500))
screenHeight = 500
screenWidth = 700
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

font.init()
fontVar = font.SysFont("Arial", 24)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play()

rocket = Player(("rocket.png"), 300, 400, 6, 65)
ufo = Enemy("ufo.png", random.randint(80, 700 - 80), -50, 1, 65)
ufo2 = Enemy("ufo.png", random.randint(80, 700 - 80), -50, 1, 65)
ufo3 = Enemy("ufo.png", random.randint(80, 700 - 80), -50, 1, 65)
ufo4 = Enemy("ufo.png", random.randint(80, 700 - 80), -50, 1, 65)
ufo5 = Enemy("ufo.png", random.randint(80, 700 - 80), -50, 1, 65)

asteroid1 = Asteroid("asteroid.png", random.randint(80, 700 - 80), -50, 2, 65)
asteroid2 = Asteroid("asteroid.png", random.randint(80, 700 - 80), -50, 2, 65)
asteroid3 = Asteroid("asteroid.png", random.randint(80, 700 - 80), -50, 2, 65)

rocketGroup = sprite.Group()
rocketGroup.add(rocket)

monsters = sprite.Group()
monsters.add(ufo)
monsters.add(ufo2)
monsters.add(ufo3)
monsters.add(ufo4)
monsters.add(ufo5)

asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)

clock = time.Clock()

score = 0

keys = key.get_pressed()
if keys[K_SPACE]:
    #bullet = Bullet(("bullet.png"), rocket.rect.x, rocket.rect.y, 5, 50)
    print("space")

youLoseText = font.SysFont("Arial", 80).render('YOU LOSE!', True, (255,50,50))
loseWidth = youLoseText.get_width()
loseHeight = youLoseText.get_height()

youWinText = font.SysFont("Arial", 80).render('YOU WIN!', True, (50,255,50))
winWidth = youWinText.get_width()
winHeight = youWinText.get_height()

reloadingText = font.SysFont("Arial", 60).render('reloading...', True, (255,20,30))
reloadWidth = reloadingText.get_width()
reloadHeight = reloadingText.get_height()

explosions = sprite.Group()

game = True
paused = False
canShoot = True
bulletsFired = 0
reloadTime = 1

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and bulletsFired < 5:
                canShoot = True
                rocket.fire()
                fireSound = mixer.Sound("8bitfire.wav")
                fireSound.set_volume(0.3)
                fireSound.play()
                #bulletsFired += 1
                canShoot = False

    if paused == False:

        window.blit(background, (0, 0))

        window.blit(fontVar.render('Score: ' + str(score), True, (100,100,100)), (10,20))
        window.blit(fontVar.render('Missed: ' + str(missed), True, (100,100,100)), (10,40))

        if missed >= 3:
            window.blit(youLoseText, (screenWidth / 2 - loseWidth / 2, screenHeight / 2 - loseHeight / 2))
            paused = True

        if score >= 20:
            window.blit(youWinText, (screenWidth / 2 - winWidth / 2, screenHeight / 2 - winHeight / 2))
            paused = True

        monsters.update()
        monsters.draw(window)

        asteroids.update()
        asteroids.draw(window)

        rocket.update()
        rocket.reset()

        bullets.update()
        bullets.draw(window)

        hits = sprite.groupcollide(bullets, monsters, True, True)
        score += len(hits)

        monsterCollisions = sprite.groupcollide(rocketGroup, monsters, True, True)
        asteroidCollisions = sprite.groupcollide(rocketGroup, asteroids, True, True)

        if monsterCollisions or asteroidCollisions:
            window.blit(youLoseText, (screenWidth / 2 - loseWidth / 2, screenHeight / 2 - loseHeight / 2))
            paused = True

        for hit in hits:
            for monster in hits[hit]:
                #explosion = GameSprite("explosion.gif")
                explosion = Explosion(monster.rect.centerx - 25, monster.rect.centery - 25)
                explosions.add(explosion)

                explosionSound = mixer.Sound("8bitexplosion.wav")
                explosionSound.set_volume(0.1)
                explosionSound.play()
                new_ufo = Enemy("ufo.png", random.randint(80, 700 - 80), -50, 1, 65)
                monsters.add(new_ufo)

        explosions.update()
        explosions.draw(window)

        display.update()
        clock.tick(60)


