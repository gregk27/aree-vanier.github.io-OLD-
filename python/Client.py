# VERSION 3.5
import pickle, sys, threading, pygame, socket, gregJoy #@UnusedImports

from Classes import *  # @UnusedWildImport


pygame.init()
gregJoy.init()


args = sys.argv
print(args)

map = pygame.Surface((5000, 5000))   #@ReservedAssignment
nameFont = pygame.font.Font("Resources/res/data-latin.ttf", 25)
menuFont = pygame.font.Font("Resources/res/data-latin.ttf", 50)
connected = False


tabMenuOn = False
showNames = True

messages = []

sock = socket.socket()

print(socket.gethostname())

#Set up username and colour to send to server
userName = args[3].replace("_", " ")
print(args[4:7])
colour = [float(args[4]),float(args[5]),float(args[6]),]
dataString = ""
dataString+=(userName)
dataString+=("|")
dataString+=(str(int(colour[0]))+"\\")
dataString+=(str(int(colour[1]))+"\\")
dataString+=(str(int(colour[2])))
print(dataString)


#Connect to server
while not connected:
    host = args[1]
    port =  int(args[2])
    try:
        print("Connecting")
        sock.connect((host, port))
        if(sock.recv(512).decode() == "Connected"):
            print("Connected")
            connected = True
            sock.sendall(dataString.encode())
            print(str(sock.recv(512).decode))
        else:
            print("Connection Failed")
    except:
        print("Connection Failed")



#Thread to get controls and send to server
class GetControls(threading.Thread):
    def __init__(self):
        super(GetControls, self).__init__()
        #delay for showNames toggle
        self.delay = 0
    
    def run(self):
        global tabMenuOn, showNames, connected
        while connected:
            self.delay -= 1
            try:
                pygame.event.pump()
    
                keys = pygame.key.get_pressed()
                if(keys[pygame.K_TAB]):
                    tabMenuOn = True
                else:
                    tabMenuOn = False
                if(keys[pygame.K_q] and self.delay < 0):
                    showNames = not showNames
                    self.delay = 1000
                joy = None
                if(len(gregJoy.joysticks) > 0):
                    joy = gregJoy.check(gregJoy.joysticks[0])
                data = [keys, joy]
                sock.sendall(pickle.dumps(data))
            except:
                pass

gc = GetControls()
gc.start()
 
WIDTH, HEIGHT = pygame.display.list_modes()[0]
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

#set up hitmarkers
hitmarkers = pygame.Surface((100,100))
pygame.draw.line(hitmarkers, [255,255,255], [0,0], [1000,1000], 5)
pygame.draw.line(hitmarkers, [255,255,255], [90,0], [0,90], 5)
pygame.draw.circle(hitmarkers, [0,0,0], (int(hitmarkers.get_width()/2), int(hitmarkers.get_height()/2)), 35, 0)



