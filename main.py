from utils import * #import settings
from os import path #find local files

mixer.init()
count=0
class Player(sprite.Sprite): #pygame sprite class

    def __init__(self): #initialize sprite class
        super().__init__()
        player1=image.load('resources/assets/player/run/player-run-1.png')
        player2=image.load('resources/assets/player/run/player-run-2.png')
        player3=image.load('resources/assets/player/run/player-run-3.png')
        player4=image.load('resources/assets/player/run/player-run-4.png')
        player5=image.load('resources/assets/player/run/player-run-5.png')
        player6=image.load('resources/assets/player/run/player-run-6.png')
        self.playerWalk=[player1,player2,player3,player4,player5,player6]
        #self. = attributes of the same object/class
        self.playerIndex=0
        for i in range(6):
            self.playerWalk[i] = transform.scale(self.playerWalk[i],(84,84)) #resize all of the frames in the list
    
        playerJump=image.load('resources/assets/player/jump/player-jump-1.png')
        self.playerJump=transform.scale(playerJump, (84,84))

        #image=image displayed
        self.image=self.playerWalk[self.playerIndex] #what will be displayed will depend on the playerIndex value
        self.rect = self.image.get_rect(midbottom = (80, 300)) #rect=location
        self.gravity=0
 
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

    def update(self): #controls sprite actions by calling the methods
        self.PlayerInput()
        self.Gravity()
        self.PlayerAnimation()

class Obstacle(sprite.Sprite):

    def __init__(self, type): #type argument for either sky or ground enemy
        super().__init__()
        if type=='opossum':
            enemy1=image.load('resources/assets/opossum/opossum-1.png')
            enemy2=image.load('resources/assets/opossum/opossum-2.png')
            enemy3=image.load('resources/assets/opossum/opossum-3.png')
            enemy4=image.load('resources/assets/opossum/opossum-4.png')
            enemy5=image.load('resources/assets/opossum/opossum-5.png')
            enemy6=image.load('resources/assets/opossum/opossum-6.png')
            self.frames=[enemy1,enemy2,enemy3,enemy4,enemy5,enemy6]

            for i in range(6):
                self.frames[i]=transform.scale(self.frames[i], (72,56))

            yPosition=300 #spawn on ground
        else: #eagle
            skyEnemy1=image.load('resources/assets/eagle/eagle-attack-1.png')
            skyEnemy2=image.load('resources/assets/eagle/eagle-attack-2.png')
            skyEnemy3=image.load('resources/assets/eagle/eagle-attack-3.png')
            skyEnemy4=image.load('resources/assets/eagle/eagle-attack-4.png')
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
        self.rect.x -=8 #always move to the left
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

def PlayerCollision(count):
    if sprite.spritecollide(foxPlayer.sprite, obstacleGroup, False):
        #obstacleGroup.empty() #deletes obstacles in group so that you don't die as soon as you spawn
        deathSound.play()
        count +=1
        print(count)
        time.sleep(2)
        return False #game active
    else:
        return True


dir=path.dirname(__file__)
with open(path.join(dir, highScoreFile), 'w') as f: #read and write file
    try:
        highscore = int(f.read())
    except: #if theres an error
        highscore = 0

jumpSound=mixer.Sound('resources/audio/jump.wav')
test_font=font.Font("resources/fonts/Pixeltype.ttf", 50) #using this font
bgMusic=mixer.Sound('resources/audio/music.ogg')
bgMusic.play(loops = -1) #forever loop background music
deathSound=mixer.Sound('resources/audio/die.wav')

foxPlayer = sprite.GroupSingle() #container which holds single sprite
foxPlayer.add(Player()) #makes player class part a part of groupsingle()

obstacleGroup=sprite.Group() #holdes sprite class

sky=image.load('resources/assets/sky.png')
background=transform.scale(sky, (800,400))

ground=image.load('resources/assets/ground.png')
platform=transform.scale(ground, (800, 100))
x=0
bgimg=image.load('resources/assets/bg.png')
bg=transform.scale(bgimg, (800,400))

#player
idleFox=image.load('resources/assets/player/idle/player-idle-1.png')
idleFox=transform.scale(idleFox, (175,175))
idleRect=idleFox.get_rect(center=(400,175))

#intro screen
#gameName=test_font.render('Fox Runner', False, DARKPURPLE)
gameName=image.load('resources/assets/title.png')
gameNameRect=gameName.get_rect(center=(400,150))
#gameMessage=test_font.render('Press space to start', False, DARKPURPLE)
gameMessage = transform.scale(image.load("resources/assets/press-enter.png"), (205, 30))
gameMessageRect=gameMessage.get_rect(center=(400,320))

#timer
obstacleTimer=USEREVENT+1 #custom event
time.set_timer(obstacleTimer, 1500) #trigger event every x time

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
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
         screen.blit(platform, (relX - platform.get_rect().width,300))
         if relX < platform.get_rect().width:
             screen.blit(platform, (relX, 300))
         x-=6
         score=displayScore() #call score function
         
         foxPlayer.draw(screen) #draw sprites from player groupSingle
         foxPlayer.update() #update sprites with update method
         obstacleGroup.draw(screen)
         obstacleGroup.update()
         #gameActive = PlayerCollision()
         PlayerCollision(count)

    else:
        if score > highscore:
            highscore = score
            with open(path.join(dir, highScoreFile), 'w') as f:
                f.write(str(score)) 
        screen.blit(bg, (0,0))
        screen.blit(gameName, gameNameRect) #title game
        scoreMessage=test_font.render(f'Score: {score}', False, DARKPURPLE)
        scoreMessageRect=scoreMessage.get_rect(center=(400,330))
        highScoreMessage=test_font.render(f'Highscore: {highscore}', False, DARKPURPLE)
        highScoreMessageRect=highScoreMessage.get_rect(center=(400,300))

        if score==0: #after you start the game, score is no longer 0
            if (time.get_ticks()//1000) % 2==0: #blinking effect
                screen.blit(gameMessage, gameMessageRect) #when first load game
            else:
                screen.blit(bg, (0,0))
                screen.blit(gameName, gameNameRect) #title game
        else:
            screen.blit(scoreMessage,scoreMessageRect) #message after playing game
            screen.blit(highScoreMessage,highScoreMessageRect) #message after playing game

    clock.tick(60) #frames per second
    display.flip()
            
quit()
