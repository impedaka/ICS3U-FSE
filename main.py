from utils import * #import settings
from os import path #find local files
mixer.init()

#since im relitively new to classes, i got a bit of help from the internet
class Player(sprite.Sprite): #pygame sprite class
    def __init__(self, screen): #initialize sprite class
        super().__init__()
        #self.import_character_assets()
        
        #dust particles
        #.convert_alpha doesnt make game laggy, got helped from internet
        dustRun1=image.load('resources/assets/player/dust_particles/run/run_1.png').convert_alpha()
        dustRun2=image.load('resources/assets/player/dust_particles/run/run_2.png').convert_alpha()
        dustRun3=image.load('resources/assets/player/dust_particles/run/run_3.png').convert_alpha()
        dustRun4=image.load('resources/assets/player/dust_particles/run/run_4.png').convert_alpha()
        dustRun5=image.load('resources/assets/player/dust_particles/run/run_5.png').convert_alpha()
        self.dustIndex = 0
        self.display_surface = screen
        self.dustIndexRun=[dustRun1, dustRun2, dustRun3, dustRun4, dustRun5]
        #player animation
        player1=image.load('resources/assets/player/run/player-run-1.png').convert_alpha()
        player2=image.load('resources/assets/player/run/player-run-2.png').convert_alpha()
        player3=image.load('resources/assets/player/run/player-run-3.png').convert_alpha()
        player4=image.load('resources/assets/player/run/player-run-4.png').convert_alpha()
        player5=image.load('resources/assets/player/run/player-run-5.png').convert_alpha()
        player6=image.load('resources/assets/player/run/player-run-6.png').convert_alpha()
        self.playerWalk=[player1,player2,player3,player4,player5,player6]
        #self. = attributes of the same object/class
        self.playerIndex=0
        for i in range(6):
            self.playerWalk[i] = transform.scale(self.playerWalk[i],(84,84)) #resize all of the frames in the list
    
        playerJump=image.load('resources/assets/player/jump/player-jump-1.png').convert_alpha()
        self.playerJump=transform.scale(playerJump, (84,84))

        #image=image displayed
        self.image=self.playerWalk[self.playerIndex] #what will be displayed will depend on the playerIndex value
        self.rect = self.image.get_rect(midbottom = (80, 300)) #rect=location
        self.gravity=0
    #def DustParticles(self):
    #    self.dustJump = import_folder('resources/assets/player/dust_particles/jump')
    def PlayerInput(self): #player control method
        keys = key.get_pressed()
        if keys[K_SPACE] and self.rect.bottom >=300: #touch ground and space key pressed
            self.gravity = -20 #'jump' or go against gravity
            jumpSound.play() #plays sound

    def Gravity(self):
        self.gravity+=1
        self.rect.y +=self.gravity #by default, player rect y will always be 300
        if self.rect.bottom>=300:
            self.rect.bottom=300 #player will always be above ground

    def PlayerAnimation(self):
        if self.rect.bottom<300: #jump is player is in air
            self.image=self.playerJump
        else: #walking animation when on floor
            self.playerIndex+=0.2 #animation frame rate speed
            if self.playerIndex>=len(self.playerWalk):
                self.playerIndex=0 #after the last frame, go to the first frame
            self.image = self.playerWalk[int(self.playerIndex)] #player will be updated with different frames
    def RunDustAnimation(self):
        if self.rect.bottom==300: #only show animation while running on ground
            self.dustIndex+=0.2
            if self.dustIndex>=len(self.dustIndexRun):
                self.dustIndex=0
            dustParticle = self.dustIndexRun[int(self.dustIndex)]
            pos  = self.rect.bottomleft - math.Vector2(6, 10) #adjust position (got helped with this)
            self.display_surface.blit(dustParticle, pos)
            
    def update(self): #controls sprite actions by calling the methods
        self.PlayerInput()
        self.Gravity()
        self.PlayerAnimation()
        self.RunDustAnimation()

class Obstacle(sprite.Sprite):

    def __init__(self, type): #type argument for either sky or ground enemy
        super().__init__()
        if type=='opossum':
            enemy1=image.load('resources/assets/opossum/opossum-1.png').convert_alpha()
            enemy2=image.load('resources/assets/opossum/opossum-2.png').convert_alpha()
            enemy3=image.load('resources/assets/opossum/opossum-3.png').convert_alpha()
            enemy4=image.load('resources/assets/opossum/opossum-4.png').convert_alpha()
            enemy5=image.load('resources/assets/opossum/opossum-5.png').convert_alpha()
            enemy6=image.load('resources/assets/opossum/opossum-6.png').convert_alpha()
            self.frames=[enemy1,enemy2,enemy3,enemy4,enemy5,enemy6]

            for i in range(6):
                self.frames[i]=transform.scale(self.frames[i], (72,56))

            yPosition=300 #spawn on ground
        else: #eagle
            skyEnemy1=image.load('resources/assets/eagle/eagle-attack-1.png').convert_alpha()
            skyEnemy2=image.load('resources/assets/eagle/eagle-attack-2.png').convert_alpha()
            skyEnemy3=image.load('resources/assets/eagle/eagle-attack-3.png').convert_alpha()
            skyEnemy4=image.load('resources/assets/eagle/eagle-attack-4.png').convert_alpha()
            self.frames=[skyEnemy1,skyEnemy2,skyEnemy3,skyEnemy4]  

            for i in range(4):
                self.frames[i]=transform.scale(self.frames[i], (84,60))

            yPosition=200 #spawn in sky
            
        self.animationIndex=0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), yPosition)) #randomly spawn between x 900 and 1100

    def EnemyAnimation(self):
        self.animationIndex+=0.2 #animation frame rate speed
        if self.animationIndex>=len(self.frames):
           self.animationIndex=0 #after the last frame, go to the first frame
        self.image = self.frames[int(self.animationIndex)] 

    def update(self):
        self.EnemyAnimation()
        self.rect.x -=gameSpeed #always move to the left
        self.CleanUp()

    def CleanUp(self):
        if self.rect.x <= -100: #when you can no longer see the sprite
            self.kill() #remove sprite from groups to save memory
 
