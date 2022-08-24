# includes all player controls and game graphics, and runs game

from cmu_112_graphics import *
import math
import random
from initVariables import *

### Start App Screen ###
# draws splash screen
def startMode_redrawAll(app,canvas):
    canvas.create_image(app.width/2,app.height/2,image=ImageTk.PhotoImage(app.splashImg))
    canvas.create_text(app.width/2,app.height/10,text = '112Fishing',
                      font = 'Arial 32',fill = 'black')
    canvas.create_text(app.width/2,app.height*9.5/10,text = 'Press Enter to Start',
                      font = 'Arial 16',fill = 'black')
    canvas.create_text(app.width/2,app.height*9/10,text = 'Press H for Help',
                      font = 'Arial 16',fill = 'black')

# player can access help (instructions) or start the game through key presses
def startMode_keyPressed(app,event):
    if event.key == 'Enter':
        app.mode = 'prefishingMode'
    elif event.key.lower() == 'h':
        app.mode = 'helpMode'
        app.prevMode = 'startMode'

### Help Screen ###
# prints instructions for player
def helpMode_redrawAll(app,canvas):
    canvas.create_text(app.width/2,app.height*(1/5),text = "Catch fish by lining the hook up with a fish's mouth.",
                        font = 'Arial 10', fill = 'black')
    canvas.create_text(app.width/2,app.height*(2/5), text = "Adjusting the tension of the rod with the Up and Down arrow keys",
                        font = 'Arial 10', fill = 'black')
    canvas.create_text(app.width/2,app.height*(3/5),text = "Fish are automatically sold for money, which you can then spend.",
                        font = 'Arial 10', fill = 'black')
    canvas.create_text(app.width/2,app.height*(4/5),text = "Different fish are sold for different prices.",
                        font = 'Arial 10', fill = 'black')
    canvas.create_text (app.width/2,app.height*9/10,text = 'Press R to return',
                        font = 'Arial 10', fill = 'black')

# player can return to previous screen by pressing 'r'
def helpMode_keyPressed(app,event):
    if event.key.lower() == 'r':
        app.mode = app.prevMode

### "Menu" Before Fishing (prefishing screen)###
# draws each part of prefishing screen
def prefishingMode_redrawAll(app,canvas):
    # sky / water line
    canvas.create_rectangle(0,0,app.width,app.height/2,fill = app.sky)
    canvas.create_rectangle(0,app.height/2,app.width,app.height,fill='blue')
    # boat / person
    canvas.create_image(app.width*(1/5),app.height*(2/5),
                        image = app.playerPhImg)
    canvas.create_arc(0,app.height*(2/7),app.width/3,app.height*(4/7),
                      start = 0, extent = -180,fill = 'brown')
    # text instructions for navigating screens
    canvas.create_text(app.width/2,app.height/20,text = 'Press F to fish')
    canvas.create_text(app.width/2,app.height/20+15,text = 'Press S to shop')
    canvas.create_text(app.width/2,app.height/20+30,text = 'Press H for Help')
    canvas.create_text(app.width/2,app.height/20+45,text = 'Press Enter to change rod color')
    canvas.create_text(app.width/2,app.height/20+60,text = f'Current rod color: {app.rodColor}')
    # if app.endFishing is true, then the player is returning from fishing screen.
    # if player caught a fish, then game draws a message that notifies player
    # of the fish they caught and how much it was worth
    if app.endFishing:
        if app.hookedFish != None:
            canvas.create_rectangle(app.width/2-100,app.height/2-50,
                                    app.width/2+100,app.height/2+50,
                                    fill = 'white')
            canvas.create_text(app.width/2,app.height/2,
                                text = f"""You caught a {app.hookedFish}!
            Sold for ${app.hookedFish.price}""")

