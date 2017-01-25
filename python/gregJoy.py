                        ##############################
                        #         GregJoy            #
                        #   Free joystick support    #
                        #     By Gregory Kelly       #
                        #       DO NOT EDIT          #
                        ##############################
import sys

import pygame


joysticks = []

pygame.joystick.init()
pygame.init()


# Variables for locations in list #
AXIS_PITCH = 1
AXIS_ROLL = 0
AXIS_THROTTLE = 2
BUTTON_TRIGGER = BUTTON_1 = 3
BUTTON_2 = 4
BUTTON_3 = 5
BUTTON_4 = 6
BUTTON_5 = 7
BUTTON_6 = 8
BUTTON_7 = 9
BUTTON_8 = 10
BUTTON_9 = 11
BUTTON_10 = 12
BUTTON_11 = 13





# Must be called first, initializes joysticks #
def init():
    print("Thank you for using GregJoy. Joystick support brought to you by Gregory Kelly")
    for joy in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(joy))
        joysticks[joy].init()
        
        
# Needs player count, surface to draw to, nameFont to use, colour of text OR list of colours to use, dimesions of screen. WARNING WILL OVERRIDE MAIN CODE WHILE IN EFFECT #
def assign(players, screen, nameFont, colour, dimensions):
    unassigned = joysticks.copy()
    toReturn = []
    for i in range(players):
        assigned = False
        while(not assigned):
            pygame.event.pump()
            if(pygame.key.get_pressed()[pygame.K_ESCAPE]): pygame.quit(); sys.exit();
            screen.fill([0,0,0])
            outString = "Player "+str(i+1)+" pull the trigger"
            if(type(colour) is list):
                out = nameFont.render(outString, 1, colour[i], None)
            else:
                out = nameFont.render(outString, 1, colour, None)
            screen.blit(out, (dimensions[0]/2-out.get_width()/2, dimensions[1]/2-out.get_height()/2))
            pygame.display.flip()
            if(len(unassigned) == 0):
                break
            for stick in unassigned:
                if(stick.get_button(0) == 1):
                    if(stick not in toReturn):
                        toReturn.append(stick)
                        unassigned.remove(stick)
                        assigned = True
    return(toReturn)


# Returns the values of three axis, and 5 buttons on the passed joystick
def check(joystick):
    if(joystick == None): return([0,0,0,0,0,0,0,0])
    toReturn = []
    toReturn.append(joystick.get_axis(0))
    toReturn.append(joystick.get_axis(1))
    toReturn.append(joystick.get_axis(2))
    for i in range(0,11):
        toReturn.append(joystick.get_button(i))
    return(toReturn)