def displayScore(): #displaying score
    currentTime = time.get_ticks() // 1000 - startTime #score goes up per second and if you start a new game, score is set to 0
    score = test_font.render(f'{currentTime}',False,DARKPURPLE)
    scoreRect = score.get_rect(center = (400,50))
    screen.blit(score,scoreRect)
    return currentTime

def PlayerCollision():
    if sprite.spritecollide(foxPlayer.sprite, obstacleGroup, False): #if player and obstacle are colliding, obstacle will not be deleted (False)
        obstacleGroup.empty() #deletes obstacles in group so that you don't die as soon as you spawn
        deathSound.play()
        return False #game active false
    else:
        return True
#got helped with this
dir=path.dirname(__file__)
with open(path.join(dir, highScoreFile), 'w') as f: #read and write file
    try:
        highscore = int(f.read())
    except: #if theres an error
        highscore = 0

jumpSound=mixer.Sound('resources/audio/jump.wav')
test_font=font.Font("resources/fonts/Pixeltype.ttf", 50) #using this font
deathSound=mixer.Sound('resources/audio/die.wav')
mixer.music.load('resources/audio/music.ogg')
mixer.music.play(-1)
foxPlayer = sprite.GroupSingle() #container which holds single sprite
foxPlayer.add(Player(screen)) #makes player class part a part of groupsingle()

obstacleGroup=sprite.Group() #holdes sprite class

sky=image.load('resources/assets/sky.png').convert_alpha()
background=transform.scale(sky, (800,400))

ground=image.load('resources/assets/ground.png').convert_alpha()
platform=transform.scale(ground, (800, 100))
bgimg=image.load('resources/assets/bg.png').convert_alpha()
bg=transform.scale(bgimg, (800,400))

#intro screen
gameName=image.load('resources/assets/title.png').convert_alpha()
gameNameRect=gameName.get_rect(center=(400,150))
gameMessage = transform.scale(image.load("resources/assets/press-enter.png").convert_alpha(), (205, 30))
gameMessageRect=gameMessage.get_rect(center=(400,320))

#timer
obstacleTimer=USEREVENT+1 #custom event
time.set_timer(obstacleTimer, 1500) #trigger event every x time
x=0 #platform coordinates
gameSpeed = 6 #default game speed
while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==KEYDOWN and evt.key == K_w:
            mixer.music.fadeout(1000) #no music
        if evt.type==KEYDOWN and evt.key == K_e:
            mixer.music.play(-1) #loops music
        if gameActive == True:
            if evt.type==obstacleTimer: #when the event is triggered
                #higher change of opossums spawning
                obstacleGroup.add(Obstacle(choice(['eagle', 'opossum', 'opossum', 'opossum']))) #choice randomly choses item from list
        else:
            if evt.type==KEYDOWN and evt.key==K_SPACE:
                gameActive=True #start game with space bar
                startTime=(time.get_ticks()//1000)
    if gameActive: #gameActive is true 
        relX= x% platform.get_rect().width
        screen.blit(background, (0,0))      
        screen.blit(platform, (relX - platform.get_rect().width,300)) #moving platform
        if relX < platform.get_rect().width:
            screen.blit(platform, (relX, 300)) #covers the entire screen by bliting another image at tne end
        x-=gameSpeed #pace moves with teh game
        score=displayScore() #call score function

        gameSpeed = (score // 5) +6 #higher score=faster speed
        foxPlayer.draw(screen) #draw sprites from player groupSingle
        foxPlayer.update() #update sprites with update method
        obstacleGroup.draw(screen)
        obstacleGroup.update()
        gameActive = PlayerCollision() #true or false

    else:
        if score > highscore: #update highscore file
            highscore = score
            with open(path.join(dir, highScoreFile), 'w') as f:
                f.write(str(score)) 
        screen.blit(bg, (0,0))
        screen.blit(gameName, gameNameRect) #title game
        scoreMessage=test_font.render(f'Score: {score}', False, DARKPURPLE)
        scoreMessageRect=scoreMessage.get_rect(center=(400,330))
        highScoreMessage=test_font.render(f'Highscore: {highscore}', False, DARKPURPLE)
        highScoreMessageRect=highScoreMessage.get_rect(center=(400,300))
        if score == 0: 
            screen.blit(bg, (0,0))
            screen.blit(gameMessage, gameMessageRect)
            screen.blit(gameName, gameNameRect) #title game
        else: 
            screen.blit(scoreMessage,scoreMessageRect) #message after playing game
            screen.blit(highScoreMessage, highScoreMessageRect)
    clock.tick(60) #frames per second
    display.flip()
            
quit()
