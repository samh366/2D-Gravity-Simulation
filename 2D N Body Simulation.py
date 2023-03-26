import os
import random

import pygame
import math

G = 6.67430e-11

from simulation import AU, Simulation
import time

directory = os.path.dirname(os.path.realpath(__file__))

# Timestep of one hour
simName = "2D N Body Simulation 1.1"
mysim = Simulation()
mysim.setParameters(name=simName, size=AU*5, allPairs=True, timestep=8*3600, iterations=1, theta=1)
mysim.setReturnValues("name", "position")

random.seed(4)

mysim.addStar(
    name="Sun",
    mass=1.98847e30,
    radius=696340*1000,
    position=[0, 0, 0],
    velocity=[0, 0, 0],
    texture=None,
    luminosity=0,
    surfaceTemp=0
)

for i in range(100):
    dist = random.randint(AU*0.2, AU*1.5)
    v = math.sqrt((G*1.98847e30)/dist)  # Calc orbital speed
    angle = random.randint(0, 360)    # Random angle
    # Translate pos
    Px = dist*math.cos(math.radians(angle))
    Py = dist*math.sin(math.radians(angle))
    # Translate V
    Vx = -math.sin(math.radians(angle))*v
    Vy = math.cos(math.radians(angle))*v

    mysim.addPlanet(
        name="Planet " + str(i),
        mass=random.randint(1, 1000)*10e22,
        radius=6371*1000,
        position=[Px, Py, 0],
        velocity=[Vx, Vy, 0],
        gravity=True,
        texture=None
    )


pygame.init()
pygame.display.set_caption("N-Body Galaxy Simulation - All Pairs Algorithm")

gameWidth = 800
gameHeight = 800
gameDisplay = pygame.display.set_mode((gameWidth, gameHeight))

scalex = 800/(AU*5)
scaley = -800/(AU*5)

clock = pygame.time.Clock()

timeStarted = None

def drawPlanets(summary):
    for key in list(summary):
        if "Sun" in summary[key]["name"]:
            color = pygame.Color((245, 226, 17))
            size = 10

        if "Fragment" in summary[key]["name"]:
            color = pygame.Color((150, 150, 150))

        if "Planet" in summary[key]["name"]:
            color = pygame.Color((150, 150, 150))
            size = 5
        
        circlePos = (gameWidth/2 + summary[key]["position"][0] * scalex, gameHeight/2 + summary[key]["position"][1] * scaley)
        pygame.draw.circle(gameDisplay, color, circlePos, size)

        #print(summary[key]["position"])


# Draw barnes hut grid each frame
def drawLines(node, start=True):
    # Draw a green frame
    if start:
        pygame.draw.rect(gameDisplay, (0, 255, 0), pygame.Rect(0, 0, gameWidth, gameHeight), 2)

    for childNode in node.childNodes:
        if childNode != None:
            drawLines(childNode, False)
            # Draw line
            centre = [gameWidth/2 + childNode.centre[0]*scalex, gameHeight/2 + childNode.centre[1]*scaley]
            centre = [round(centre[0] - (childNode.quadSize*scalex)), round(centre[1] - (childNode.quadSize*-scaley))]
            length = [childNode.quadSize*scalex*2, childNode.quadSize*-scaley*2]

            pygame.draw.rect(gameDisplay, (0, 255, 0), pygame.Rect(
                centre[0],
                centre[1],
                length[0],
                length[1]),
                2
            )



crashed = False
pause = True
showLines = False
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)
FINALTIME = -1
root = None

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                showLines = not showLines
            
            if event.key == pygame.K_SPACE:
                pause = not pause
                timeStarted = time.time()
            

    gameDisplay.fill((0, 0, 0))

    # Advance simulation
    if not pause and mysim.getFrames() < 2000:
        summary, root = mysim.simulate()

    else:
        summary = mysim.summary()

    if mysim.getFrames() >= 2000 and FINALTIME == -1:
        FINALTIME = round(time.time() - timeStarted)

    drawPlanets(summary)

    if root != None and showLines == True:
        drawLines(root, start=True)


    # Show num of frames
    textsurface = myfont.render("Frames Calculated: {}".format(str(mysim.getFrames())), False, (255, 255, 255))
    gameDisplay.blit(textsurface,(0,0))

    if root != None:
        # Show num of bodies
        textsurface2 = myfont.render("Simulated Bodies: {}".format(root.numOfBodies), False, (255, 255, 255))
        gameDisplay.blit(textsurface2,(0,20))
    
    # Show time passed in years
    years = round((mysim.getFrames()*mysim.getTimestep())/(365*24*3600), 2)
    textsurface3 = myfont.render("Year: {}".format(str(years)), False, (255, 255, 255))
    gameDisplay.blit(textsurface3,(0,40))

    # Show real time
    if timeStarted != None:
        if FINALTIME == -1:
            seconds = round(time.time() - timeStarted)
        else:
            seconds = FINALTIME
    else:
        seconds = 0
    timer = "{}:{}".format(str(seconds//60).zfill(2), str(seconds%60).zfill(2))
    textsurface3 = myfont.render("Time Elapsed: {}".format(str(timer)), False, (255, 255, 255))
    gameDisplay.blit(textsurface3,(0,60))

    pygame.display.update()
    clock.tick(60)



pygame.quit()
quit()
