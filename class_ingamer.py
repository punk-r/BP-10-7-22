import pygame
clock = pygame.time.Clock()
import sys
import os.path
from os import path
import support_functions
from support_functions import *

#--------------------------------------------------------------------------------------------class ingamer
# parent class pro pohybujici se objekty v hre                                                # ingamer predek i pro reff a coach?? zjednodusil by se kod
class ingamer(pygame.sprite.Sprite):
    def __init__(self,new_position):
        #self.position = new_position
        self.path_target = 0
        self.velocity = [1,0]
        self.radius = 15
        self.image = "notset"
        self.rect = pygame.Rect( new_position[0],new_position[1], self.radius * 2, self.radius * 2)
        self.rect.center = new_position

    step = 2
    destination_move = [0,0]                                                                            #uzito?
    #lab_mode_b = 1
    color = BLUE
    collision_allowed_b = False
    selected_b = False
    team_type = "Neutral"          # H - human ,  AI , Neutral for ball and reff
    field_site = "neutral"         # L team ma vlastni branu na levo, R team ma vlastni branu na pravo
    reinforsment = False

    '''
    1.uhel pocitame od brany sveho teamu , kdyz hrac stoji v uhlu 180 ,znamena ze je 'zady' k brane
    2.hrac se muze nastavit pouze jednim smerem to znamena kdyz chci nastavit -20 supnu musim uzit 340   (360 -20)
    pokud je brana v pravo uhly se zrcadli aby platilo pravidlo 1



    field_site = L
                             90
    b                  0.     |     1.
    r                         |
    a               0 ------------------ 180
    n                         |
    a                   3.    |     2.
                             270

    field_site = R
                             90
                       1.     |     0.                b
                              |                       r
                 180 ------------------ 0             a
                              |                       n
                        2.    |     3.                a
                             270


    '''

    # vypocte uhel k druhemu objektu(nebo novy smer) , a to v zavislosti na field_site
    def calculate_angle_to_other_object(self,new_target):
        # pozice newtarget k 'sobe'

        # urceni qvadrantu
        below = True
        left = True

        # error hodnota pro pripad ze ew target je uvnit radiusu hrace => hrac bude natocen k souperove brane
        # nelze nastavit target blizez k hraci nez radius
        new_angle = 180

        # vypocet vzdalenosti
        target_adjescent =  abs (self.rect.center[0] -  new_target[0])
        target_opposite =  abs (  self.rect.center[1] -  new_target[1])
        target_hypotensue = sqrt(target_opposite**2   +    target_adjescent**2)                                # pouzij udelanou funkco pythagoras_disnace

        if  target_hypotensue > self.radius and target_adjescent != 0 :
            new_angle = degrees (atan ( target_opposite / target_adjescent ))

            if self.rect.center[1] < new_target[1] :
                below = False

            if self.field_site == "left"or self.field_site == "neutral":
                if self.rect.center[0] >= new_target[0] :
                    left = False

                # uhel se meri od vodorovne x osy
                # dopocet dle kvadranntu
                if  below == False and left == False :
                    new_angle = 360 - new_angle
                elif  below == True and left == True :
                    new_angle = 90 + ( 90 - new_angle)
                elif  below == False and left == True :
                    new_angle = 180 + new_angle

            # orava pro oponenta
            if self.field_site == "right":

                new_angle = degrees (atan ( target_opposite / target_adjescent ))

                if self.rect.center[0] >= new_target[0]:
                    left = False

                # uhel se meri od vodorovne x osy
                # dopocet dle kvadranntu
                if  below == True and left == False :
                    new_angle = 180 - new_angle
                elif  below == True and left == True :
                    new_angle =  new_angle
                elif  below == False and left == True :
                    new_angle = 360 - new_angle
                elif  below == False and left == False :
                    new_angle =  180 + new_angle

            # prepocet pro mezni hodnotu ,kdy je uhel 90 stupnu => osa Y , vypocet atran vyse
            if self.rect.center[0] == new_target[0]:
                if self.rect.center[1] > new_target[1]:
                    new_angle = 90
                else:
                    new_angle = 270

        # vraci vypocitany uhel k objektu nebo novy 'cil' pohybu
        return new_angle


    # dle uhlu se nastavi vektor pohybu tj. zmena na ose x a y pro pohyb objektu ve hre
    def set_path_target(self,new_angle):
        # qvadrant
        below = -1
        left = -1

        # krok je 2 pixely => mene trhane pohyby , lze nastavit
        step = self.step

        #  cislo kvadrantu se vypocita jinak nezli klasicke oznaceni, zalezi na pootoceni od brany
        qvadrant =  floor (new_angle / 90)  # pro mic je cislo 0,1,2,3

        if self.field_site == "right":
            qvadrant =  floor (new_angle / 90)  # je cislo 0,1,2,3
            qvadrants_list = [[1 ,-1 ],[1 ,-1 ],[1 ,-1 ],[1 , -1]]

        if self.field_site == "left" or self.field_site == "neutral":
            qvadrant =  floor (new_angle / 90)  # je cislo 0,1,2,3
            qvadrants_list = [[-1 ,-1 ],[-1 ,-1 ],[-1 ,-1 ],[-1 , -1]]

        left =  qvadrants_list [qvadrant] [0]
        below = qvadrants_list [qvadrant] [1]

        shift_hypotensue = step
        shift_adjescent = left * cos(radians(new_angle)) *  shift_hypotensue
        shift_opposite = below * sin(radians(new_angle)) *  shift_hypotensue

        self.velocity[0] =  round (shift_adjescent)
        self.velocity[1] =  round (shift_opposite)
        self.path_target = new_angle

        if self.field_site == "left" or self.field_site == "neutral":
            # hranicni hodnoty
            if new_angle == 0:
                self.velocity[0] = -1 * step
                self.velocity[1] = 0
            if new_angle == 90:
                self.velocity[0] =  0
                self.velocity[1] = -1 * step
            if new_angle == 180:
                self.velocity[0] = step
                self.velocity[1] =  0
            if new_angle == 270:
                self.velocity[0] =  0
                self.velocity[1] =  step

        if self.field_site == "right":
            # hranicni hodnoty
            if new_angle == 0:
                self.velocity[0] =  step
                self.velocity[1] = 0
            if new_angle == 90:
                self.velocity[0] =  0
                self.velocity[1] = -1 * step
            if new_angle == 180:
                self.velocity[0] = -1 * step
                self.velocity[1] =  0
            if new_angle == 270:
                self.velocity[0] =  0
                self.velocity[1] =  step


    # ulozi graphic surface
    def set_graphic(self,graphic_name):
        picture_test = pygame.image.load(graphic_name)
        self.image = pygame.transform.scale(picture_test, (40, 40))

    def reset_graphic(self):
        self.image = "notset"

    # vykresli objekt hry                                                                   # zkontroluj draw ingames and ball ??? zjednodusit
    def draw_ingamer (self,game_window):
        # kresli vision hrace - kam se diva
        # kresleno z velocity jelikoz to je uhel kam hrac smeruje

        view = 12 # zobrazeni pohledu je 10 pixelu , velocity je |2| * 5 = 10
        if self.velocity[0] <= 2 or self.velocity[0] <= 2:
            vision_adjescent = view * self.velocity[0]
            vision_opposite = view * self.velocity[1]
        else:
            vision_adjescent = int(view * self.velocity[0] * 0.8)
            vision_opposite = int(view * self.velocity[1]  * 0.8)

        if self.selected_b == True:
            vision_color = RED
        else:
            vision_color = GREEN

        if self.reinforsment == True:
            vision_color = BLUE

        pygame.draw.lines(game_window.surface, vision_color, True, ((self.rect.center[0] ,self.rect.center[1] ), \
                                (self.rect.center[0] + vision_adjescent ,self.rect.center[1] + vision_opposite  )), 1)


        if self.image == "notset":
            if self.selected_b == True:
                color = YELLOW_SELECTED_ITEMS
            else:
                color = self.color
            pygame.draw.circle(game_window.surface, color, ( self.rect.center[0] ,self.rect.center[1]) ,self.radius, 2)

        else:
            game_window.surface.blit(self.image, (int (self.rect.center[0] - 20      ) ,int(self.rect.center[1]   -20        )))


    # nastaveni nove pozice
    def set_position(self,new_x,new_y):
        self.rect.center = [new_x,new_y]

    # nastavi zda je objekt oznacen
    def set_selected (self,new_status):
        #hrac muze byt oznaceny pouze pokud je v teamu uzivatele                                            # zkontrolovat  ,muze se ukazovat data pro AI hrace bez moznosti je ovladat
        if new_status == True :
            if self.team_type != 1: # "AI" :
                self.selected_b = True
        else:
            self.selected_b = False

    # zkontroluje zda bylo kliknuto na objekt
    def is_selected_by_click (self,position_clicked):
        x_limits = [  self.rect.center[0] - self.radius   ,  self.rect.center[0] + self.radius    ]
        y_limits = [  self.rect.center[1] - self.radius   ,  self.rect.center[1] + self.radius    ]

        if is_clikced_on_circle(x_limits,y_limits,position_clicked) == True:
            return True
        else:
            return False

    # vrati hodnotu z slotu
    def read_selected (self):
        return self.selected_b
