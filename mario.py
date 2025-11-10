from pygame import*
from random import*

import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'

def text(message,x,y,font_color,font_size, font_type='assets/font.otf'):
        font_type=font.Font(font_type,font_size)
        text=font_type.render(message,True,font_color)
        window.blit (text, (x,y))




init()
fireball_set=0
mari=0
mm=0
move=0
fire=0
no_fire=0
# Corrected file path and typo
mixer.music.load('assets/mario-theme.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.1)
ouchs=mixer.Sound('assets/ouchs.ogg')
bye=mixer.Sound('assets/goomba-destroy.ogg')
mx=43
my=80
big=0
game=1
time_set=0
fire_time1=time.get_ticks()
fire_time2=time.get_ticks()
# Corrected file path and typo (assuming 'mario-end.ogg')
end=mixer.Sound('assets/mario-end.ogg') 
jump=mixer.Sound('assets/stomp.ogg')
sound=0
jump_count=30
score = 0
goomba_direction=0
# This file is MISSING from your assets folder!
csound=mixer.Sound('assets/coin-sound.ogg') 
power=mixer.Sound('assets/power-up.ogg')
win=mixer.Sound('assets/mario-win.ogg')
goomba_bye=0
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)
mario_blue = (116,147,246)
question_cooldown=0
width=1000
height =495
map=[
    'b    h      h     h                                                                                                                                                    ',
    'b                                                                                                                                                                      ',
    'b                                                                                                                                                                      ',
    'b                                                                                                                                                                      ',
    'b                                                                                                                                                                      ',
    'b                                                                                                                                                                      ',
    'b                                                                             g  g                                                                                     ',
    'b          ...u..     .?.                                                    .........                                     s                                           ',
    'b  m                                                                                                                      ss                                           ',
    'b                    .                        ..  .                                                                      sss                                           ',
    'b                   ...                      ...  ..                      .f.                                           ssss                                           ',
    'b               ...   ..                    ....  ...                                                                  sssss           c                               ',
    'b    h                                     .....  ....         ?????                                                  ssssss                                           ',
    'b  t =      ==g    p      ==g     =       ......  .....                                                   gg         sssssss       l   #                               ',
    'b-----------------------------------------------  --------------------  -------------   -------------------------------------------------------------------------------',
    'b-----------------------------------------------  --------------------  -------------   -------------------------------------------------------------------------------',
    'b-----------------------------------------------  --------------------  -------------   -------------------------------------------------------------------------------',
]

class  Ground (sprite.Sprite):
    def __init__(self, x,y,id):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/ground.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.id = id
    def update(self):
        global move
        keys = key.get_pressed()
        if keys[K_RIGHT] and move==1:
            self.rect.x-=10
        if keys[K_LEFT] and move==1:
            move=0



