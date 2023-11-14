import pygame, sys
from pygame.locals import *
from pygame.math import *

# display dimensions
HEIGHT = 960
WIDTH = 1280

# frames per second
FPS = 60

# radius
R = 75

# ground gravity
G = 0.5

# bounce factor
BOUNCE = 0.85


pygame.init()
 
clock = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ballaballa ** 2")


ball = pygame.image.load("ball2.png")


# position
pos = Vector2(WIDTH / 2.0, 200)

# velocity
vel = Vector2(0.0, 0.0)

# acceleration
acc = Vector2(0.0, 0.0)


# gravitate ball to mouse
mouseGravity = False

# sounds
bottomSound = pygame.mixer.Sound("bottom.wav")
leftSound = pygame.mixer.Sound("left.wav") 
rightSound = pygame.mixer.Sound("right.wav") 
topSound = pygame.mixer.Sound("top.wav") 
snapSound = pygame.mixer.Sound("snap.wav")  
mouseGravitySound = pygame.mixer.Sound("gnoiz.wav") 
mouseGravitySound.set_volume(0.3)

# compute sound level depending on velocity
def computeSoundLevel(v):
    level = v.length() / 84.0
    level = min(0.7, level)
    return level
 

while True:

    #### READ INPUT ###

    mousePos = Vector2(pygame.mouse.get_pos())

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # throw
            throwDirection = (mousePos - pos) * 0.07
            vel += throwDirection
            snapSound.set_volume(computeSoundLevel(throwDirection))
            pygame.mixer.Sound.play(snapSound) 

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouseGravity = True
            pygame.mixer.Sound.play(mouseGravitySound, -1) 

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouseGravity = False
            pygame.mixer.Sound.stop(mouseGravitySound)

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


    #### UPDATE ###

    # basic gravity
    acc = Vector2(0, G)

    # mouse gravity
    if mouseGravity:
        acc += 125000 * (Vector2(mousePos) - Vector2(pos)).normalize() / pos.distance_squared_to(mousePos)

    # limit acc
    if acc.length() > 1:
        acc.scale_to_length(1)

    # limit vel
    if vel.length() > 100:
        vel.scale_to_length(100)

    # move
    vel += acc
    pos += vel

    # check wall collision (x)
    if pos.x - R < 0:
        # left
        pos.x = R
        vel.x = -vel.x * BOUNCE
        vel.y = vel.y * BOUNCE
        leftSound.set_volume(computeSoundLevel(vel))
        pygame.mixer.Sound.play(leftSound) 
    elif pos.x + R > WIDTH:
        # right
        pos.x = WIDTH - R
        vel.x = -vel.x * BOUNCE
        vel.y = vel.y * BOUNCE
        rightSound.set_volume(computeSoundLevel(vel))
        pygame.mixer.Sound.play(rightSound) 

    # check wall collision (y)
    if pos.y - R < 0:
        # top
        pos.y = R
        vel.y = - vel.y * BOUNCE
        vel.x = vel.x * BOUNCE
        topSound.set_volume(computeSoundLevel(vel))
        pygame.mixer.Sound.play(topSound) 
    elif pos.y + R > HEIGHT:
        # bottom
        pos.y = HEIGHT - R
        vel.y = - vel.y * BOUNCE
        vel.x = vel.x * BOUNCE
        bottomSound.set_volume(computeSoundLevel(vel))
        pygame.mixer.Sound.play(bottomSound) 


    #### DRAW ###

    # white background
    displaysurface.fill((255,255,255))

    # mouse circle
    if mouseGravity:
        pygame.draw.circle(displaysurface, (255,255,205), mousePos, 33)
    else:
        pygame.draw.circle(displaysurface, (255,225,225), mousePos, 33)

    # draw ball
    displaysurface.blit(ball, pos - Vector2(R, R)) 

    # draw acceleration line
    pygame.draw.line(displaysurface, (50,0,200), pos, pos + (acc * 100), 3) 

    # draw velocity line
    pygame.draw.line(displaysurface, (0,0,0), pos, pos + (vel * 10), 3)

 
    pygame.display.update()
    
    clock.tick(FPS)