# VERSION 1.5

import colorsys
from distutils.command import install
import os
import pickle
import socket
import subprocess
import threading
import time
from urllib.request import urlopen, urlretrieve

import pygame
from pygame.surface import Surface


pygame.init()

screen = pygame.display.set_mode([int(960),int(720)])
pygame.key.set_repeat(50,50)
pygame.display.set_caption("Launcher")

running = True


# TODO: fix bot aiming, fix hitmarkers, fix hitmarker erase code, add objectives, add bot count box, show weapon bettter, powerups?, redo project structure, add mini-launcher, redo menu, add saving hosts, change thread exit code, add sound, prevent bad hue


class ClientThread(threading.Thread):
    def __init__(self, port, host, name, colour):
        super(ClientThread, self).__init__()
        self.port = port
        self.host = host
        self.name = name
        self.colour = colour
        self.running = False
        self.toKill = False
    
    def run(self):
        self.running = True
        print("Started")
        args = self.host+" "+str(self.port)+" "+self.name.replace(" ", "_")+" "+str(self.colour[0])+" "+str(self.colour[1])+" "+str(self.colour[2])
        subprocess.call("C:\Python33\python.exe Client.py "+args)
        print("DONE CLIENT")
        self.toKill = True

        
class ServerThread(threading.Thread):
    def __init__(self, port, bots):
        super(ServerThread, self).__init__()
        self.port = port
        self.bots = bots
        self.running = False
        self.toKill = False
    
    def run(self):
        self.running = True
        print("Started")
        subprocess.call("C:\Python33\python.exe Server.py "+str(self.port)+" "+str(self.bots))
        print("DONE")
        self.toKill = True


# Old colour code
# hue = 300
# while hue > 255:
#     hue = float(input("Enter hue: "))
# colour = colorsys.hsv_to_rgb(hue/255, 1, 1)




class Server:
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port
        self.selected = False
        self.surf = pygame.Surface((640, 120))
        self.x = 0
        self.y = 0
       
    def update(self,x,y):
        self.x = x
        self.y = y 
        if(self.selected):
            self.surf.fill((152,152,152))
        else:
            self.surf.fill((105,105,105))
        pygame.draw.rect(self.surf, [0,0,0], [0,0,640,120], 5)
        title = titleFont.render(self.name, 1, [255,255,255])
        subTitle = subtitleFont.render(self.host+":"+str(self.port), 1 ,[255,255,255])
        self.surf.blit(title, (20,20))
        self.surf.blit(subTitle, (20,75))
        self.rect = pygame.rect.Rect(self.x, self.y, self.surf.get_width(), self.surf.get_height())
        self.rect = pygame.rect.Rect(self.x, self.y, self.surf.get_width(), self.surf.get_height())


# Version check code
# Data format:
# VERSION x.x

servers = []
data = []