# player can naviagte game menus through key presses
def prefishingMode_keyPressed(app,event):
    # if the end fishing message is up, then setting app.endFishing to False
    # will remove that message
    if app.endFishing:
        app.endFishing = False
    elif event.key.lower() == 'h':
        app.mode = 'helpMode'
        app.prevMode = 'prefishingMode'
    elif event.key.lower() == 'f':
        initFishingVars(app)
        initPhysicsVars(app)
        app.mode = 'fishingMode'
    elif event.key.lower() == 's':
        app.mode = 'shopMode'
    elif event.key == 'Enter':
        changeRodColor(app)

# changes rod color to next rod color that has been unlocked by player
def changeRodColor(app):
    originalIndex = app.rodColorIndex
    app.rodColorIndex += 1
    app.rodColorIndex %= 5
    while (app.rodColorUnlocked[app.rodColorIndex] == False and 
           app.rodColorIndex != originalIndex):
           app.rodColorIndex += 1
           app.rodColorIndex %= 5
    app.rodColor = app.rodColors[app.rodColorIndex]
    
### Actual Fishing (fishing screen)###
# Pressing 'c' cancels the fishing, returning player to prefishing screen
def fishingMode_keyPressed(app,event):
    if event.key.lower() == 'c':
        app.mode = 'prefishingMode'

# side scrolling from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#sidescrollerExamples 
# draws sky, water, fishing pole, fishing line, hook, and fish
def fishingMode_redrawAll(app,canvas):
    # sky / water line
    canvas.create_rectangle(0,0,app.width,
                            app.waterY-app.scrollY, fill = app.sky)
    canvas.create_rectangle(0,app.waterY-app.scrollY,
                            app.width,app.height,fill = 'blue')
    # fishing pole
    canvas.create_rectangle(0,app.poleY-app.scrollY,
                            app.width/2-app.scrollX,
                            app.poleY-app.scrollY+app.poleWidth,
                            fill= app.rodColor)
    canvas.create_line(app.width/2-app.scrollX,app.poleY-app.scrollY+app.poleWidth,
                       app.width/2,app.height/2)
    # hook
    canvas.create_image(app.width/2,app.height/2 - app.hookHeight/2,
                        image = app.pHook)
    # bait (app.baitRadius is in meters, each pixel is 1 cm, so multiply app.baitRadius by 100 cm/m)
    canvas.create_oval(app.baitX-app.baitRadius*100,app.baitY-app.baitRadius*100,
                       app.baitX+app.baitRadius*100,app.baitY+app.baitRadius*100,
                        fill = 'grey')
    canvas.create_text(app.width/2,app.height/20,
                        text = 'Press C to cancel')
    # depending on the direction that the fish/boid is facing, the fish image
    # must be offset by +- fish.imageWidth/2
    for fish in app.fish:
        if fish.dx < 0:
            canvas.create_image(fish.cx+fish.imageWidth/2-app.scrollX,fish.cy-app.scrollY,
                            image = fish.pImage)
        else:
            canvas.create_image(fish.cx-fish.imageWidth/2-app.scrollX,fish.cy-app.scrollY,
                            image = fish.pImage)
    for boid in app.boids:
        if app.boidCMV < 0:
            canvas.create_image(boid.cx+boid.imageWidth/2-app.scrollX,boid.cy-app.scrollY,
                            image = boid.pImage)
        else:
            canvas.create_image(boid.cx-boid.imageWidth/2-app.scrollX,boid.cy-app.scrollY,
                            image = boid.pImage)
    if app.hookedFish != None:
        if app.hookedFish.dx < 0:
            canvas.create_image(app.hookedFish.cx+app.hookedFish.imageWidth/2,
                                app.hookedFish.cy,
                                image = app.hookedFish.pImage)
        else:
            canvas.create_image(app.hookedFish.cx-app.hookedFish.imageWidth/2,
                                app.hookedFish.cy,
                                image = app.hookedFish.pImage)

# returns random position and direction of a fish / boid
def getRandPositionAndDir(app):
    x = random.randint(10,app.width-10)
    y = random.randint(app.height/2+app.loBound,app.height/2+app.hiBound)
    dx = random.randint(-4,4)
    while abs(dx) <= 3:
        dx = random.randint(-4,4)
    return x,y,dx

