# VERSION 1.1

import random
import time

import pygame, sys, math, socket, threading

from Classes import *
import gregJoy
import pointInsidePolygon
import pickle, traceback

## Fix drifting
## Change spawns - distance from location
## Change rotation controls
## reload delays
## range limitations

args = sys.argv





                # Left tread #                                        # Right Tread #                                
tankShape = [[[-8,14],[-8,-22],[-15,-22],[-15,18],[-8,18],[-8,14], [8,14],[8,-22],[15,-22],[15,18],[8,18],[8,14]], 
             # Gun Part #
             [[-8,14],[8,14],[8,-9],[1,-9],[1,-27],[-1,-27],[-1,-9],[-8,-9]],
            # Hitbox
            [[-15,-22],[-8,-22],[8,-22],[15,-22],[15,1],[15,18],[8,18],[-8,18],[-15,18],[-15,1]]]


# Sources
# Font: http://www.1001freefonts.com/data_control.font

mapSize = 5000





sock = socket.socket()
port = int(args[1])
host = socket.gethostname()
sock.bind((host, port))
print("Server hosted on:", host+":"+str(port))



# players = [Tank(100,100,tankShape,[255,255,255], "PLAYER")]
# bots = [Bot(1000,1000,tankShape, [255,0,0], "BOT"),Bot(2500,2500,tankShape, [255,0,0], "BOT"),Bot(4500,4500,tankShape, [255,0,0], "BOT")]

bots = [Bot(1000,1000,tankShape, [255,255,255], "MYBOT.CA", 5000), Bot(1000,1000,tankShape, [255,255,255], "Another bot", 5000), Bot(1000,1000,tankShape, [255,255,255], "Dat bot doe", 5000)]
players = []
clients = []
msgs = []

class Client(threading.Thread):
    def __init__(self, client):
        super(Client, self).__init__()
        self.client = client
        self.fails = 0
        self.fireModeDelay = 0
        
    
    def run(self):
        currentTime = time.time()
        while True:
            self.fireModeDelay -= 1
            oldTime = currentTime
            currentTime = time.time()
            deltaTime = currentTime - oldTime + 0.0001
#             print(deltaTime)
            try:
                data = pickle.loads(self.client.recv(2048))
#                 print(data)
                player = players[clients.index(self)] 
                keys = data[0]
                joy = data[1]
                if(keys[pygame.K_UP]): player.propel(7.5*deltaTime)
                if(keys[pygame.K_DOWN]): player.propel(-7.5*deltaTime)
                if(keys[pygame.K_LEFT]): player.rotate(-75*deltaTime)
                if(keys[pygame.K_RIGHT]): player.rotate(75*deltaTime)
                if(keys[pygame.K_a]): player.gunAngle -= 75*deltaTime
                if(keys[pygame.K_d]): player.gunAngle += 75*deltaTime
                if(keys[pygame.K_SPACE]): player.shoot()
                if(keys[pygame.K_r] and player.dead): 
                    player.revive(random.randint(100, 4900),random.randint(100, 4900))
                if(keys[pygame.K_r] and not player.dead): 
                    player.reload()
                if(keys[pygame.K_c] and self.fireModeDelay < 0):
                    self.fireModeDelay = 100
                    player.fireMode += 1
                    if(player.fireMode == 3):
                        player.fireMode = 0
                        
                if(not joy == None):
                    if(joy[gregJoy.AXIS_PITCH] > DEADZONE): player.propel(-0.75*gregJoy.AXIS_PITCH*10*deltaTime)
                    if(joy[gregJoy.AXIS_PITCH] < -DEADZONE): player.propel(0.75*gregJoy.AXIS_PITCH*10*deltaTime)
                    if(joy[gregJoy.AXIS_ROLL] > DEADZONE): player.rotate(7.5*gregJoy.AXIS_PITCH*5*deltaTime)
                    if(joy[gregJoy.AXIS_ROLL] < -DEADZONE): player.rotate(-7.5*gregJoy.AXIS_PITCH*5*deltaTime)
                    if(joy[gregJoy.BUTTON_4]): player.gunAngle -= 75*deltaTime
                    if(joy[gregJoy.BUTTON_5]): player.gunAngle += 75*deltaTime
                    if(joy[gregJoy.BUTTON_TRIGGER]): player.shoot()
                    if(joy[gregJoy.BUTTON_3] and player.dead): 
                        player.revive(random.randint(100, 4900),random.randint(100, 4900))
                    if(joy[gregJoy.BUTTON_3] and not player.dead): 
                        player.reload()
                    if(joy[gregJoy.BUTTON_2] and self.fireModeDelay < 0):
                        self.fireModeDelay = 500
                        player.fireMode += 1
                        if(player.fireMode == 3):
                            player.fireMode = 0
            except:
                pass