class VersionCheck(threading.Thread):
    def __init__(self):
        super(VersionCheck, self).__init__()
        self.completed = 0
        self.total = 11
    def run(self):
        global servers, data
        try:
            client = open("Client.py")
            clientVersion = client.readline()
            client.close()
            
            clientVersion = clientVersion.replace("# VERSION ", "")
            clientVersion = clientVersion.replace("\n", "")
        except:
            clientVersion = 0.0
        
        self.completed += 1
        
        try:
            server = open("Server.py")
            serverVersion = server.readline()
            server.close()
            
            serverVersion = serverVersion.replace("# VERSION ", "")
            serverVersion = serverVersion.replace("\n", "")
        except:
            serverVersion = 0.0
        
        self.completed += 1
        
        try:
            classes = open("Classes.py")
            classesVersion = classes.readline()
            classes.close()
            
            classesVersion = classesVersion.replace("# VERSION ", "")
            classesVersion = classesVersion.replace("\n", "")
        except:
            classesVersion = 0.0
        
        self.completed += 1
        print(clientVersion, serverVersion, classesVersion)
        
        
        webClient = urlopen("https://aree-vanier.github.io/python/Client.py")
        webClientContents = webClient.read().decode()
        webClientVersion = webClientContents.split("\n")[0]
        webClientVersion = webClientVersion.replace("# VERSION ", "")
        webClientVersion = webClientVersion.replace("\n", "")
        
        if(float(webClientVersion) > float(clientVersion)):
            client = open("Client.py", "w")
            client.write(webClientContents)
            client.close()
        
        webClient.close()
        
        self.completed += 1
        
        webServer = urlopen("https://aree-vanier.github.io/python/Server.py")
        webServerContents = webServer.read().decode()
        webServerVersion = webServerContents.split("\n")[0]
        webServerVersion = webServerVersion.replace("# VERSION ", "")
        webServerVersion = webServerVersion.replace("\n", "")
        
        if(float(webServerVersion) > float(serverVersion)):
            server = open("Server.py", "w")
            server.write(webServerContents)
            server.close()
        
        webServer.close()
        
        self.completed += 1
        
        webClasses = urlopen("https://aree-vanier.github.io/python/Classes.py")
        webClassesContents = webClasses.read().decode()
        webClassesVersion = webClassesContents.split("\n")[0]
        webClassesVersion = webClassesVersion.replace("# VERSION ", "")
        webClassesVersion = webClassesVersion.replace("\n", "")
        
        if(float(webClassesVersion) > float(classesVersion)):
            classes = open("Classes.py", "w")
            classes.write(webClassesContents)
            classes.close()
        
        webClasses.close()
        
        self.completed += 1
                
        print(webClientVersion, webServerVersion, webClassesVersion)
        
        
        if(not os.path.exists("pointInsidePolygon.py")):
            pip = open("pointInsidePolygon.py", "w")
            webpip = urlopen("https://aree-vanier.github.io/python/pointInsidePolygon.py")
            pip.write(webpip.read().decode())
            webpip.close()
            pip.close()
            
        self.completed += 1
        
        if(not os.path.exists("gregJoy.py")):
            gj = open("gregJoy.py", "w")
            webgj = urlopen("https://aree-vanier.github.io/python/gregJoy.py")
            gj.write(webgj.read().decode())
            webgj.close()
            gj.close()
        
        self.completed += 1
        
        if(not os.path.exists("gregJoy.py")):
            gj = open("gregJoy.py", "w")
            webgj = urlopen("https://aree-vanier.github.io/python/gregJoy.py")
            gj.write(webgj.read().decode())
            webgj.close()
            gj.close()
        
        self.completed += 1
        
        if(not os.path.exists("data-latin.ttf")):
            urlretrieve("https://aree-vanier.github.io/python/data-latin.ttf", "data-latin.ttf")
        
        self.completed += 1
        
        
#         servers,data = pickle.loads(open("launcher.cfg",'r'))
#         saveFile.close()
# #         except:
        servers = [Server("Local Machine", socket.gethostname(), 1111), Server("Greg", "KCV-INLABA03FE2", 1111)]
        data = ["Name","0"]
        self.completed += 1
        

vc = VersionCheck()
vc.start()
font = pygame.font.Font("data-latin.ttf", 30)
while True:
    screen.fill([0,0,0])
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
    out = "Completed "+str(vc.completed) + "/" + str(vc.total)+" actions" 
    outSurf = font.render(out, 1, [255,255,255])
    screen.blit(outSurf, (screen.get_width()/2-outSurf.get_width()/2, screen.get_height()/2-outSurf.get_height()/2))
    pygame.display.flip()
    if(vc.completed == vc.total):
        vc.join(1)
        break;

