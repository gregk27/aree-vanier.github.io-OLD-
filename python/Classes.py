# VERSION 3.5

import math, random

import pygame
from colorsys import hsv_to_rgb

#setup map size
mapSize = 0
def init(mapS):
    global mapSize
    mapSize = mapS
    
    
screen = None

FRICTION = 0.05

#Basic entity class, extended by tank
class Entity:
    def __init__(self, x, y, shape, colour):
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = colour
        self.scale = 1
        self.angle = 0
        self.speed = 0
        self.simSpeed = 1
        self.maxSpeed = 1
        self.minSpeed = -1
        
    def getShape(self, usePoints, angle):
        ang=(angle+90)*math.pi/180.0
        points=[]
        for p in usePoints:
            x=(p[0]*self.scale)*math.cos(ang)-(p[1]*self.scale)*math.sin(ang)+self.x
            y=(p[0]*self.scale)*math.sin(ang)+(p[1]*self.scale)*math.cos(ang)+self.y
            points.append([x,y])
        return points
    
    def draw(self, surface):
        pygame.draw.polygon(surface, self.colour, self.getShape(self.shape), 1)
        
        
    def propel(self, addSpeed):
        self.speed += addSpeed
    
    def move(self):
        self.oldX = self.x
        self.oldY = self.y
        self.x += ((self.simSpeed*self.speed)*math.cos(self.angle*math.pi/180))
        self.y += ((self.simSpeed*self.speed)*math.sin(self.angle*math.pi/180))
        if(self.x >= mapSize or self.x <= 0):
            self.x = self.oldX
        if(self.y >= mapSize or self.y <= 0):
            self.y = self.oldY
        if(self.speed > self.maxSpeed): self.speed = self.maxSpeed
        if(self.speed < self.minSpeed): self.speed = self.minSpeed
        if(self.speed > 0): self.speed -= FRICTION
        if(self.speed < -0.01): self.speed += FRICTION        
        
    def rotate(self, angle):
        self.angle += angle

        
class Tank(Entity):
    def __init__(self, x, y, shape, colour, name, ammo):
        super().__init__(x, y, shape, colour)
        self.fireMode = 0
        self.maxAmmo = ammo
        self.reloadTimer = 0
        self.maxClip = 25
        self.ammo = ammo-self.maxClip
        self.clip = 25
        
        self.dead = False
        self.deaths = 0
        self.kills = 0
        self.name = name
        self.score = 0
        self.maxHealth = 1000
        self.health = 1000
        self.gun = self.shape[1]
        self.body = self.shape[0]
        self.hitbox = self.shape[2]
        self.gunAngle = self.angle
        self.bullets = []
        self.cooldown = 0
        self.hitMarkers = 0
        
    def draw(self, surface):
        pygame.draw.polygon(surface, [0,0,0], self.getShape(self.body, self.angle), 0)
        pygame.draw.polygon(surface, self.colour, self.getShape(self.body, self.angle), 1)
        if(not self.dead):
            pygame.draw.polygon(surface, [0,0,0], self.getShape(self.gun, self.gunAngle), 0)
            pygame.draw.polygon(surface, self.colour, self.getShape(self.gun, self.gunAngle), 1)
        
    def rotate(self, angle):
        Entity.rotate(self, angle)
        self.gunAngle += angle
    
    def move(self):
        self.cooldown -= 1
        self.reloadTimer -= 1
        
        if(self.reloadTimer == 1):
            if(self.ammo > self.maxClip):
                self.ammo -= self.maxClip-self.clip
                self.clip += self.maxClip-self.clip
            else:
                self.clip += self.ammo
                self.ammo = 0
        Entity.move(self)
        
    def shoot(self):
        if(self.cooldown < 1 and self.clip > 0 and self.reloadTimer < 0):
            self.clip -= 1
            #Shoot basic bullet, med. damage and med. cooldown
            if(self.fireMode == 0):
                self.bullets.append(Bullet(self.x+27*math.cos(self.gunAngle*math.pi/180), self.y+27*math.sin(self.gunAngle*math.pi/180), 3, self.colour, self.gunAngle+random.randint(0,10)-5, 100))
                self.cooldown = 50
            #Shoot machine gun, low damage and short cooldown
            elif(self.fireMode == 1):
                self.bullets.append(Bullet(self.x+27*math.cos(self.gunAngle*math.pi/180), self.y+27*math.sin(self.gunAngle*math.pi/180), 3, self.colour, self.gunAngle+random.randint(0,10)-5, 25))
                self.cooldown = 20
            #Shoot sniper, high damage and long cooldown
            elif(self.fireMode == 2):
                self.bullets.append(Bullet(self.x+27*math.cos(self.gunAngle*math.pi/180), self.y+27*math.sin(self.gunAngle*math.pi/180), 6, self.colour, self.gunAngle+random.randint(0,10)-5, 500))
                self.cooldown = 200
            #Shoot shotgun, shoots up to 5 basic bullets at once, with slightly reduced cooldowns
            elif(self.fireMode == 3):
                self.clip += 1
                self.cooldown = 0
                for i in range(0,5):  # @UnusedVariable
                    if(self.clip > 0):
                        self.bullets.append(Bullet(self.x+27*math.cos(self.gunAngle*math.pi/180), self.y+27*math.sin(self.gunAngle*math.pi/180), 2, self.colour, self.gunAngle+random.randint(0,10)-5, 100))
                        self.clip -= 1   
                        self.cooldown += 30

    #Erase the tank by drawing over the lines with black     
    def erase(self, surface):
        temp = self.colour
        self.colour = [0,0,0]
        self.draw(surface)
        self.colour = temp
        
    def revive(self, x, y):
        self.health = self.maxHealth
        self.x = x
        self.y = y
        self.dead = False
        self.cooldown = 0
        self.ammo = self.maxAmmo
        self.clip = self.maxClip
    
    def reload(self):
        if(self.reloadTimer < 0):
            self.reloadTimer = 120
            
   
