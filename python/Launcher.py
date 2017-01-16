# VERSION 1.1

import colorsys
from distutils.command import install
import os
import subprocess
import threading
import time
from urllib.request import urlopen, urlretrieve

import pygame
from pygame.surface import Surface


pygame.init()

screen = pygame.display.set_mode([640,480])
pygame.key.set_repeat(50,50)
pygame.display.set_caption("Launcher")

running = True





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
    def __init__(self, port):
        super(ServerThread, self).__init__()
        self.port = port
        self.running = False
        self.toKill = False
    
    def run(self):
        self.running = True
        print("Started")
        subprocess.call("C:\Python33\python.exe Server.py "+str(self.port))
        print("DONE")
        self.toKill = True


# Old colour code
# hue = 300
# while hue > 255:
#     hue = float(input("Enter hue: "))
# colour = colorsys.hsv_to_rgb(hue/255, 1, 1)


class TextField:
    def __init__(self, x, y, default, type, limit):
        self.x = x
        self.y = y
        self.text = default
        self.type = type
        self.limit = limit
        self.font = pygame.font.Font("data-latin.ttf", 25)
        self.sizeTest = self.font.render("W"*limit, 1, [0,0,0])
        self.width = self.sizeTest.get_width()+10
        self.height = self.sizeTest.get_height()+10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.focused = False
        self.surface = pygame.Surface((self.width, self.height))
        
    def draw(self, surface):
        self.text.replace("|", "")
        self.surface.fill([132,132,132])
        removeLine = False
        if(self.focused and len(self.text) < self.limit):
            self.text += "|"
            removeLine = True
        textSurf = self.font.render(self.text, 1, [255,255,255])
        if(removeLine):
            self.text = self.text[0:len(self.text)-1]
        self.surface.blit(textSurf, [5,5])
        surface.blit(self.surface, (self.x, self.y))
        
        
class Button:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.font = pygame.font.Font("data-latin.ttf", 25)
        self.sizeTest = self.font.render(self.label, 1, [0,0,0])
        self.surface = pygame.Surface((self.sizeTest.get_width()+10, self.sizeTest.get_height()+10))
        self.rect = pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())
        
    def draw(self, surface):
        self.surface.fill([132,132,132])
        textSurf = self.font.render(self.label, 1, [255,255,255])
        self.surface.blit(textSurf, [5,5])
        surface.blit(self.surface, (self.x, self.y))




# Version check code
# Data format:
# VERSION x.x

class VersionCheck(threading.Thread):
    def __init__(self):
        super(VersionCheck, self).__init__()
        self.completed = 0
        self.total = 10
    def run(self):
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
        print(clientVersion + " " + serverVersion + " " + classesVersion)
        
        
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



focusedField = None
fields =[TextField(10,10,"KCV-INLABA03FE2", 0, 20),TextField(10,60,"1111",1,4),TextField(10,110,"Name",0,16),TextField(10,160,"Hue",1,3)]

clientButton = Button(10, 250, "Launch Client")
serverButton = Button(10, 300, "Launch Server")


ct = ClientThread(1111, "KCV-INLABA03FE2", "NAME", 1)
st = ServerThread(1111)
while running:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        if(event.type == pygame.KEYUP):
            if(event.key == pygame.K_BACKSPACE):
                focusedField.text = focusedField.text[0:len(focusedField.text)-1]
            else:
                if(not focusedField == None and not (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT) and len(focusedField.text) < focusedField.limit):
                    if(event.key == pygame.K_SPACE):
                        focusedField.text+=" "
                    else:
                        focusedField.text += pygame.key.name(event.key)
                    
        if(event.type == pygame.MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            for field in fields:
                if(field.focused and not focusedField == field):
                    field.focused = False
                if(field.rect.collidepoint(pos)):
                    field.focused = True
                    focusedField = field
            if(clientButton.rect.collidepoint(pos) and not ct.running):
                print("CT")
                ct.host = fields[0].text
                ct.port = int(fields[1].text)
                ct.name = fields[2].text
                ct.colour = colorsys.hsv_to_rgb(int(fields[3].text)/255, 1, 1)
                ct.colour = [int(ct.colour[0]*255), int(ct.colour[1]*255), int(ct.colour[2]*255)]
                ct.start()
            if(serverButton.rect.collidepoint(pos) and not ct.running and not st.running):
                print("CT+ST")
                st.port = int(fields[1].text)
                st.start()
                time.sleep(2.5)
                ct.host = fields[0].text
                ct.port = int(fields[1].text)
                ct.name = fields[2].text
                ct.colour = colorsys.hsv_to_rgb(int(fields[3].text)/255, 1, 1)
                ct.colour = [int(ct.colour[0]*255), int(ct.colour[1]*255), int(ct.colour[2]*255)]
                ct.start()
        
    
    
    screen.fill([0,0,0])
    for field in fields:
        field.draw(screen)
        
    try:
        colour = colorsys.hsv_to_rgb(int(fields[3].text)/255, 1, 1)
        pygame.draw.rect(screen, [int(colour[0]*255), int(colour[1]*255), int(colour[2]*255)], [540,0,100,100], 0)
    except:
        pass
    
    clientButton.draw(screen)
    serverButton.draw(screen)
    
    pygame.display.flip()
    
    
    
    
    
    if(ct.toKill): ct = ClientThread(1111, "KCV-INLABA03FE2", "Name", 1)
    if(st.toKill): st = ServerThread(1111)
                

pygame.quit()
exit()