class TextField:
    def __init__(self, x, y, default, type, limit, label):
        self.label = label
        self.x = x
        self.y = y
        self.text = default
        self.type = type
        self.limit = limit
        self.font = pygame.font.Font("data-latin.ttf", 25)
        self.sizeTest = self.font.render("W"*limit, 1, [0,0,0])
        self.labelSurf = self.font.render(self.label, 1, [255,255,255])
        self.width = self.sizeTest.get_width()+10+self.labelSurf.get_width()+10
        self.height = self.sizeTest.get_height()+10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.focused = False
        self.surface = pygame.Surface((self.width, self.height))
        
    def draw(self, surface):
        self.text.replace("|", "")
        self.surface.fill([0,0,0])
        pygame.draw.rect(self.surface, [132,132,132], [self.labelSurf.get_width()+5,0, 1000, 100], 0)
        removeLine = False
        if(self.focused and len(self.text) < self.limit):
            self.text += "|"
            removeLine = True
        textSurf = self.font.render(self.text, 1, [255,255,255])
        if(removeLine):
            self.text = self.text[0:len(self.text)-1]
        self.surface.blit(self.labelSurf, (5,5))
        self.surface.blit(textSurf, [self.labelSurf.get_width()+10,5])
        surface.blit(self.surface, (self.x, self.y))
        
        
class Button:
    def __init__(self, x, y, label, fontsize):
        if(fontsize == 0):
            fontsize = 25
        self.x = x
        self.y = y
        self.label = label
        self.font = pygame.font.Font("data-latin.ttf", fontsize)
        self.sizeTest = self.font.render(self.label, 1, [0,0,0])
        self.surface = pygame.Surface((self.sizeTest.get_width()+10, self.sizeTest.get_height()+10))
        self.rect = pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())
        
    def draw(self, surface):
        self.surface.fill([132,132,132])
        textSurf = self.font.render(self.label, 1, [255,255,255])
        self.surface.blit(textSurf, [5,5])
        surface.blit(self.surface, (self.x, self.y))





focusedField = None
fields1 =[TextField(10,10,"Server", 0, 30, "Name:"),TextField(10,60,"", 0, 30, "Hostname:"),TextField(10,110,"1111",1,4, "Port:")]
fields2 =[TextField(10,10,data[0],0,16, "Username:"),TextField(10,60,data[1],1,3,"Hue:")]
fields3 =[TextField(10,10,"1111",1,4,"Port:"), TextField(10,60,"0",1,2, "Bots:")]

launchServerButton = Button(10, 110, "Launch Server",0 )
addServerButton = Button(0,0, "Add Server", 0)
confirmAddServerButton = Button(10, 160, "Add Server", 0)
view2ConfirmButton = Button(10, 110, "Confirm", 0)
view2Button = Button(0,50,"View 2",0 )
cancelButton = Button(10, 210, "Cancel",0)
hostServerButton = Button(0,680,"Host Server",0)
playButton = Button(0,600,"Connect", 75)
playButton.x = screen.get_width()/2-playButton.rect.width
playButton.rect.x = playButton.x
playButton.rect.y = playButton.y

ct = ClientThread(1111, "KCV-INLABA03FE2", "NAME", 1)
st = ServerThread(1111, 0)

titleFont = pygame.font.Font("data-latin.ttf", 26)
subtitleFont = pygame.font.Font("data-latin.ttf", 18)






selectedServer = servers[0]
selectedServer.selected = True

serverSurf = pygame.Surface((640,480))
def drawServers():
    global servers
    serverSurf.fill((105,105,105))
    for server in servers:
        server.update(160, 120*servers.index(server)+80)
        serverSurf.blit(server.surf, (0,120*servers.index(server)))
        
    
    screen.blit(serverSurf, (160, 80))

def view1():
    for field in fields1:
        field.draw(screen)
    confirmAddServerButton.draw(screen)
    cancelButton.draw(screen)

def view2():
    for field in fields2:
        field.draw(screen)
            
    try:
        pass
        colour = colorsys.hsv_to_rgb(int(fields2[1].text)/255, 1, 1)
        pygame.draw.rect(screen, [int(colour[0]*255), int(colour[1]*255), int(colour[2]*255)], [560,0,400,400], 0)
    except:
        pass
    view2ConfirmButton.draw(screen)
    cancelButton.draw(screen)

def view3():
    for field in fields3:
        field.draw(screen)
    launchServerButton.draw(screen)
    cancelButton.draw(screen)