class Bot(Tank):
    def __init__(self, x, y, shape, colour, name, ammo):
        self.target=0
        super().__init__(x, y, shape, colour, name, ammo)
        
    def move(self, targets, speed):
        #Default target center of map
        targeting = True
        targetX = 2500
        targetY = 2500
        
        while targeting:
            #If self is only target, stop
            if(len(targets) < 2):
                targeting = False
            try:
                #Check if targeting self or if target is dead
                if(not targets[self.target] == self and not targets[self.target].dead):
                    targetX = targets[self.target].x
                    targetY = targets[self.target].y
                    targeting = False
                else:
                    self.target=random.randint(0,len(targets))
            except:
                ("BUG")
                self.target=random.randint(0,len(targets))
        
        #Don't get closer than 50 pixels
        if(abs(self.x-targetX) > 50 or abs(self.y-targetY) > 50):
            self.propel(speed)
            targetAngle = math.atan2(targetY-self.y, targetX-self.x)*180/math.pi
            self.gunAngle = targetAngle
            self.angle = targetAngle
        
        # Shoot if within 200 pixels
        if(abs(self.x-targetX) < 200 or abs(self.y-targetY) < 200):
            self.shoot()  
            if(self.clip < 5):
                self.reload()
        Tank.move(self)
        
        
    def revive(self, targetCount):
        self.target = random.randint(0, targetCount)
        super().revive(random.randint(0,4900), random.randint(0,4900))
        self.fireMode = random.randint(0,4)
        
class Bullet:
    def __init__(self, x, y, speed, colour, angle, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.colour = colour
        self.shape = [[-1,-1],[-1,2],[1,2],[1,-1],[0,-2]]
        self.angle = angle
        self.scale = 1
        self.life = 500
        self.damage = damage
        
    def getShape(self):
        ang=(self.angle+90)*math.pi/180.0
        points=[]
        for p in self.shape:
            x=(p[0]*self.scale)*math.cos(ang)-(p[1]*self.scale)*math.sin(ang)+self.x
            y=(p[0]*self.scale)*math.sin(ang)+(p[1]*self.scale)*math.cos(ang)+self.y
            points.append([x,y])
        return points
    
    def move(self):
        self.life -= 1
        self.x += ((self.speed)*math.cos(self.angle*math.pi/180))
        self.y += ((self.speed)*math.sin(self.angle*math.pi/180))
        self.pos = [self.x, self.y]
        
    def draw(self, surface):
        pygame.draw.polygon(surface, self.colour, self.getShape(), 1)
        
        
        
class Terrain:
    def __init__(self, x, y, points, scale, angle):
        self.x = x
        self.y = y
        self.points = points
        self.angle = angle
        self.scale = scale
    
    def getShape(self):
        ang=(self.angle)*math.pi/180.0
        points=[]
        for p in self.points:
            x=(p[0]*self.scale)*math.cos(ang)-(p[1]*self.scale)*math.sin(ang)+self.x
            y=(p[0]*self.scale)*math.sin(ang)+(p[1]*self.scale)*math.cos(ang)+self.y
            points.append([x,y])
        return points
    
    def draw(self, surface):
        pygame.draw.polygon(surface, [255,255,255], self.getShape(), 0)
        

class Supply:
    def __init__(self, x, y, life):
        self.life = life
        self.x = x
        self.y = y
        self.colour = [179, 179, 179]
        self.points = [[-10,-10],[-10,10],[10,10],[10,-10]]
        self.angle = 0
        self.hue = 0
        self.hasSupplied = []
        self.scale = 1
    
    def getShape(self):
        ang=(self.angle)*math.pi/180.0
        points=[]
        for p in self.points:
            x=(p[0]*self.scale)*math.cos(ang)-(p[1]*self.scale)*math.sin(ang)+self.x
            y=(p[0]*self.scale)*math.sin(ang)+(p[1]*self.scale)*math.cos(ang)+self.y
            points.append([x,y])
        return points
    
    def draw(self, surface):
        pygame.draw.polygon(surface, self.colour, self.getShape(), 0)
        
    def update(self):
        self.life -= 1
        self.angle +=5
        self.hue += 1
        if(self.hue == 260): self.hue = 0
        colour = hsv_to_rgb(self.hue/255, 1, 1)
        self.colour = [colour[0]*255, colour[1]*255, colour[2]*255]
        
    def resupply(self, target):
        print("HIT")
        if(target not in self.hasSupplied):
            print("SUPPLYING")
            target.ammo += target.maxAmmo/2
            if(target.ammo > target.maxAmmo): target.ammo = target.maxAmmo
            target.health += target.maxHealth/2
            if(target.health > target.maxHealth): target.health = target.maxHealth
            self.hasSupplied.append(target)
            target.ammo= int(target.ammo)
            target.health = int(target.health)
        return target
        
        
        