# every 100 ms, timer fires to recalculate forces on the fish and hook, 
# including their velocities
def fishingMode_timerFired(app):
    # when underwater, consider buoyant force, drag, and viscosity
    setForces(app)
    app.xAccel = app.netForceX / app.totalMass
    app.xVelocity += app.xAccel
    app.yAccel = (app.netForceY / (app.totalMass)) 
    app.yVelocity += app.yAccel
    # turn velocity into cm
    app.scrollX += app.xVelocity*100
    app.scrollY += app.yVelocity*100
    # if fish is successfully caught
    if app.scrollY < -(0.3)*app.width:
        app.endFishing = True
        if app.hookedFish != None:
            app.money += app.hookedFish.price
        app.mode = 'prefishingMode'
    # attempt to spawn fish every 0.5 second and if there are less than 10
    # fish currently
    if app.spawnCounter >= 5 and len(app.fish) < 10:
        spawnFish(app)
        app.spawnCounter = 0
    else:
        app.spawnCounter += 1
    # fish movement
    moveFish(app)
    moveBoids(app)

# generates a random number to determine the type of fish that is spawned (if any)
# if no boids are currently in the game, randomly generates a number to determine
# whether or not to spawn the fish as a set of boids instead.
def spawnFish(app):
    # probability check
    check = random.randint(1,100)
    prob = check / 100
    cx,cy,dx = getRandPositionAndDir(app)
    newFish = None
    if prob <= 0.2:
        newFish = app.Walleye(cx,cy,dx)
    elif prob > 0.21 and prob <= 0.60:
        newFish = app.Bluegill(cx,cy,dx)
    elif prob > 0.61 and prob <= 0.90:
        newFish = app.Bass(cx,cy,dx)
    if app.boids == []:
        boidCheck = random.randint(1,100)
        if boidCheck > 85 and newFish != None:
            spawnBoids(app, type(newFish))
            return
    elif newFish != None:
        if dx < 0:
            newFish.transpose()
        app.fish.append(newFish)

# creates boids in random positions (around a random point) and adds them 
# to app.boids
def spawnBoids(app,fishType):
    # create boids and add them to list
    app.boidCM = (getRandPositionAndDir(app)[0],getRandPositionAndDir(app)[1])
    app.boidCMV = getRandPositionAndDir(app)[2]
    lowerBound = app.boidCM[1]+app.boidSpawnRange
    upperBound = app.boidCM[1]-app.boidSpawnRange
    leftBound = app.boidCM[0]-app.boidSpawnRange
    rightBound = app.boidCM[0]+app.boidSpawnRange
    for i in range(10):
        randY = random.randint(upperBound,lowerBound)
        randX = random.randint(leftBound,rightBound)
        newBoid = fishType(randX,randY,app.boidCMV)
        if app.boidCMV < 0:
            newBoid.transpose()
        app.boids.append(newBoid)

# gets total mass, buoyant force, viscosity force, and rArea based on whether
# or not there is a fish hooked on the line
def getPhysicsInputs(app):
    if app.isHooked:
        app.totalMass = app.baitMass + app.hookedFish.mass
        app.bForce = 1000*(.098)*app.hookedFish.volume
        app.vForce = 0
        app.rArea = app.hookedFish.rArea
    else:
        app.totalMass = app.baitMass
        app.bForce = 1000*(.098)*app.baitVolume
        app.vForce = 6*math.pi*app.vCoeff*app.baitRadius*app.yVelocity
        app.rArea = app.baitRefArea