#Draw tab menu
tabMenuSurface = pygame.Surface((640, 480))
headers = ["NAME", "  POINTS  ", "  KILLS  ", "  DEATHS  "]
def tabMenu(players):
    #Sort a local copy of players based on score
    players = sorted(players, key=lambda x: x.score, reverse=True)
    
    tabMenuSurface.set_alpha(192)
    tabMenuSurface.fill([169,169,169])
    height = 0
    width = 0
    nameWidthSurf = nameFont.render("WWWWWWWWWWWWWWWW", 1, [0,0,0])
    headerWidths = []
    
    for head in headers:
        surf = nameFont.render(head, 1, [255,255,255])
        if(head == "NAME"):
            tabMenuSurface.blit(surf, (width+nameWidthSurf.get_width()/2, height))
            width += nameWidthSurf.get_width()
        else:
            tabMenuSurface.blit(surf, (width, height))
            width += surf.get_width()
        headerWidths.append(surf.get_width())
    height += nameWidthSurf.get_height()+5
    pygame.draw.line(tabMenuSurface, [255,255,255], [0,height], [tabMenuSurface.get_width(), height])
    height += 5
    
    for player in players:
        width = 0
        surf = nameFont.render(player.name, 1, player.colour)
        tabMenuSurface.blit(surf, (width, height))
        width += nameWidthSurf.get_width()
        
        surf = nameFont.render(str(player.score), 1, player.colour)
        tabMenuSurface.blit(surf, (width+headerWidths[1]/2, height))
        width += headerWidths[1]
        
        surf = nameFont.render(str(player.kills), 1, player.colour)
        tabMenuSurface.blit(surf, (width+headerWidths[2]/2, height))
        width += headerWidths[2]
        
        surf = nameFont.render(str(player.deaths), 1, player.colour)
        tabMenuSurface.blit(surf, (width+headerWidths[3]/2, height))
        width += headerWidths[3]
        
        height += nameWidthSurf.get_height()+5
        pygame.draw.line(tabMenuSurface, [255,255,255], [0,height], [tabMenuSurface.get_width(), height])
        height += 5
        
        
    screen.blit(tabMenuSurface, (WIDTH/2-tabMenuSurface.get_width()/2, HEIGHT/2-tabMenuSurface.get_height()/2))
    


toQuit = False