class  Castle (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/mario-castle.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        global move
        keys = key.get_pressed()
        if keys[K_RIGHT] and move==1:
            self.rect.x-=10
        if keys[K_LEFT] and move==1:
            move=0



class  Stair (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/stair.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        global move
        # run()
        keys = key.get_pressed()
        if keys[K_RIGHT] and move==1:
            self.rect.x-=10
        if keys[K_LEFT] and move==1:
            # self.rect.x+=10
            move=0



class  Fireball (sprite.Sprite):
    def __init__(self, x,y,dir):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/fireball.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.direction=dir
        self.fall_speed = 2
        self.on_ground = False
    def upload(self):
        global no_fire
        if no_fire==1:
            self.kill()
        print('test')
    def update(self):
        
        global no_fire
        # pass
        self.rect.y+=self.fall_speed
        self.fall_speed+=0.5
        bricks=sprite.spritecollide(self,ground_group,False)
        for w in bricks:
                self.rect.bottom = w.rect.top
                self.fall_speed=2
                self.on_ground=True
        if self.on_ground==True:
            # self.jump()
            self.rect.y-=40
            self.on_ground=False
        if self.direction=='right':
            self.rect.x+=5
        else:
            self.rect.x-=5
        if no_fire==1:      
            self.kill
    

class  Barrier (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/barrier.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]



class  Fbarrier (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/barrier.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        global move
        # run()
        keys = key.get_pressed()
        if keys[K_RIGHT] and move==1:
            self.rect.x-=10
        if keys[K_LEFT] and move==1:
            # self.rect.x+=10
            move=0



class  Flower (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/fire_flower.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        global move
        # run()
        keys = key.get_pressed()
        if keys[K_RIGHT] and move==1:
            self.rect.x-=10
        if keys[K_LEFT] and move==1:
            # self.rect.x+=10
            move=0
        if sprite.spritecollide(self, mario_group, False):
            global fire
            self.kill()
            fire=1

class  Goomba (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/goomba.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.direction=-3
        self.speed=5
        self.fall_speed = 2
        self.generate=randint(1,2)
    def update(self):
        global move
        keys = key.get_pressed()
        if keys[K_RIGHT] and move==1:
            self.rect.x-=10
        if keys[K_LEFT] and move==1:
            move=0
            # self.rect.x+=10
        global goomba_bye
        self.rect.y+=self.fall_speed
        self.fall_speed+=0.5
        bricks=sprite.spritecollide(self,ground_group,False)
        for w in bricks:
                if w.id==0:
                    self.rect.bottom = w.rect.top
                    self.fall_speed = 0
        if mario.rect.collidepoint(self.rect.centerx,self.rect.top) or sprite.spritecollide(self, fireball_group, True):
            self.kill()
            global game, size
            mixer.Sound.play(bye)
            goomba_bye+=1
        elif mario.rect.collidepoint(self.rect.left,self.rect.centery) or mario.rect.collidepoint(self.rect.right,self.rect.centery):
            global sound
            mario.image = image.load('assets/ouch.png')
            if sound == 0:
                game=0
                sound+=1
            mario.kill()
        if abs(self.rect.x-mario.rect.x)<20*30:
            if sprite.spritecollide(self,obstacle_group,False):
                if self.direction==-3:
                    self.direction=3
                else:
                    self.direction=-3
            self.rect.x+= self.direction
class  Mushroom (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/mushroom.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        global move
        keys = key.get_pressed()
        if keys[K_RIGHT] and move==1:
            self.rect.x-=10
        if keys[K_LEFT] and move==1:
            move=0
            # self.rect.x+=10

class  Fquestion (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/question.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.state = True
        self.id = randint(1,2)
        # self.id2 = randint(1,2)
    def update(self):
        global move
        keys = key.get_pressed()
        if self.state==True:
            if keys[K_RIGHT] and move==1:
                self.rect.x-=10
            if keys[K_LEFT] and move==1:
                move=0
        if self.state==False:
            if keys[K_RIGHT] and move==1:
                self.rect.x-=5
            # self.rect.x+=10
        if self.rect.colliderect(mario.rect) and self.state == True:
            # if self.id == 1:
            global flower
            flower = Flower(self.rect.centerx,self.rect.top-13)
            flower_group.add(flower)
            # else:
            #     mushroom = Mushroom(self.rect.centerx,self.rect.top-13)
            #     mushroom_group.add(mushroom)
            self.image = image.load('assets/empty.png')
            # print('yay')
            self.state = False
            obstacle_group.add(self)

class  Question (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/question.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.state = True
        self.id = randint(1,2)
        # self.id2 = randint(1,2)
    def update(self):
        global move
        keys = key.get_pressed()
        if self.state==True:
            if keys[K_RIGHT] and move==1:
                self.rect.x-=10
            if keys[K_LEFT] and move==1:
                move=0
        if self.state==False:
            if keys[K_RIGHT] and move==1:
                self.rect.x-=5
            # self.rect.x+=10
        if self.rect.colliderect(mario.rect) and self.state == True:
            # if self.id == 1:
            coin = Coin(self.rect.centerx,self.rect.top-13)
            coin_group.add(coin)
            # else:
            #     mushroom = Mushroom(self.rect.centerx,self.rect.top-13)
            #     mushroom_group.add(mushroom)
            self.image = image.load('assets/empty.png')
            # print('yay')
            self.state = False
            obstacle_group.add(self)
            
class  Mquestion (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/question.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.state = True
        self.id = randint(1,2)
        # self.id2 = randint(1,2)
    def update(self):
        global move
        keys = key.get_pressed()
        if self.state==True:
            if keys[K_RIGHT] and move==1:
                self.rect.x-=10
            if keys[K_LEFT] and move==1:
                move=0
        if self.state==False:
            if keys[K_RIGHT] and move==1:
                self.rect.x-=5
            # self.rect.x+=10
        if self.rect.colliderect(mario.rect) and self.state == True:
            # if self.id == 1:
            # coin = Coin(self.rect.centerx,self.rect.top-13)
            # coin_group.add(coin)
            # else:
            mushroom = Mushroom(self.rect.centerx,self.rect.top-13)
            mushroom_group.add(mushroom)
            self.image = image.load('assets/empty.png')
            # print('yay')
            self.state = False
            obstacle_group.add(self)

class  Brick (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/mario-brick.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.id = 0
    def update(self):
        global move
        keys = key.get_pressed()
        if keys[K_RIGHT] and move==1:
            self.rect.x-=10
        if keys[K_LEFT] and move==1:
            move=0
            # self.rect.x+=10

class  Tnt (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/tnt.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        global move
        keys = key.get_pressed()
        if keys[K_RIGHT] and move==1:
            self.rect.x-=10
        if keys[K_LEFT] and move==1:
            move=0
        #     self.rect.x+=10

class  Coin (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/coin2.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        global move
        keys = key.get_pressed()
        if keys[K_RIGHT] and move==1:
            self.rect.x-=10
        if keys[K_LEFT] and move==1:
            move=0
        #     self.rect.x+=10
        global score
        if sprite.spritecollide(self, mario_group, False):
            self.kill()
            mixer.Sound.play(csound)
            score+=1
            # print(score)

class  Mario (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/mario1.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.direction = 'down'
        self.make_jump = False
        self.fall_speed = 2
        self.on_ground = False
        self.mx=36
        self.my=48
        
    def update(self):
        keys = key.get_pressed()
        
        # if self.rect.centerx >= width/2:
        global move, mari, mm, fire, fireball_set, fire_time1, fire_time2, time_set, game, no_fire
        #     move=1
        # if fire==1:
        if sprite.spritecollide(self, testing_group, False):
            no_fire=1
            
            print('test')
            # time.delay(5000)
            fireball_group.empty()
            game=3
        if self.rect.y >= height:
            game=0
        fire_time2=time.get_ticks()
        # print(fire_time2)
        if sprite.spritecollide(self, fquestion_group, False):
            no_fire=1
        if fire_time2-fire_time1>=500:
            time_set=1
            # fire_time2=fire_time1
            fire_time1=fire_time2
            # print(fire)
        if self.rect.centerx >= width/2:
            move=1
        if keys[K_LEFT] and move==1:
            move=0
        # global fire
        if fire==1:
            self.image = image.load('assets/fire_mario.png')
            fireball_set=fire
            # fire=3
            # pass
        self.rect.y+=self.fall_speed
        self.fall_speed+=0.5
        # print(self.fall_speed)
        if sprite.spritecollide(self,mushroom_group,True):
            global big
            big=1
            self.mx=36
            self.my=60
            # self.image = transform.scale(self.image,(43,150))
            # print('mushroom')
            mixer.Sound.play(power)
        if sprite.spritecollide(self,tnt_group,False):
            global goomba_bye
            self.image = image.load('assets/ouch.png')
            mixer.Sound.play(ouchs)
        # global keys, fireball
        keys=key.get_pressed()
        
        if fireball_set==1 and keys[K_LCTRL] | keys[K_LSHIFT] and time_set==1:
            fireball=Fireball(self.rect.centerx,self.rect.centery,self.direction)
            fireball_group.add(fireball)
            time_set=0
            # goomba_bye+=1
        # if self.rect.collidepoint(goomba.rect.centerx,goomba.rect.top):
        #     goomba.kill()
        #     print('ouch')
        # if goomba_bye==0:
        #     if self.rect.collidepoint(goomba.rect.left,goomba.rect.centery) or self.rect.collidepoint(goomba.rect.right,goomba.rect.centery):
        #         # goomba.kill()
        #         self.image = image.load('assets/ouch.png')
        #         mixer.Sound.play(ouchs)
        #         # display.update()
        #         # time.delay(5000)
        #         self.kill()
        bricks=sprite.spritecollide(self,obstacle_group,False)        
        for w in bricks:
                self.rect.bottom = w.rect.top
                self.fall_speed=2
                self.on_ground=True
        keys = key.get_pressed()
        if fire==0:
            mari=0
            mm=0
            # global mari, mm
            mari='assets/mario1.png'
            mm='assets/mario1-left.png'
        if fire==1:
            # global mari, mm
            mari='assets/fire_mario.png'
            mm='assets/fire_mario-left.png'
            fire=3
            transform.scale(self.image,(36,60))
        if move == 0:
            if keys[K_RIGHT]:
                    if self.direction != 'right':
                        self.image = image.load(mari)
                        self.direction='right'
                        self.image = transform.scale(self.image,(self.mx,self.my))
                    else:
                        self.rect.x += 10
            if keys[K_LEFT]:
                    if self.direction != 'left':
                        self.image = image.load(mm)
                        self.direction='left'
                        self.image = transform.scale(self.image,(self.mx,self.my))
                        self.rect.update(self.rect.x,self.rect.y,self.mx,self.my)
                    else:
                        self.rect.x -= 10
        if move==1:
            if keys[K_RIGHT]:
                if self.direction != 'right':
                            self.image = image.load(mari)
                            self.direction='right'
                            self.image = transform.scale(self.image,(self.mx,self.my))
            if keys[K_LEFT]:
                if self.direction != 'left':
                        self.image = image.load(mm)
                        self.direction='left'
                        self.image = transform.scale(self.image,(self.mx,self.my))
                        self.rect.update(self.rect.x,self.rect.y,self.mx,self.my)
        
        bricks=sprite.spritecollide(self,obstacle_group,False)        
        for w in bricks:
            if self.direction == 'left':
                self.rect.left = w.rect.right
            if self.direction == 'right':
                self.rect.right = w.rect.left
        if self.on_ground == True:
            if keys[K_UP]:
                        self.direction='up'
                        self.rect.y-=80
                        mixer.Sound.play(jump)
                        self.on_ground = False
                        
    #     if self.make_jump:
    #         self.jump()
    #         bricks=sprite.spritecollide(self,obstacle_group,False)        
    #         for w in bricks:
    #             if self.direction == 'up':
    #                 self.rect.bottom = w.rect.top
    #                 self.make_jump = False
    def jump(self):
        global jump_count
        if jump_count>=-30:
            self.rect.y-=jump_count/2
            jump_count-=3
        else:
            jump_count=30
            self.make_jump=False

firework_group = sprite.Group()
stair_group = sprite.Group()
castle_group = sprite.Group()
fireball_group = sprite.Group()
fquestion_group = sprite.Group()
flower_group = sprite.Group()
testing_group = sprite.Group()
goomba_group = sprite.Group()
mushroom_group = sprite.Group()
obstacle_group = sprite.Group()
ground_group = sprite.Group()
question_group = sprite.Group()
mario_group = sprite.Group()
coin_group = sprite.Group()
tnt_group = sprite.Group()
# fireball_group.upload()
# mario_group.
size=30
x=0
y=0
for ro in map:
    for s in ro:
        if s == '-':
            ground = Ground(x,y,0)
            obstacle_group.add(ground)
            ground_group.add(ground)

        if s == '=':
            ground = Ground(x,y,1)
            obstacle_group.add(ground)
            ground_group.add(ground)
        if s == '?':
            question = Question(x,y)
            question_group.add(question)
        
        if s == '.':
            brick = Brick(x,y)
            obstacle_group.add(brick)
            ground_group.add(brick)
        if s == 'm':
            mario = Mario(x,y-10)
            mario_group.add(mario)
        if s == 't':
            tnt = Tnt(x,y)
            tnt_group.add(tnt)
        if s == 'g':
            goomba = Goomba(x,y)
            goomba_group.add(goomba)
        if s == 'u':
            mquestion = Mquestion(x,y)
            question_group.add(mquestion)
        if s == 'f':
            fquestion = Fquestion(x,y)
            question_group.add(fquestion)
        if s == 'b':
            barrier = Barrier(x,y)
            obstacle_group.add(barrier)
        if s == 'c':
            castle = Castle(x,y)
            castle_group.add(castle)
        if s == 's':
            stair = Stair(x,y)
            obstacle_group.add(stair)
        if s == '#':
            fbarrier = Fbarrier(x,y)
            testing_group.add(fbarrier)
        x+=size
    x=0
    y+=size
size_window = (width, height)
window = display.set_mode(size_window)
display.set_caption('Mario')
run=True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    window.fill(mario_blue)
    # print(fire_time1)
    if game==1:
        testing_group.update()
        castle_group.update()
        stair_group.update()
        question_group.update()
        coin_group.update()
        obstacle_group.update()
        mushroom_group.update()
        tnt_group.update()
        goomba_group.update()
        flower_group.update()
        # coin_group.update()
        mario_group.update()
        # question_group.update()

    if game==1 or game==3:
        
        tnt_group.draw(window)
        flower_group.draw(window)
        obstacle_group.draw(window)
        ground_group.draw(window)
        mushroom_group.draw(window)
        question_group.draw(window)
        coin_group.draw(window)
        goomba_group.draw(window)
        castle_group.draw(window)
        fireball_group.draw(window)
        stair_group.draw(window)
        mario_group.draw(window)
        firework_group.draw(window)
        fireball_group.update()
        # Fireball.upload(fireball_group)
        keys = key.get_pressed()
        if keys[K_RIGHT] and mario.rect.x >= width/2:
            move==1

    if game==3:
        # print('test')
        # fireball_group.()
        # Fireball.kill
        # time.delay(1000)
        mixer.music.fadeout(1000)
        firework=image.load('assets/fireworks.png')
        window.blit(firework, (width//2-150, 30))
        mixer.Sound.play(win)
        text('YOU WIN!', width/2-250, height/2-100, 'green', 100)
        display.update()
        time.delay(16000)
        run=False
    
    if game==0:
        mixer.music.fadeout(1000)
        mixer.Sound.play(end)
        text('GAME OVER', width/2-250, height/2-100, 'red', 100)
        display.update()
        time.delay(5500)
        run=False
    
    display.update()
    time.delay(50)
    

quit()
