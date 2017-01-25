# VERSION 3

import random, time, pygame, sys, socket, threading, gregJoy, pointInsidePolygon, pickle  # @UnusedImport

from Classes import *  # @UnusedWildImport


## Change spawns - distance from location
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




#Initiate socket
sock = socket.socket()
port = int(args[1])
host = socket.gethostname()
sock.bind((host, port))
print("Server hosted on:", host+":"+str(port))



#Create bots
names = ["mybot.ca", "Another bot", "Dat Bot Doe", "Bot051144", "ThisIsNotABot", "Sake!", "Michael Botjayi", "Bots-R-Us", "xXx_ambotr_xXx", "You're Winner!", "TheQuickBrownFox", "The good", "The bad", "The ugly ;(", "xXx_proreaps_xXx", "ProGenji", "Bot Cnena", "Glitchy", "WhyDoYouStruggle", "The Bot Johnson"]
bots = []

for i in range(0,int(args[2])):
    print("new bot")
    bots.append(Bot(random.randint(0,4900),random.randint(0,4900),tankShape, [255,255,255], random.choice(names), 5000))


players = []
clients = []
msgs = []

DEADZONE = 0.25

#Thread created for each client, handles all communications
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
            try:
                data = pickle.loads(self.client.recv(2048))
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
                if(keys[pygame.K_1]): player.fireMode = 0
                if(keys[pygame.K_2]): player.fireMode = 1
                if(keys[pygame.K_3]): player.fireMode = 2
                if(keys[pygame.K_4]): player.fireMode = 3
                if(keys[pygame.K_END] and player.health > 900 and player.ammo > player.maxAmmo-player.maxClip-10): 
                    player.deaths += 1
                    player.revive(random.randint(100, 4900),random.randint(100, 4900))
                        
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
                    
    def send(self, data):
        global msgs
        #Kick after failed connection
        if(self.fails >= 2):
            msgs.append(["SERVER: "+players[clients.index(self)].name+" disconnected", players[clients.index(self)].colour])
            players.pop(clients.index(self))
            clients.remove(self)
            print("CLIENT REMOVED")
        
        #Try to send data
        try:
            sendout = pickle.dumps(data)
            self.client.sendall(sendout)
            self.fails = 0
        except:
            print("send failed", self.fails)
            self.fails += 1


#Thread that is always running to check for new client connections
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

#initializes classes
init(mapSize)


running = True
currentTime = time.time()

#Creates shapes for terrain
terrainShapes = [
    [[0,0],[10,0],[10,36],[46,36],[46,46],[0,46]],
    [[0,0],[36,36],[0,36]],
    [[0,0],[36,0],[36,36],[0,36]],
    [[0,0],[72,0],[72,10],[0,10]]
    ]

#Generates terrain: random x, y, rotation, and size
terrain = []
terrainShape = []
for i in range(random.randint(15,17)):
    t = Terrain(random.randint(0,4900),random.randint(0,4900), random.choice(terrainShapes), random.randint(3,6), random.randint(0,360))
    print(t.x, t.y, t.scale)
    terrainShapes.append(t.getShape())
    terrain.append(t)
print(len(terrain))

#Initiates supply drops
supplies = []
lastDrop = time.time()



while running:
    #Calculate delta time
    oldTime = currentTime
    currentTime = time.time()
    deltaTime = currentTime - oldTime
    
    #Move bots
    if(len(players) > 0):
        for bot in bots:
            if(bot.dead):
                bot.revive(len(players))
            else:
                bot.move(players+bots, 0.060)
                if(bot.health < 0):
                    bot.dead = True   
            
            for bullet in bot.bullets:
                if(bullet.life > 0):
                    bullet.move()
                else:
                    bot.bullets.remove(bullet)
                    
    #Move players
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
    
    #Create supply drop every minute
    if(time.time() - lastDrop >= 60):
        supplies.append(Supply(random.randint(0,4900),random.randint(0,4900), 2500))
        lastDrop = time.time()
        msgs.append(["SERVER: SUPPLY DROP", [255,255,255]])
    
    #Update supply drop
    for s in supplies:
        s.update()
        if(s.life == 0):
            supplies.remove(s)

    
    #Collision detection
    for i in players+bots:
        iShape =  i.getShape(i.hitbox, i.angle)
        
        for p in iShape: 
            
            #Against terrain
            for t in terrainShapes:
                if(abs(i.x-t[0][0]) < 500 and abs(i.y-t[0][1]) < 500):
                    if(pointInsidePolygon.check(p[0], p[1], t)):
                        i.x = i.oldX
                        i.y = i.oldY
                        
            #Against supplies
            for s in supplies:
                if(abs(i.x-s.x) < 50 and abs(i.y-s.y) < 50):
                    if(pointInsidePolygon.check(p[0], p[1], s.getShape())):
                        i = s.resupply(i)
        
        for e in players+bots:
            #Againts bullets
            for bullet in e.bullets:
                if(abs(i.x-bullet.x) < 75 and abs(i.y-bullet.y) < 75):
                    if(pointInsidePolygon.check(bullet.x, bullet.y, iShape) and i.health > -1):
                        i.health -= bullet.damage
                        if(i==e):
                            i.score -= 100
                        else:
#                             e.hitMarkers = 10
                            e.score += 25
                            if(i.health < 0):
                                e.kills += 1
                                e.score += 500
                                msgs.append(["KILL: "+e.name+" | "+str(e.fireMode)+" | "+i.name, e.colour])
                            if(bullet in e.bullets):
                                e.bullets.remove(bullet)  
                #Check bullet against terrain (done here to reduce amount of loops)
                for t in terrainShapes:
                    if(abs(bullet.x-t[0][0]) < 300 and abs(bullet.y-t[0][1]) < 300):
                        if(pointInsidePolygon.check(bullet.x, bullet.y, t)):
                            if(bullet in e.bullets):
                                e.bullets.remove(bullet)
    
    #Send data to clients            
    for client in clients:
        client.send([players+bots, terrain+supplies, clients.index(client), msgs])
        if(not msgs == []):
            print(msgs)
    msgs = []
    
    
    if(deltaTime < 0.02):
        time.sleep(0.02-deltaTime)