# Starting Code:
##print("CT+ST")
##                st.port = int(fields[1].text)
##                st.start()
##                time.sleep(2.5)
#                 ct.host = fields[0].text
#                 ct.port = int(fields[1].text)
#                 ct.name = fields[2].text
#                 ct.colour = colorsys.hsv_to_rgb(int(fields[3].text)/255, 1, 1)
#                 ct.colour = [int(ct.colour[0]*255), int(ct.colour[1]*255), int(ct.colour[2]*255)]
#                 ct.start()


## View 0 is main, view 1 is add server, view 2 is change name/colour, view 3 is to lauch a server
view = 0



while running:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        if(event.type == pygame.KEYUP and not focusedField == None):
            if(event.key == pygame.K_BACKSPACE):
                focusedField.text = focusedField.text[0:len(focusedField.text)-1]
            else:
                if(not focusedField == None and not (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT) and len(focusedField.text) < focusedField.limit):
                    if(event.key == pygame.K_SPACE):
                        focusedField.text+=" "
                    else:
                        focusedField.text += pygame.key.name(event.key)
        if(event.type == pygame.MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            if(view == 0):
                if(addServerButton.rect.collidepoint(pos)):
                    view = 1
                    focusedField = None
                if(view2Button.rect.collidepoint(pos)):
                    view = 2
                    focusedField = None
                if(hostServerButton.rect.collidepoint(pos)):
                    view = 3
                    focusedField = None
                if(playButton.rect.collidepoint(pos)):
                    ct.host = selectedServer.host
                    ct.port = int(selectedServer.port)
                    ct.name = fields2[0].text
                    ct.colour = colorsys.hsv_to_rgb(int(fields2[1].text)/255, 1, 1)
                    ct.colour = [int(ct.colour[0]*255), int(ct.colour[1]*255), int(ct.colour[2]*255)]
                    ct.start()
                for server in servers:
                    if(server.rect.collidepoint(pos)):
                        print("server: "+str(servers.index(server)))
                        server.selected = True
                        selectedServer.selected = False
                        selectedServer = server
            if(view == 1):
                for field in fields1:
                    if(field.rect.collidepoint(pos)):
                        if(not focusedField == None):
                            focusedField.focused = False
                        field.focused = True
                        focusedField = field
                if(confirmAddServerButton.rect.collidepoint(pos)):
                    servers.append(Server(fields1[0].text, fields1[1].text, fields1[2].text))
                    view = 0
                    focusedField = None
            if(view == 2):
                for field in fields2:
                    if(field.rect.collidepoint(pos)):
                        if(not focusedField == None):
                            focusedField.focused = False
                        field.focused = True
                        focusedField = field
                if(view2ConfirmButton.rect.collidepoint(pos)):
                    view = 0
                    focusedField = None
            if(view == 3):
                for field in fields3:
                    if(field.rect.collidepoint(pos)):
                        if(not focusedField == None):
                            focusedField.focused = False
                        field.focused = True
                        focusedField = field
                if(view2ConfirmButton.rect.collidepoint(pos)):
                    st.port = int(fields3[0].text)
                    st.bots = int(fields3[1].text)
                    st.start()
                    view = 0
                    focusedField = None
            if(not view == 0):
                if(cancelButton.rect.collidepoint(pos)):
                    view = 0
                    focusedField = None

                
    
    
    screen.fill([0,0,0])


    
    if(view == 0):
        drawServers()
        addServerButton.draw(screen)
        view2Button.draw(screen)
        playButton.draw(screen)
        hostServerButton.draw(screen)
    if(view == 1):
        view1()
    if(view == 2):
        view2()
    if(view == 3):
        view3()
        
        
    
    pygame.display.flip()
    
    
    
    
    
    if(ct.toKill): ct = ClientThread(1111, "KCV-INLABA03FE2", "Name", 1)
    if(st.toKill): st = ServerThread(1111, 0)
                

saveFile = open("launcher.cfg", 'wb')
saveFile.write(pickle.dumps([servers, [fields2[0], fields2[1]]]))
saveFile.close()
pygame.quit()
exit()
