# initializes variables for game
from cmu_112_graphics import *
import math

def appStarted(app):
    # scale for the fish images
    app.scale = 1/20
    # defines fish and fish subclasses
    app.Walleye,app.Bluegill,app.Bass = initFishClasses(app)
    initRodVars(app)
    initImages(app)
    app.sky = 'deep sky blue'
    app.money = 0
    initFishingVars(app)
    initPhysicsVars(app)
    app.mode = 'startMode'
    # lower and upper bounds (in depth) for where fish can spawn
    app.loBound = 100
    app.hiBound = 300

def initFishClasses(app):
    class Fish:
        def __init__(self,cx,cy,dx):
            self.cx = cx
            self.cy = cy
            self.dx = dx
            self.isHooked = False
        # transpose from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#flipImage 
        def transpose(self):
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.pImage = ImageTk.PhotoImage(self.image)

    # cx and cy represent position of fish mouth
    # rArea: reference area for a cylinder, used to calculate drag
    # walleye image from https://www.subpng.com/png-9i3lv9/
    class Walleye(Fish):
        def __init__(self,cx,cy,dx):
            super().__init__(cx,cy,dx)
            self.price = 20
            # temporary radius to draw it as a circle
            self.r = 10
            self.mass = 2
            self.volume = 0.007
            self.rArea = 0.003
            self.image = app.loadImage('walleye.png')
            self.image = app.scaleImage(self.image,app.scale)
            self.imageWidth,self.imageHeight = self.image.size
            self.pImage = ImageTk.PhotoImage(self.image)
        def __repr__(self):
            return f'Walleye'

    # bluegill image from https://www.cleanpng.com/png-bluegill-fish-gill-actinopterygii-drawing-clip-art-5572451/
    class Bluegill(Fish):
        def __init__(self,cx,cy,dx):
            super().__init__(cx,cy,dx)
            self.r = 6
            self.mass = 0.2
            self.volume = 0.002
            self.rArea = 0.001
            self.price = 10
            self.image = app.loadImage('bluegill.png')
            self.image = app.scaleImage(self.image,app.scale)
            self.imageWidth,self.imageHeight = self.image.size
            self.pImage = ImageTk.PhotoImage(self.image)
        def __repr__(self):
            return f'Bluegill'

    # bass image from https://www.subpng.com/png-0g2oyd/
    class Bass(Fish):
        def __init__(self,cx,cy,dx):
            super().__init__(cx,cy,dx)
            self.r = 10
            self.mass = 1
            self.volume = 0.004
            self.rArea = 0.001
            self.price = 5
            self.image = app.loadImage('bass.png')
            self.image = app.scaleImage(self.image,app.scale)
            self.imageWidth,self.imageHeight = self.image.size
            self.pImage = ImageTk.PhotoImage(self.image)
        def __repr__(self):
            return f'Bass'
    return Walleye,Bluegill,Bass

# initializes images, scales them down, and caches them in PhotoImages
def initImages(app):
    # splashImg source: https://depositphotos.com/vector-images/fishing-boat-cartoon.html
    # playerImg source: https://www.pinterest.com/pin/552605816782293976/
    # hook source: https://www.pinclipart.com/pindetail/bmRhbh_fish-hook-png-download-png-image-with-transparent/
    app.splashImg = app.loadImage('splashscreen.jpg')
    app.playerImg = app.loadImage('prefishing boy.png')
    app.playerImg = app.scaleImage(app.playerImg,1/2)
    app.playerPhImg = ImageTk.PhotoImage(app.playerImg)
    app.hook = app.loadImage('hook.png')
    app.hook = app.scaleImage(app.playerImg,1/15)
    app.hookWidth,app.hookHeight = app.hook.size
    app.pHook = ImageTk.PhotoImage(app.hook)

# initializes rod variables that are used to manage the color of rods,
# the prices of rods, and the rectangles in the shop to buy rod colors
def initRodVars(app):
    # manage rod colors
    app.rodColors = ['brown','white','red','silver','gold']
    app.rodPrices = [0,5,20,50,100]
    app.rodColorIndex = 0
    app.rodColorUnlocked = [True,False,False,False,False]
    app.rodColor = app.rodColors[app.rodColorIndex]
    # manage shop rectangles to buy rod colors
    app.rHeight,app.rWidth = app.height / 7, app.width / 2
    # vertical spacing between rectangles
    app.yMargin = app.height/15
    # horizontal space between rectangle and game border
    app.xMargin = (app.width - app.rWidth) / 2

# initializes variables used in fishing, such as base positions, velocities,
# forces, and other physical inputs
def initFishingVars(app):
    app.endFishing = False
    app.fish = []
    app.boids = []
    # boid center of mass (tuple of position on canvas) and boid center of mass velocity
    app.boidCM = (0,0)
    app.boidCMV = 0
    app.boidSpawnRange = 50
    app.hookedFish = None
    # bait dimensions, modeled after larva
    app.baitMass = 0.001
    app.baitVolume = 1*(10**-6)
    app.baitRadius = ((3/4)*app.baitVolume/math.pi)**1/3
    # reference area for a sphere (cross sectional area)
    app.baitRefArea = math.pi*app.baitRadius**2
    app.totalMass = app.baitMass
    app.rArea = app.baitRefArea
    app.baitX = app.width / 2
    app.baitY = app.height / 2
    app.waterY = app.height / 2
    app.poleY = app.height / 6
    app.poleWidth = 10
    app.scrollX = 0
    app.scrollY = 0
    app.spawnCounter = 10
    app.isHooked = False

def initPhysicsVars(app):
    app.tension = 0
    app.yTension = 0
    app.xTension = 0
    # velocity = pixels / 0.1s, where 1 pixel = 1 cm
    # positive direction down
    app.xVelocity = 0
    app.yVelocity = 0
    # acceleration of gravity = .098 m/ds^2
    app.gForce = app.baitMass * 0.098
    # vForce - skin friction experienced by bait/fish
    app.vForce = 0
    # buoyant force = density * gravity * volume displaced by object
    # water density = 1000 kg/m^3
    app.bForce = 0
    app.drag = 0
    # assume spherical baits, drag coefficient of sphere
    app.netForceY = (app.gForce)
    app.netForceX = 0
    app.xAccel = 0
    app.yAccel = app.netForceY / app.baitMass
    # drag coefficients for spheres (bait) and cylinder (fish)
    app.dSCoeff = 0.47
    app.dCCoeff = 0.82
    # viscocity coefficient
    app.vCoeff = 0.0102