# calculates net X and Y forces based on physical inputs
def setForces(app):
    getPhysicsInputs(app)
    app.gForce = app.totalMass * 0.098
    # horizontal motion
    if app.xVelocity != 0:
        app.angle = math.atan((app.scrollY+app.poleY) / (app.scrollX+10**-8))
        app.xTension = app.tension * math.cos(app.angle)
        app.yTension = app.tension * math.sin(app.angle)
        if app.xVelocity > 0:
            app.netForceX = app.xTension - app.drag
        else:
            app.netForceX = app.xTension + app.drag
    else:
        app.yTension = app.tension
    # if underwater
    if app.scrollY > 0:
        app.drag = (0.5)*(1000)*(app.yVelocity**2)*(app.rArea)*(app.dSCoeff)
        if app.yVelocity >= 0:
            app.netForceY = (-app.yTension-app.bForce-app.drag-app.vForce
                        +app.gForce)
        elif app.yVelocity < 0:
            app.netForceY = (-app.yTension-app.bForce
                            +app.drag+app.vForce+app.gForce)
    # if air, no buoyant or viscosity force
    else:
        app.drag = ((0.5)*(1.2)*(app.yVelocity**2)*(app.rArea)
                        *(app.dCCoeff))
        if app.yVelocity >= 0:
            app.netForceY = (-app.yTension-app.drag+app.gForce)
        elif app.yVelocity < 0:
            app.netForceY = (-app.yTension+app.drag+app.gForce)

