#settings
from pygame import *
from random import randint, choice #random integer and randomly pick from list
font.init()
running=True
width,height=800,400
screen=display.set_mode((width,height))
display.set_caption('Fox Runner') #program title
clock=time.Clock()
gameActive=False
startTime=0
YELLOW=(252,183,36,255)
DARKPURPLE=(50, 43,67,255)
BLUE=(214,243,255)
SATBLUE=(71,243,255)
DARKBLUE=(47,189,255)
score=0
highScoreFile= "highscore.txt"
