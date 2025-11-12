import asyncio
import os
import sys
from pygame import *
from random import *

# --- PyScript Boilerplate ---
# This code tells Pygame to draw inside the HTML element
# that the <py-script> tag is targeting.
target_id = os.environ.get("PYGAME_TARGET", "game-container")
os.environ['SDL_AUDIODRIVER'] = 'sdl2'
os.environ['SDL_VIDEO_DRIVER'] = 'emscripten'
os.environ['PYGAME_DISPLAY'] = f'#{target_id}'

# We must initialize the display module *before* set_mode is called
# so it can read the environment variable.
display.init()
# --- End of PyScript Boilerplate ---

def text(window, message,x,y,font_color,font_size, font_type='assets/font.otf'):
        font_type=font.Font(font_type,font_size)
        text=font_type.render(message,True,font_color)
        window.blit (text, (x,y))

# All classes (Ground, Castle, Mario, etc.) remain unchanged
# ... (all your original class definitions go here) ...
# I am copying them here for a complete file.

class  Ground (sprite.Sprite):
    def __init__(self, x,y,id):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/ground.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.id = id
    def update(self, mario_move, keys):
        if keys[K_RIGHT] and mario_move==1:
            self.rect.x-=10
        if keys[K_LEFT] and mario_move==1:
            mario_move=0

class  Castle (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/mario-castle.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self, mario_move, keys):
        if keys[K_RIGHT] and mario_move==1:
            self.rect.x-=10
        if keys[K_LEFT] and mario_move==1:
            mario_move=0

class  Stair (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/stair.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self, mario_move, keys):
        if keys[K_RIGHT] and mario_move==1:
            self.rect.x-=10
        if keys[K_LEFT] and mario_move==1:
            mario_move=0

class  Fireball (sprite.Sprite):
    def __init__(self, x,y,dir):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/fireball.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.direction=dir
        self.fall_speed = 2
        self.on_ground = False
    
    # Removed the 'upload' method as it wasn't being used
    # and was causing a 'no_fire' NameError.

    def update(self, no_fire, ground_group):
        self.rect.y+=self.fall_speed
        self.fall_speed+=0.5
        bricks=sprite.spritecollide(self,ground_group,False)
        for w in bricks:
                self.rect.bottom = w.rect.top
                self.fall_speed=2
                self.on_ground=True
        if self.on_ground==True:
            self.rect.y-=40
            self.on_ground=False
        if self.direction=='right':
            self.rect.x+=5
        else:
            self.rect.x-=5
        if no_fire==1:      
            self.kill() # Corrected from self.kill to self.kill()
    
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
    def update(self, mario_move, keys):
        if keys[K_RIGHT] and mario_move==1:
            self.rect.x-=10
        if keys[K_LEFT] and mario_move==1:
            mario_move=0