# every second, moves fish. if fish is close enough (within 10 pixel), hooks it
# onto fishing line. 
# if fish is at the edge of the screen, flips its image and direction.
def moveFish(app):
    i = 0
    while i in range(len(app.fish)):
        f = app.fish[i]
        f.cx += f.dx
        if f.cx <= 0 or f.cx >= app.width:
            f.dx = -f.dx
            f.transpose()
        d = getDistance(f.cx,f.cy-app.scrollY,app.width//2,app.height//2)
        if abs(d) < 10 and app.isHooked == False:
            changeToHooked(app,i,app.fish)
        else:
            i += 1 

# takes input index i of fish f and hooks it onto the bait
# app.tension increases (natural reaction when a fish is felt on the rod)
# pops it from the list (either app.fish or app.boid)
def changeToHooked(app,i,listFishOrBoid):
    f = listFishOrBoid[i]
    if listFishOrBoid == app.boids:
        f.dx = app.boidCMV
    app.isHooked = True
    f.isHooked = True
    app.tension += 0.05
    app.hookedFish = f
    addFishMomentum(app)
    listFishOrBoid.pop(i)
    f.cx,f.cy = app.width//2,app.height//2

# when a fish is hooked, it transfers some momentum onto the hook and line
# calculates the momentum of the fish as it is hooked, and then calculates the
# velocity of the fish and line in the horizontal direction
def addFishMomentum(app):
    # fish "struggles", increasing its speed
    app.hookedFish.dx *= 5
    # dx is in pixels = cm, multiply by 0.01 to turn into meters
    momentum = app.hookedFish.mass * app.hookedFish.dx*0.01
    getPhysicsInputs(app)
    app.xVelocity = (momentum / app.totalMass)

# boids movement based on http://www.vergenet.net/~conrad/boids/pseudocode.html
# moves each boid in app.boids
def moveBoids(app):
    # first check if any boids are hooked
    i = 0
    while i in range(len(app.boids)):
        boid = app.boids[i]
        d = getDistance(boid.cx,boid.cy-app.scrollY,app.width//2,app.height//2)
        if abs(d) < 10 and app.isHooked == False:
            changeToHooked(app,i,app.boids)
            break
        else:
            i += 1
    # moves the boids based on algorithm above
    for boid in app.boids:
        v1 = boidCohesion(app,boid)
        v2 = boidSeparation(app,boid)
        xMovement = v1[0] + v2[0]
        yMovement = v1[1] + v2[1]
        boid.cx += xMovement + app.boidCMV
        boid.cy += yMovement
        if app.boidCM[0] < 0 or app.boidCM[0] > app.width:
            boid.transpose()
    app.boidCM = (app.boidCM[0]+app.boidCMV,app.boidCM[1])
    # changes direction of the boids when its center of mass hits edge of screen
    if app.boidCM[0] < 0 or app.boidCM[0] > app.width:
        app.boidCMV = -1*app.boidCMV

# returns velocity vector of cohesion factor in boid movement
# boids try to stay somewhat close to each other by moving towards
# the center of mass of the boids as a whole
def boidCohesion(app,boid):
    # calculate perceived center of mass of boid
    sumX = 0
    sumY = 0
    for b in app.boids:
        if b != boid:
            sumX += b.cx
            sumY += b.cy
    averageX = sumX / (len(app.boids)-1)
    averageY = sumY / (len(app.boids)-1)
    perceivedCM = (averageX,averageY)
    xDistance = perceivedCM[0] - boid.cx
    yDistance = perceivedCM[1] - boid.cy
    # every 100 ms, boid moves 1% towards perceived CM
    return (xDistance/100,yDistance/100)

# returns velocity vector of separation factor in boid movement
# boids try to keep some separation from each other (to not run into others)
def boidSeparation(app,boid):
    dx = 0
    dy = 0
    for b in app.boids:
        if b != boid:
            d = getDistance(b.cx,b.cy,boid.cx,boid.cy)
            if d < 5:
                dx = dx - (b.cx - boid.cx)
                dy = dy - (b.cy - boid.cy)
    # every 100 ms, boids move 5% "away from each other"
    return (dx/20,dy/20)

# returns distance between two points
def getDistance(x0,y0,x1,y1):
    return ((x1-x0)**2+(y1-y0)**2)**0.5

# player controls tension by pressing Up and Down arrow keys
def fishingMode_keyPressed(app,event):
    if app.isHooked:
        # limits the tension that the player can control
        # when there is a fish on the hook, allows the player to increase tension more
        if abs(app.tension) <= 4:
            if event.key == 'Up':
                app.tension += 1/4
            elif event.key == 'Down':
                app.tension -= 1/4
    else:
        # limits the tension that the player can control
        # tension changes are very small to allow them to have more control
        if abs(app.tension) <= 4 / 10000:
            if event.key == 'Up':
                app.tension += 1 / 100000
            elif event.key == 'Down':
                app.tension -= 1 / 100000
    # cancels fishing and returns to prefishing screen
    if event.key.lower() == 'c':
        app.mode = 'prefishingMode'
        initFishingVars(app)
        initPhysicsVars(app)

### Shop Screen ###
### Unlock rod colors with money
def shopMode_redrawAll(app,canvas):
    canvas.create_text(app.width/2,app.height/20,text = f'Money: ${app.money}')
    canvas.create_text(app.width/2,app.height*9.5/10,text = 'Press R to return')
    drawRodColorRectangles(app,canvas)

# draws each button that player can click to buy new rod colors
# displays color name and price
# if rod color already bought, notifies player as such
def drawRodColorRectangles(app,canvas):
    for i in range(1,len(app.rodColors)):
        canvas.create_rectangle(app.xMargin,app.yMargin*i+(i-1)*app.rHeight,
                                app.xMargin+app.rWidth,i*(app.rHeight+app.yMargin),
                                fill = app.rodColors[i])
        if app.rodColorUnlocked[i]:
            canvas.create_text(app.width/2,app.yMargin*i+app.rHeight*(0.5+(i-1)),
                                text = 'Already bought!')
        else:
            canvas.create_text(app.width/2,app.yMargin*i+app.rHeight*(0.5+(i-1)),
                                text = f'{app.rodColors[i]}: ${app.rodPrices[i]}')

# checks if the player's mouseclick is within a box. If the rod color hasn't
# been bought and the player has enough money to buy it, player buys it
def shopMode_mousePressed(app,event):
    x,y = event.x,event.y
    leftBound = app.xMargin
    rightBound = app.xMargin + app.rWidth
    if x <= rightBound and x >= leftBound:
        for i in range(1,len(app.rodColors)):
            upperBound = app.yMargin*i+(i-1)*app.rHeight
            lowerBound = i*(app.rHeight+app.yMargin)
            if y <= lowerBound and y >= upperBound:
                if app.rodColorUnlocked[i] == False:
                    price = app.rodPrices[i]
                    if app.money >= price:
                        app.money -= price
                        app.rodColorUnlocked[i] = True

# when 'r' is pressed, player returns to previous screen
def shopMode_keyPressed(app,event):
    if event.key.lower() == 'r':
        app.mode = 'prefishingMode'

runApp(width=600,height=700)