import pygame
import time
import random
from freegames import vector

pygame.init()

global score
# scorefile
def savescore(point):
    scorefile=open("Flappy.txt","a")
    scorestring = "%s" %point
    scorefile.write("\n Player score is:"+scorestring)
    scorefile.write("\n player loose")
    scorefile.write("\n###############")
    scorefile.close()
    
# game height and width
display_width = 800
display_height = 600

# colors 
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53,115,255)

# setting width bird image
flappy_width = 60

# displaying image and setting caption
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Flappy Birds')
clock = pygame.time.Clock()
flappyicon = pygame.image.load('img.jpg')
pygame.display.set_icon(flappyicon)

# variables
pause = False
crash=False

# quit code
def quitgame():
    pygame.quit()
    quit()

# unpause code
def unpause():
    global pause
    pause = False

# item dodged
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

# game over code
def out(points):
    savescore(points)
    largeText = pygame.font.SysFont("comicsansms",50)
    TextSurf, TextRect = text_objects("Game Over ", largeText)
    TextRect.center = ((display_width/3),(display_height/3))
    gameDisplay.blit(TextSurf, TextRect)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Play Again",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

# object display on screen code
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

# flappy bird
def flapp(x,y):
    gameDisplay.blit(flappyicon, (x, y))

# setting message
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',100)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

# paused code
def paused():

    largeText = pygame.font.SysFont("comicsansms",100)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)   

# setting text
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

# setting button
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

# game intro code
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Flappy Birds", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)    

# game loop code
def game_loop():
    global pause
    global crash 
    
    x = (display_width * 0.85)    
    y = (display_height * 0.30)
    ychange = 0

    rang= random.randrange(100,600)
    
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100
    
    dodged = 0

    while not crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                ychange = -3
            elif event.type == pygame.MOUSEBUTTONUP:
                ychange = 3

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()

        y += ychange
        gameDisplay.fill(white)

        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_startx += thing_speed
        flapp(x,y)
        things_dodged(dodged)

        if y > display_width - flappy_width or y < 0 :
            out(dodged)
            
        if thing_startx > display_width:
            thing_startx = 0 - thing_width
            thing_starty = random.randrange(0, display_height)
            dodged += 1
            thing_speed += 1
            thing_height += (dodged * 1)


        if x < thing_startx+thing_width:
            if y > thing_starty and y < thing_starty + thing_height or y + flappy_width > thing_starty and y + flappy_width < thing_starty + thing_height:
                out(dodged)
                
        pygame.display.update()
        clock.tick(60)

#calling function
game_intro()
game_loop()
pygame.quit()
quit()        