print("Connected:", connected)
while connected:
    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                print("ESCAPE")
                connected = False
                print("Connected Status")
    try:
        data = sock.recv(32786)
        data = pickle.loads(data)
    except:
        continue

    
    players, terrain, ID, msgs = data
    #Copy messages locally
    if(not msgs == []):
        print(msgs)
    if(len(msgs) > 0):
        for msg in msgs:
            messages.append([msg[0], msg[1], 250])
            
    localPlayer = players[ID]
    pos = pygame.mouse.get_pos()
    mouseX = localPlayer.x+(pos[0]-WIDTH/2)
    mouseY = localPlayer.y+(pos[1]-HEIGHT/2)
    screen.fill([255,255,255])
    
    #Gridlines
    for x in range(0,5000,1000):
        pygame.draw.line(map, [255,255,255], (x,0), (x,5000), 2)
            
    for y in range(0,5000,1000):
        pygame.draw.line(map, [255,255,255], (0,y), (5000,y), 2)
    
    #Hitmarkers
    if(localPlayer.hitMarkers > 0):
        map.blit(hitmarkers, (localPlayer.x-hitmarkers.get_width()/2, localPlayer.y-hitmarkers.get_height()/2))
        localPlayer.hitMarkers -= 1
        
    #Draw players and bots +bullets
    for player in players:
        player.draw(map)
        for bullet in player.bullets:
            bullet.draw(map)
        #Show nametags on all non local player tanks if showNames is toggled
        if(showNames and not player == localPlayer):
            surf = nameFont.render(str(player.name), 1, player.colour)
            map.blit(surf, (player.x-surf.get_width()/2, player.y-surf.get_height()/2-15))
            pygame.draw.rect(map, [255,0,0], [player.x-50, player.y-5, 100,10], 0)
            if(player.health > 0):
                pygame.draw.rect(map, [0,255,0], [player.x-50, player.y-5, player.health/10,10], 0)
            
        #Draw nametag if hover over tank
        else:
            if(abs(mouseX-player.x) < 37 and abs(mouseY-player.y) < 37):
                surf = nameFont.render(str(player.name), 1, player.colour)
                map.blit(surf, (mouseX-surf.get_width()/2, mouseY-surf.get_height()/2-15))
                pygame.draw.rect(map, [255,0,0], [mouseX-50, mouseY-5, 100,10], 0)
                if(player.health > 0):
                    pygame.draw.rect(map, [0,255,0], [mouseX-50, mouseY-5, player.health/10,10], 0)
    
    #Draw terrain and supply drops
    for t in terrain:
        if(type(t) == Supply):
            if(localPlayer not in t.hasSupplied):
                t.draw(map)
        else:    
            t.draw(map)
    
    
    print("DRAWING")
    #Draw the map to the screen
    screen.blit(map, (-localPlayer.x+WIDTH/2, -localPlayer.y+HEIGHT/2))
    #Prep the minimap
    pygame.draw.rect(map, [255,255,255], (localPlayer.x-WIDTH/2, localPlayer.y-HEIGHT/2, WIDTH, HEIGHT), 25)
    for player in players:
        pygame.draw.circle(map, player.colour, (int(player.x), int(player.y)), 35, 0)
    minimap = pygame.transform.scale(map, (250, 250))
    screen.blit(minimap, (0,0))
    pygame.draw.rect(screen, [255,255,255], [0, 0, minimap.get_width(), minimap.get_height()], 1)
    pygame.draw.rect(map, [0,0,0], (localPlayer.x-WIDTH/2, localPlayer.y-HEIGHT/2, WIDTH, HEIGHT), 25)
    

    
    #Erase code#
    for player in players:
        pygame.draw.circle(map, [0,0,0], (int(player.x), int(player.y)), 35, 0)
        for bullet in player.bullets:
            pygame.draw.circle(map, [0,0,0], (int(bullet.x), int(bullet.y)), 5, 0)
        if(showNames):
            pygame.draw.rect(map, [0,0,0], [player.x-150, player.y-50, 300, 100], 0)
    pygame.draw.rect(map, [0,0,0], [mouseX-150, mouseY-50, 300,70], 0)
    
    pygame.draw.rect(screen, [255,0,0], [WIDTH/2-500,0,1000,25], 0)
    if(localPlayer.health > 0):
        pygame.draw.rect(screen, [0,255,0], [WIDTH/2-500,0,localPlayer.health,25], 0)
    for t in terrain:
        if(type(t) == Supply):
            pygame.draw.rect(map, [0,0,0], [t.x-50, t.y-50, 100, 100], 0)
            pass
    
    #Draw ammo count
    ammo = menuFont.render(str(localPlayer.clip)+"/"+str(localPlayer.ammo)+"/"+str(localPlayer.fireMode+1), 1, [255,255,255], [0,0,0])
    ammox = 10
    ammoy = HEIGHT-ammo.get_height()-50
    screen.blit(ammo, (ammox, ammoy))
    
    
    #Animate reloading circle
    if(localPlayer.reloadTimer > 0):
        arcx = ammox-8
        arcy = ammoy+ammo.get_rect()[3]/2-(ammo.get_rect()[2]-10)/2
        arch = ammo.get_rect()[2]+10
        arcw = ammo.get_rect()[2]+10
        pygame.draw.arc(screen, [255,255,255], [arcx, arcy, arcw, arch], 0, math.radians(360-(localPlayer.reloadTimer*3)), 3)
    
    #Draw tab menu
    if(tabMenuOn):
        tabMenu(players)
        
    
    if(localPlayer.dead):
        surf = menuFont.render("You Died!", 1, localPlayer.colour)
        screen.blit(surf, (WIDTH/2-surf.get_width()/2, 250))
        surf = menuFont.render("Press R to retry", 1, localPlayer.colour)
        screen.blit(surf, (WIDTH/2-surf.get_width()/2, HEIGHT/2-surf.get_height()*1.5))
        surf = menuFont.render("Press ESCAPE to quit", 1, localPlayer.colour)
        screen.blit(surf, (WIDTH/2-surf.get_width()/2, HEIGHT/2+surf.get_height()*1.5))
    
    #Draw messages
    msgY = HEIGHT
    for message in messages:
        message[2] -= 1;
        if(message[2] < 0):
            messages.remove(message)
        else:
            surf = menuFont.render(message[0], 1, message[1])
            msgY -= surf.get_height()+25
            screen.blit(surf, (WIDTH-surf.get_width()-25, msgY))
    
    
    pygame.display.flip()

#Exit code
print("NOTHING")
sock.close()
print("Socket")
try:
    gc.join(0.5)
    print("Threads")
except:
    print("ERROR")
pygame.quit()
print("Pygame")
exit(0)