class  Flower (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/fire_flower.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    
    # Passing global state into update
    def update(self, mario_move, keys, mario_group):
        if keys[K_RIGHT] and mario_move==1:
            self.rect.x-=10
        if keys[K_LEFT] and mario_move==1:
            mario_move=0
        if sprite.spritecollide(self, mario_group, False):
            self.kill()
            return 1 # Return 1 to set fire=1
        return 0

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
    
    # Passing global state into update
    def update(self, mario_move, keys, ground_group, mario, fireball_group, obstacle_group, bye):
        if keys[K_RIGHT] and mario_move==1:
            self.rect.x-=10
        if keys[K_LEFT] and mario_move==1:
            mario_move=0
        
        self.rect.y+=self.fall_speed
        self.fall_speed+=0.5
        bricks=sprite.spritecollide(self,ground_group,False)
        for w in bricks:
                if w.id==0:
                    self.rect.bottom = w.rect.top
                    self.fall_speed = 0
        
        # Return codes to update game state
        # 1 = goomba destroyed, 2 = mario destroyed
        if mario.rect.collidepoint(self.rect.centerx,self.rect.top) or sprite.spritecollide(self, fireball_group, True):
            self.kill()
            mixer.Sound.play(bye) # 'bye' needs to be in scope
            return 1 
        elif mario.rect.collidepoint(self.rect.left,self.rect.centery) or mario.rect.collidepoint(self.rect.right,self.rect.centery):
            mario.image = image.load('assets/ouch.png')
            mario.kill()
            return 2 

        if abs(self.rect.x-mario.rect.x)<20*30:
            if sprite.spritecollide(self,obstacle_group,False):
                if self.direction==-3:
                    self.direction=3
                else:
                    self.direction=-3
            self.rect.x+= self.direction
        return 0

class  Mushroom (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/mushroom.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self, mario_move, keys):
        if keys[K_RIGHT] and mario_move==1:
            self.rect.x-=10
        if keys[K_LEFT] and mario_move==1:
            mario_move=0

class  Fquestion (sprite.Sprite):
    def __init__(self, x,y, flower_group): # Pass group in
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/question.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.state = True
        self.id = randint(1,2)
        self.flower_group = flower_group # Store group
        
    def update(self, mario_move, keys, mario, obstacle_group):
        if self.state==True:
            if keys[K_RIGHT] and mario_move==1:
                self.rect.x-=10
            if keys[K_LEFT] and mario_move==1:
                mario_move=0
        if self.state==False:
            if keys[K_RIGHT] and mario_move==1:
                self.rect.x-=5
        
        # Check collision with Mario's *head*
        if self.state and self.rect.colliderect(mario.rect) and mario.rect.top < self.rect.bottom and mario.fall_speed < 0:
            flower = Flower(self.rect.centerx,self.rect.top-13)
            self.flower_group.add(flower)
            self.image = image.load('assets/empty.png')
            self.state = False
            obstacle_group.add(self)

class  Question (sprite.Sprite):
    def __init__(self, x,y, coin_group): # Pass group in
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/question.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.state = True
        self.id = randint(1,2)
        self.coin_group = coin_group # Store group

    def update(self, mario_move, keys, mario, obstacle_group):
        if self.state==True:
            if keys[K_RIGHT] and mario_move==1:
                self.rect.x-=10
            if keys[K_LEFT] and mario_move==1:
                mario_move=0
        if self.state==False:
            if keys[K_RIGHT] and mario_move==1:
                self.rect.x-=5
        
        # Check collision with Mario's *head*
        if self.state and self.rect.colliderect(mario.rect) and mario.rect.top < self.rect.bottom and mario.fall_speed < 0:
            coin = Coin(self.rect.centerx,self.rect.top-13)
            self.coin_group.add(coin)
            self.image = image.load('assets/empty.png')
            self.state = False
            obstacle_group.add(self)
            
class  Mquestion (sprite.Sprite):
    def __init__(self, x,y, mushroom_group): # Pass group in
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/question.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.state = True
        self.id = randint(1,2)
        self.mushroom_group = mushroom_group # Store group

    def update(self, mario_move, keys, mario, obstacle_group):
        if self.state==True:
            if keys[K_RIGHT] and mario_move==1:
                self.rect.x-=10
            if keys[K_LEFT] and mario_move==1:
                mario_move=0
        if self.state==False:
            if keys[K_RIGHT] and mario_move==1:
                self.rect.x-=5
        
        # Check collision with Mario's *head*
        if self.state and self.rect.colliderect(mario.rect) and mario.rect.top < self.rect.bottom and mario.fall_speed < 0:
            mushroom = Mushroom(self.rect.centerx,self.rect.top-13)
            self.mushroom_group.add(mushroom)
            self.image = image.load('assets/empty.png')
            self.state = False
            obstacle_group.add(self)

class  Brick (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/mario-brick.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.id = 0
    def update(self, mario_move, keys):
        if keys[K_RIGHT] and mario_move==1:
            self.rect.x-=10
        if keys[K_LEFT] and mario_move==1:
            mario_move=0

class  Tnt (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/tnt.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self, mario_move, keys):
        if keys[K_RIGHT] and mario_move==1:
            self.rect.x-=10
        if keys[K_LEFT] and mario_move==1:
            mario_move=0

class  Coin (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/coin2.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    
    # Passing global state into update
    def update(self, mario_move, keys, mario_group, csound):
        if keys[K_RIGHT] and mario_move==1:
            self.rect.x-=10
        if keys[K_LEFT] and mario_move==1:
            mario_move=0
        
        if sprite.spritecollide(self, mario_group, False):
            self.kill()
            mixer.Sound.play(csound)
            return 1 # Return 1 to increment score
        return 0

class  Mario (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/mario1.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.direction = 'down' # Start facing right
        self.make_jump = False
        self.fall_speed = 2
        self.on_ground = False
        self.mx=36
        self.my=48
        self.fire = 0 # Use internal state
        self.mari_img = image.load('assets/mario1.png')
        self.mm_img = image.load('assets/mario1-left.png')
        self.fire_mari_img = image.load('assets/fire_mario.png')
        self.fire_mm_img = image.load('assets/fire_mario-left.png')
        
    def update(self, keys, testing_group, fquestion_group, mushroom_group, tnt_group, 
             obstacle_group, fireball_group, jump_sound, power_sound, ouchs_sound, height, width):
        
        mario_move = 0
        no_fire = 0
        game_state = 1 # 1=playing, 3=win, 0=lose
        fireball_set = 0
        
        if sprite.spritecollide(self, testing_group, False):
            no_fire=1
            fireball_group.empty()
            game_state=3
        if self.rect.y >= height:
            game_state=0
        
        if sprite.spritecollide(self, fquestion_group, False):
            no_fire=1
        
        if self.rect.centerx >= width/2:
            mario_move=1
        if keys[K_LEFT] and mario_move==1:
            mario_move=0
        
        if self.fire > 0:
            fireball_set = 1

        self.rect.y+=self.fall_speed
        self.fall_speed+=0.5

        if sprite.spritecollide(self,mushroom_group,True):
            mixer.Sound.play(power_sound)
            if self.fire == 0: # Only grow if small
                self.mx=36
                self.my=60
                self.image = transform.scale(self.image,(self.mx,self.my))

        if sprite.spritecollide(self,tnt_group,False):
            self.image = image.load('assets/ouch.png')
            mixer.Sound.play(ouchs_sound)
            # Add game over logic here
            game_state = 0

        bricks=sprite.spritecollide(self,obstacle_group,False)        
        for w in bricks:
            # Check for vertical collision
            if self.fall_speed > 0 and self.rect.bottom > w.rect.top and self.rect.top < w.rect.top:
                self.rect.bottom = w.rect.top
                self.fall_speed = 0 # Stop falling
                self.on_ground = True
            # Check for head collision
            elif self.fall_speed < 0 and self.rect.top < w.rect.bottom and self.rect.bottom > w.rect.bottom:
                self.rect.top = w.rect.bottom
                self.fall_speed = 2 # Start falling down
        
        # Horizontal movement and image flipping
        if keys[K_RIGHT]:
            if self.direction != 'right':
                self.direction='right'
                img_to_load = self.fire_mari_img if self.fire > 0 else self.mari_img
                self.image = transform.scale(img_to_load,(self.mx,self.my))
            
            if mario_move == 0:
                self.rect.x += 10
                
        elif keys[K_LEFT]:
            if self.direction != 'left':
                self.direction='left'
                img_to_load = self.fire_mm_img if self.fire > 0 else self.mm_img
                self.image = transform.scale(img_to_load,(self.mx,self.my))
            
            if mario_move == 0:
                self.rect.x -= 10
        
        # Horizontal collision
        bricks=sprite.spritecollide(self,obstacle_group,False)        
        for w in bricks:
            if self.direction == 'left' and self.rect.left < w.rect.right and self.rect.right > w.rect.right:
                self.rect.left = w.rect.right
            if self.direction == 'right' and self.rect.right > w.rect.left and self.rect.left < w.rect.left:
                self.rect.right = w.rect.left

        # Jumping
        if self.on_ground == True:
            if keys[K_UP]:
                        self.fall_speed = -15 # Apply upward velocity
                        mixer.Sound.play(jump_sound)
                        self.on_ground = False
        
        # Return all state changes
        return mario_move, no_fire, game_state, fireball_set, self.direction

    def set_fire(self):
        self.fire = 1
        self.mx = 36
        self.my = 60
        img_to_load = self.fire_mari_img if self.direction == 'right' else self.fire_mm_img
        self.image = transform.scale(img_to_load, (self.mx, self.my))

# This is the main function that PyScript will run
async def main():
    
    # --- Put ALL setup code inside main() ---
    init()
    fireball_set=0
    move=0
    no_fire=0
    
    # Load sounds (ensure paths are correct)
    try:
        mixer.music.load('assets/mario-theme.ogg')
        mixer.music.play(-1)
        mixer.music.set_volume(0.1)
        ouchs=mixer.Sound('assets/ouchs.ogg')
        bye=mixer.Sound('assets/goomba-destroy.ogg')
        end=mixer.Sound('assets/mario-end.ogg') 
        jump_sound=mixer.Sound('assets/stomp.ogg')
        csound=mixer.Sound('assets/coin-sound.ogg') 
        power=mixer.Sound('assets/power-up.ogg')
        win=mixer.Sound('assets/mario-win.ogg')
    except Exception as e:
        print(f"Error loading sounds: {e}")
        print("Continuing without sound...")
        # Create dummy sound objects
        class DummySound:
            def play(self): pass
        ouchs = bye = end = jump_sound = csound = power = win = DummySound()
        
    game=1
    time_set=0
    fire_time1=time.get_ticks()
    fire_time2=time.get_ticks()

    jump_count=30
    score = 0
    goomba_bye=0
    
    # Define colors
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    white = (255,255,255)
    mario_blue = (116,147,246)
    
    # Set dimensions
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

    # Create sprite groups
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
    
    # Map Parsing
    size=30
    x=0
    y=0
    mario = None # Define mario before loop
    
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
                question = Question(x,y, coin_group) # Pass group
                question_group.add(question)
            if s == '.':
                brick = Brick(x,y)
                obstacle_group.add(brick)
                ground_group.add(brick)
            if s == 'm':
                mario = Mario(x,y-10) # Assign mario
                mario_group.add(mario)
            if s == 't':
                tnt = Tnt(x,y)
                tnt_group.add(tnt)
            if s == 'g':
                goomba = Goomba(x,y)
                goomba_group.add(goomba)
            if s == 'u':
                mquestion = Mquestion(x,y, mushroom_group) # Pass group
                question_group.add(mquestion)
            if s == 'f':
                fquestion = Fquestion(x,y, flower_group) # Pass group
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
        
    if mario is None:
        print("Error: No 'm' (Mario) found in map!")
        return # Exit if no Mario

    # Set up the display
    size_window = (width, height)
    window = display.set_mode(size_window)
    display.set_caption('Mario')
    
    # Add a clock
    clock = time.Clock()
    
    firework = image.load('assets/fireworks.png')

    run=True
    while run:
        # --- Event Loop ---
        for e in event.get():
            if e.type == QUIT:
                run = False
        
        # Get key presses
        keys = key.get_pressed()

        # --- Game Logic ---
        if game==1:
            # Update Mario and get state changes
            mario_move, no_fire, game_state, fireball_set, mario_direction = mario.update(keys, testing_group, fquestion_group, mushroom_group, 
                                                               tnt_group, obstacle_group, fireball_group, 
                                                               jump_sound, power, ouchs, height, width)
            game = game_state # Update game state from Mario
            
            # Pass state into other updates
            testing_group.update(mario_move, keys)
            castle_group.update(mario_move, keys)
            stair_group.update(mario_move, keys)
            
            # These updates need Mario's position
            question_group.update(mario_move, keys, mario, obstacle_group)

            for coin in coin_group:
                score += coin.update(mario_move, keys, mario_group, csound)

            obstacle_group.update(mario_move, keys)
            mushroom_group.update(mario_move, keys)
            tnt_group.update(mario_move, keys)
            
            for goomba in goomba_group:
                goomba_result = goomba.update(mario_move, keys, ground_group, mario, fireball_group, obstacle_group, bye)
                if goomba_result == 1:
                    goomba_bye += 1
                elif goomba_result == 2:
                    if game != 0: # Only play sound once
                        mixer.Sound.play(ouchs)
                        game = 0 # Mario is hit
                        sound = 1
            
            for flower in flower_group:
                if flower.update(mario_move, keys, mario_group):
                    mario.set_fire() # Tell mario to be fire mario
            
            fireball_group.update(no_fire, ground_group)

            # Fireball logic
            fire_time2=time.get_ticks()
            if fire_time2-fire_time1>=500:
                time_set=1
                fire_time1=fire_time2
            
            if fireball_set==1 and (keys[K_LCTRL] or keys[K_LSHIFT]) and time_set==1:
                fireball=Fireball(mario.rect.centerx,mario.rect.centery, mario_direction)
                fireball_group.add(fireball)
                time_set=0

        # --- Drawing ---
        window.fill(mario_blue)
        
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
        
        # --- Game State Screens ---
        if game==3:
            mixer.music.fadeout(1000)
            window.blit(firework, (width//2-150, 30))
            try:
                mixer.Sound.play(win)
            except: pass
            text(window, 'YOU WIN!', width/2-250, height/2-100, green, 100)
            display.update()
            
            # Replaced time.delay with asyncio.sleep
            await asyncio.sleep(16.0) 
            run=False
        
        if game==0:
            mixer.music.fadeout(1000)
            try:
                mixer.Sound.play(end)
            except: pass
            text(window, 'GAME OVER', width/2-250, height/2-100, red, 100)
            display.update()
            
            # Replaced time.delay with asyncio.sleep
            await asyncio.sleep(5.5) 
            run=False
        
        # --- Final Update and Loop Control ---
        display.update()
        
        # Replaced time.delay(50)
        await asyncio.sleep(0) # This is CRITICAL: gives control back to the browser
        clock.tick(30) # Aim for 30 frames per second
        
    quit()
    sys.exit() # Ensure the script fully exits

# This line runs the main function when PyScript loads the file
asyncio.run(main())