#             print(deltaTime)
                    
    def send(self, data):
        global msgs
        if(self.fails >= 2):
            msgs.append(["SERVER: "+players[clients.index(self)].name+" disconnected", players[clients.index(self)].colour])
            players.pop(clients.index(self))
            clients.remove(self)
            print("CLIENT REMOVED")
        try:
            sendout = pickle.dumps(data)
            self.client.sendall(sendout)
            self.fails = 0
        except:
            print("send failed", self.fails)
            self.fails += 1


class NewClient(threading.Thread):
    def __init__(self):
        super(NewClient, self).__init__()
    
    def run(self):
        global msgs
        sock.listen(5)
        while True:
            c, addr = sock.accept()
            print("Got connection from:", addr)
            c.send(str("Connected").encode())
            data = c.recv(1024).decode()
            data = data.split("|")
            data[1] = data[1].split("\\")
            client = Client(c)
            clients.append(client)
            client.start()
            print("Username:", data[0])
            print("Colour:", data[1][0], data[1][1], data[1][2])
            players.append(Tank(random.randint(100, 4900),random.randint(100, 4900),tankShape,[int(data[1][0]),int(data[1][1]),int(data[1][2])], data[0], 200))
            c.sendall("COMPLETE".encode())
            msgs.append(["SERVER: "+data[0]+" connected", [int(data[1][0]), int(data[1][1]), int(data[1][2])]])


newClient = NewClient()
newClient.start()

DEADZONE = 0.25

init(mapSize)
running = True
currentTime = time.time()

terrainShapes = [
    [[0,0],[10,0],[10,36],[46,36],[46,46],[0,46]],
    [[0,0],[36,36],[0,36]],
    [[0,0],[36,0],[36,36],[0,36]],
    [[0,0],[72,0],[72,10],[0,10]]
    ]

terrain = []
terrainShape = []
for i in range(random.randint(15,17)):
    t = Terrain(random.randint(0,4900),random.randint(0,4900), random.choice(terrainShapes), random.randint(3,6), random.randint(0,360))
    print(t.x, t.y, t.scale)
    terrainShapes.append(t.getShape())
    terrain.append(t)
print(len(terrain))

supplies = []
lastDrop = time.time()
print(lastDrop)

while running:
    
    
    oldTime = currentTime
    currentTime = time.time()
    deltaTime = currentTime - oldTime
    for bot in bots:
        if(bot.dead):
            bot.revive()
        else:
            if(len(players)>0):
                bot.move(players[0].x, players[0].y, 0.060)
            bot.shoot()
            if(bot.health < 0):
                bot.dead = True     
            if(bot.clip < 5):
                bot.reload()
        
        for bullet in bot.bullets:
            if(bullet.life > 0):
                bullet.move()
            else:
                bot.bullets.remove(bullet)
    for player in players:
        if(not player.dead):
            player.move()
            if(player.health < 0):
                player.dead = True
                player.deaths += 1
        for bullet in player.bullets:
            if(bullet.life > 0):
                bullet.move()
            else:
                player.bullets.remove(bullet)
    
    if(time.time() - lastDrop >= 60):
        supplies.append(Supply(random.randint(0,4900),random.randint(0,4900), 2500))
        lastDrop = time.time()
        msgs.append(["SERVER: SUPPLY DROP", [255,255,255]])
    
    for s in supplies:
        s.update()
        if(s.life == 0):
            supplies.remove(s)

    

    for i in players+bots:
        iShape =  i.getShape(i.hitbox, i.angle)
        for p in iShape: 
            for t in terrainShapes:
                if(abs(i.x-t[0][0]) < 500 and abs(i.y-t[0][1]) < 500):
                    if(pointInsidePolygon.check(p[0], p[1], t)):
                        i.x = i.oldX
                        i.y = i.oldY
            for s in supplies:
                if(abs(i.x-s.x) < 50 and abs(i.y-s.y) < 50):
                    if(pointInsidePolygon.check(p[0], p[1], s.getShape())):
                        i = s.resupply(i)
        for e in players+bots:
            for bullet in e.bullets:
                if(abs(i.x-bullet.x) < 75 and abs(i.y-bullet.y) < 75):
                    if(pointInsidePolygon.check(bullet.x, bullet.y, iShape) and not i.dead):
                        i.health -= bullet.damage
                        if(i==e):
                            i.score -= 100
                        else:
                            e.score += 100
                            if(i.health < 0):
                                e.kills += 1
                                msgs.append(["KILL: "+e.name+" | "+str(e.fireMode)+" | "+i.name, e.colour])
                            if(bullet in e.bullets):
                                e.bullets.remove(bullet)         
                for t in terrainShapes:
                    if(abs(bullet.x-t[0][0]) < 300 and abs(bullet.y-t[0][1]) < 300):
                        if(pointInsidePolygon.check(bullet.x, bullet.y, t)):
                            if(bullet in e.bullets):
                                e.bullets.remove(bullet)
                                
    for client in clients:
        client.send([players+bots, terrain+supplies, clients.index(client), msgs])
        if(not msgs == []):
            print(msgs)
    msgs = []
    
    
    if(deltaTime < 0.02):
        time.sleep(0.02-deltaTime)

