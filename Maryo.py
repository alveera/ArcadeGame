import pygame, random, sys
from pygame.locals import*
pygame.init()

window_height=600
window_width=1200
black=(0,0,0)
white=(255,255,255)
fps=25
level=0
addnewflamerate=15

class dragon:
    global firerect,imagerect,Canvas
    up=False
    down=True
    velocity=15

    def __init__(self):
        self.image=load_image('dragon.png')
        self.imagerect=self.image.get_rect(center=(1150,300))  #verify the center part

    def update(self):
        if (self.imagerect.top<cactusrect.bottom):
            self.up=False
            self.down=True
        if (self.imagerect.bottom>firerect.top):
            self.up=True
            self.down=False
        if (self.down):
            self.imagerect.bottom+=self.velocity
        if (self.up):
            self.imagerect.top-=self.velocity
        Canvas.blit(self.image,self.imagerect)

    def return_height(self):
        h=self.imagerect.top
        return h

class flames:
    flamespeed=25

    def __init__(self):
        self.image = load_image('fireball.png')
        self.imagerect = self.image.get_rect()
        self.height = Dragon.return_height() + 20
        self.surface = pygame.transform.scale(self.image, (20,20))
        self.imagerect = pygame.Rect(window_width - 106, self.height, 20, 20)

    def update(self):
        self.imagerect.left-=self.flamespeed
        Canvas.blit(self.image,self.imagerect)

    def collision(self):
        if (self.imagerect.left==0):
            return True
        else:
            return False

class maryo:
    global moveup,movedown,gravity,cactusrect,firerect
    speed=10
    downspeed=20

    def __init__(self):
        self.image=load_image('maryo.png')
        self.imagerect=self.image.get_rect()
        self.imagerect.topleft=(50,window_height/2)
        self.score=0

    def update(self):
        if (moveup and (self.imagerect.top>cactusrect.bottom)):
            self.imagerect.top-=self.speed
            self.score+=1
        if (movedown and(slef.imagerect.bottom<firerect.top)):
            self.imagerect.bottom+=self.speed
            self.score+=1
        if (gravity and (self.imagerect.bottom<firerect.top)):
            self.imagerect.bottom+=self.downspeed

def terminate():
    pygame.quit()
    sys.exit()

def waitforkey():
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()
            if event.type==pygame.KEYDOWN:
                if event.key==K_ESCAPE:
                    terminate()
                return

def flamehitsmaryo(playerrect,flames):
    for f in flame_list:
        if playerrect.colliderect(f.imagerect):
            return True
        return False

def drawtext(text,font,surface,x,y):
    textobj=font.render(text,1,white)
    textrect=textobj.get_rect()
    textrect.topleft=(x,y)
    surface.blit(textobj,textrect)

def check_level(score):
    global window_height,level,cactusrect,firerect
    if score in range(0,250):
        firerect.top=window_height-50
        cactusrect.bottom=50
        level=1
    if score in range(250,500):
        firerect.top=window_height-100
        cactusrect.bottom=100
        level=2
    if score in range(500,750):
        firerect.top=window_height-150
        cactusrect.bottom=150
        level=3
    if score in range(750,1000):
        firerect.top=window_height-200
        cactusrect.bottom=200
        level=4

def load_image(imagename):
    return pygame.image.load(imagename)

mainClock=pygame.time.Clock()
Canvas=pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('MARYO')

font=pygame.font.SysFont(None,48)
scorefont=pygame.font.SysFont(None,30)

fireimage=load_image('fire_bricks.png')
firerect=fireimage.get_rect()

cactusimage=load_image('cactus_bricks.png')
cactusrect=cactusimage.get_rect()

startimage=load_image('start.png')
startrect=startimage.get_rect()
startrect.centerx=window_width/2
startrect.centery=window_height/2

endimage=load_image('end.png')
endrect=endimage.get_rect()
endrect.centerx=window_width/2
endrect.centery=window_height/2

pygame.mixer.music.load('mario_theme.wav')
gameover=pygame.mixer.Sound('mario_dies.wav')

drawtext('Mario',font,Canvas,(window_width/3),(window_height/3))
Canvas.blit(startimage,startrect)

pygame.display.update()
waitforkey()

topscore=0
Dragon=dragon()

while True:
    flame_list=[]
    player=maryo()
    moveup=movedown=gravity=False
    flameaddcounter=0

    gameover.stop()
    pygame.mixer.music.play(-1,0.0)

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            if event.type==KEYDOWN:
                if event.key==K_UP:
                    moveup=True
                    movedown=False
                    gravity=False
                if event.key==K_DOWN:
                    moveup=False
                    movedown=True
                    gravity=False
                if event.key==K_ESCAPE:
                    terminate()

            if event.type==KEYUP:
                if event.key==K_UP:
                    moveup=False
                    movedown=False
                    gravity=True
                if event.key==K_DOWN:
                    moveup=False
                    movedown=False
                    gravity=True
        flameaddcounter+=1
        check_level(player.score)

        if flameaddcounter==addnewflamerate:
            newflame=flames()
            flameaddcounter=0
            flame_list.append(newflame)

        for f in flame_list:
            flames.update(f)

        for f in flame_list:
            if f.imagerect.left<=0:
                flame_list.remove(f)

        player.update()
        Dragon.update()

        Canvas.fill(black)
        Canvas.blit(fireimage,firerect)
        Canvas.blit(cactusimage,cactusrect)
        Canvas.blit(player.image,player.imagerect)
        Canvas.blit(Dragon.image,Dragon.imagerect)

        drawtext('Score: %s   || Level: %s  ||Top Score: %s' %(player.score,level,topscore),scorefont,Canvas,350,cactusrect.bottom+15)
        for f in flame_list:
            Canvas.blit(f.surface,f.imagerect)

        if flamehitsmaryo(player.imagerect,flame_list):
            if player.score>topscore:
                topscore=player.score
            break
        if ((player.imagerect.top<=cactusrect.bottom) or (player.imagerect.bottom>=firerect.top)):
            if player.score>topscore:
                topscore=player.score
            break

        pygame.display.update()
        mainClock.tick(fps)

    pygame.mixer.music.stop()
    gameover.play()
    Canvas.blit(endimage,endrect)
    pygame.display.update()
    waitforkey()
