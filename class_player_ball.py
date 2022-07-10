
# moje knihovny
import f_menu
from f_menu import *
import f_clases
from f_clases import *
import class_ingamer
from class_ingamer import *
import class_player_ball
from class_player_ball import *
import support_functions
from support_functions import *
import screens
from screens import *

#-ppppppppppak smazat
import neural_network
from neural_network import *
import reinforsment_learning
from reinforsment_learning import *
#-pppppppppppppp

from random import randint
import tensorflow as tf
from tensorflow import keras
import numpy as np
#import matplotlib.pyplot as plt


#-------------------------------------------------------------------------------class player
class player (ingamer):
    game_status = "notSpecified"             # hra, pausa, ....
    angle = "notSpecified"                   #???ZKONTROLUJ UZ JE V INGAMER TRIDE                                                                                           #neni potreba je uzito path target
    user_driven = "notSpecified"             # kdyz je team_type human , je hrac ovladany uzivatelem Y/N
    team = "notSpecified"                    # jmeno teamu
    speed  = 0                               # osobnost hrace, urcuje rychlost kroku           -----ZATIM nepouzito-------
    balance  = 0                             # osobnost hrace, urcuje zda hrac muze spadnouot  -----ZATIM nepouzito-------
    acuracy = 0                              # osobnost hrace, urcuje presnost kopu            -----ZATIM nepouzito-------
    skills_level = 0                         # osobnost hrace, urcuje kolik vstupu hrac rozpozna pri treningu
    skills_set = []                           #skill set hrace pri vytoreni
    player_type = "99999"                    # utocnik, obrance, brankar, midfielder
    position_by_strategy = "notSpecified"    # -----ZATIM nepouzito-------
    strategy = 1                             # -----ZATIM nepouzito-------
    tactic= 1                                # -----ZATIM nepouzito-------
    dsetination_kick = "notSpecified"        # -----ZATIM nepouzito-------  asi nebude treba
    vision = 5                            # zatim vyuzitojen pro vykresleni hrace
    ball_owner_b = False                     # pokud je hrac ball owner muze provect kop
    team_coach = "notSpecified"              # trener teamu
    AI_metrix =0                                                                                                           # -----ZATIM nepouzito------- asi neni treba bo je pouzit skills_level
    model = "empty"                                                                                                        # -----zkontrolovat je treba kdyz je znam ID ??
    ID = "empty"                             # DATE TIME STAMP bude stejne jako nazev .h5 souboru
    name ="empty"
    message = 1                              # -----ZATIM nepouzito-------
    trening_time = 0


    # ulozi jmeno trenera pro team
    def save_trening_time (self,time):
        self.trening_time = int(self.trening_time) + time


    # ulozi jmeno trenera pro team
    def set_coach (self,new_coach):
        self.team_coach = new_coach

    # pri pohybu(i jine akci) hrace trener zaznamena data,vyuzito pro trenovani
    def send_data_to_coach(self,action,list_of_ingamers,The_field):
        self.team_coach.process_data(self,action, self.get_NN_data(The_field,list_of_ingamers) )

    def get_NN_data(self,The_field,list_of_ingamers):
        The_ball = list_of_ingamers[0]


                            ##                                                                    ##
                                ##                                                            ##
                # # # # # #         ##      potreba elegantnejsi a rychlejsi reseni       ##          # # # # # # # #
                                ##                                                            ##
                            ##                                                                    ##


        '''                                                                         #!!!! 2x v player +1 v kodu opravit!!!!   classes 165 radky
        Inputs:
              Hrac
            [0] - angle to own goal   /kam se diva/
            [1] - angle to ball
            [2] - distance to ball
            [3] - player type (GK,striker,defender,etc)
            [4] - qvadrant (zatim zakladni 3 & 3) 9 moznosti 12.12 prvni v prostred v nem prvni v prostred
            [4] - MISTOKVADRANTU ROVNOU SOURADNICE x - y  napr 5   x=20 - y =15    deleno1000 aby byly menci cisla
             Team
            [5] - je z teamu nejblize mici   1 je 0 neni
            [6] - tactic
            [7] - strategy
            [8] - message
            [9] - team je u balonu ball
            [10] - je v view nejaky hrac ?nastav vzdalenost?
             Hra
            [11] - game status
            [12] - game type
        Outputs:
             - otoc +22 stupnu  (kod 0)
             - otoc -22 stupnu  (kod 1)
             - krok             (kod 2)
             - kop do mice      (kod 3)
             - bez akce         (kod 4)
        '''
        #musi byt nulty index list v liste podminka pro keras vstup!
        inputs = [round(self.path_target/100), \
                   round(self.calculate_angle_to_other_object(The_ball.rect.center)/100), \
                   # oprava pro rozdil od hrany hrace ne od stredu kruznic (umozni vypocet nezavisle na velikosti hracu a mice)
                   (round(pythagoras_distance (self.rect.center, The_ball.rect.center) - self.radius - The_ball.radius))/The_field.longest_distance,
                   # delime 1100 ,to je nejdelsi mozna vzdalenost
                   int(self.player_type), \
                   # testy pak vypocitat polohu
                   # float(calculate_sector(1,self.field_site,self.rect.center,[The_field.field_width,The_field.field_height],The_field.field_bl_corner)), \
                   (self.rect.center[0] - self.rect.center[1]) / 1000  , \
                   1, \
                   int(self.tactic), \
                   int(self.strategy), \
                   int(self.message), \
                   # team u balonu -1 oponent, 0 nikdo neni u balonu, 1 vlastni team je u balonu
                   0 , \
                   # hrac v view -1 oponent, 0 nikdo neni v wiev, 1 vlastni team je
                   0 , \
                   0 , \
                   0  ]

        return inputs

    # pro hrace ovladaneho PC team ma jedno vlakno
    def move_round_once(self,The_field,list_of_ingamers):
        action = 1000 #neutralni hodnota
        model = self.model
        no_of_inputs = int(self.skills_level)
        turn_angle = 22 # hrac se muze pootocin jen o 22 stupnu (zaokrouhlovani pro cele pixely)
        inputs = [0,0,0,0]                                                                                        #------- treba zmenit pro jine vstupy nez 3!!!
        list_of_selected_inputs =[]
        list_of_selected_inputs2 =[]
        selection_coding = self.skills_set

        inputs = self.get_NN_data(The_field,list_of_ingamers)

        for inputs_loop in range (0,len(inputs)):
            if selection_coding[inputs_loop] == True:
                list_of_selected_inputs.append(inputs[inputs_loop])
            else:
                list_of_selected_inputs.append(0)

        if self.reinforsment == False:

            model = create_model_tf2(13)

            prediction =  model.predict([[[list_of_selected_inputs]]])     # ok s 3[]
            action = np.argmax(prediction[0])


            '''
            list_of_selected_inputs2.append( list_of_selected_inputs)
            print (list_of_selected_inputs2)
            prediction =  self.model.predict( np.array(list_of_selected_inputs2) ,batch_size= None )
            action = np.argmax(prediction[0])
            '''

        #action = 1000 #TESTTTTTSTSTSTSTSTSTYYY
        #clock.tick(120)                                       # 5 pro testovani zmen na 60

        if self.selected_b == False:
            # oprava pro uhly kdyz presahnou 360   /    0                                            KOD 3 x !!!!!!!!!!  opakuje se
            if action == 0:
                if (self.path_target + turn_angle) >= 360:
                    uhel = (self.path_target + turn_angle) - 360
                else:
                     uhel =   (self.path_target + turn_angle)
                self.set_path_target(uhel)
            elif action == 1:
                if (self.path_target - turn_angle) <= 0:
                    uhel = (self.path_target - turn_angle) + 359
                else:
                    uhel = (self.path_target - turn_angle)
                self.set_path_target(uhel)
            elif action == 2:
                self.move(The_field,list_of_ingamers)
            elif action == 3 and list_of_ingamers[0].owner == self:
                list_of_ingamers[0].speed = 200   #testovaci kop                                                >>>>>index 0 ?  <<<<<<<<<

    # pro hrace ovladaneho PC kazdy hrac sve vlakkno
    def move_round(self,The_field,list_of_ingamers):

        while self.game_status ==  "game" :
            self.move_round_once(The_field,list_of_ingamers)



    # prdelana metoda pomoci sprites
    def move(self,The_field,list_of_ingamers):                                                          # FUNKCE move POTREBUJE ZPREHLEDNIT
        ball_index = 0

        # hranice hriste
        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        test_target_on_field = 0
        test_player_free_path = 1
        test_ball_free_path = 1
        ball_is_frozen = False

        # kontrola zda mic neni v radius hrace
        if pythagoras_distance (list_of_ingamers[ball_index].rect.center,  self.rect.center) < list_of_ingamers[ball_index].radius + self.radius:
            ball_is_frozen = True

        #  detekce pohybu na hristi, cast hrace muze prejit pres linii hriste , pro pripad ze se balon zastavil prave na teto linii
        if self.rect.center[0] + self.velocity[0] > left - self.radius/2  and self.rect.center[0] + self.velocity[0] < right + self.radius/2  and \
            self.rect.center[1] + self.velocity[1] < bottom + self.radius/2  and self.rect.center[1] + self.velocity[1] > top - self.radius/2  :

            test_target_on_field = 1

        # kontrola kolize s micem
        if ball_is_frozen == False :

            # pohyb posune mic, hrac udelal pohyb na lokaci mice => mic se posune                           # chyba nekdy mic zamrzne u hrace mozna zaokrouhlovani pri vypoctu souradnic
            if pythagoras_distance (list_of_ingamers[ball_index].rect.center,  self.rect.center) <= (list_of_ingamers[ball_index].radius + self.radius) + 3:
            # if  pygame.sprite.collide_circle(self, list_of_ingamers[ball_index]) :

                list_of_ingamers[0].set_owner(self)

                # novy uhel(posun mice)  je stred hrace a souradnice kontaktu s micem
                ball_new_target = self.calculate_angle_to_other_object(list_of_ingamers[ball_index].rect.center)
                list_of_ingamers[ball_index].set_path_target (ball_new_target)

                test_ball_free_path  = list_of_ingamers[ball_index].is_ball_path_clear(The_field,list_of_ingamers)  #2711

                if test_ball_free_path == 1 :
                    list_of_ingamers[ball_index].speed = 2
                else:
                    list_of_ingamers[ball_index].speed = 0

            # hrac odejde od mice => jiz neni jeho vlastnik
            if pythagoras_distance (list_of_ingamers[ball_index].rect.center,  self.rect.center) > (list_of_ingamers[ball_index].radius + self.radius) + 5:
            #if pygame.sprite.collide_circle(self, list_of_ingamers[ball_index]) == False:
                  list_of_ingamers[ball_index].reset_owner(self)

        # detekce ostatnich hracu # vynecha 'sebe' v kontrolre kolize , vynecha mic index '0' v list_of_ingamers
        for no_of_ingamers in range (1,len(list_of_ingamers)):

            # vynecha 'sebe' v kontrolre kolize , vynecha mic index '0' v list_of_ingamers

            # if pygame.sprite.collide_circle(self, list_of_ingamers[no_of_ingamers]) and \
            #     list_of_ingamers[no_of_ingamers].rect.center != self.rect.center :
            distance = pythagoras_distance (list_of_ingamers[no_of_ingamers].rect.center,  self.rect.center)
            #print ("dstn a no_of_ingamers" , dstnc , no_of_ingamers)
            #if distance <= 2*self.radius:
            #    test_player_free_path = 0


        # pokud jsou  podminky splneny hrac se muze pohnout
        if test_target_on_field == 1 and test_ball_free_path == 1 and test_player_free_path == 1:

            self.rect.center =  [self.rect.center[0] + self.velocity[0], self.rect.center[1] + self.velocity[1]]

    def draw_data_lower_menu (self,The_game_window,The_field,list_of_ingamers):                                            # opravit nema byt metoda ale funkce v screens, vykreslovani
        f_print_player_details(The_game_window,The_field,self,list_of_ingamers)

        # zobrazeni hodnot jen pro tesy mozna LAB_mode
        if self.team_type == "AI" and self.selected_b == False:
            live_data = [round(self.path_target), \
                        round(self.calculate_angle_to_other_object(list_of_ingamers[1].rect.center)), \
                        # oprava pro rozdil od hrany hrace ne od stredu kruznic (umozni vypocet nezavisle na velikosti hracu a mice)
                        round(pythagoras_distance (self.rect.center,list_of_ingamers[1].rect.center) - self.radius - list_of_ingamers[1].radius  )]


            #f_print_model_live (The_game_window,The_field,self,list_of_ingamers,live_data,read_model_values ("model.h5"))

    '''

    PRIDEJ metodu 'no action' pro automatizovaneho hrace

    '''

#-------------------------------------------------------------------------------class ball
class ball (ingamer):
    radius = 7
    team_type = "AI" #  mic je neklikatelny
    resistance = 1          # udava jak mic zpomaluje  ---zatim nevyuzito---
    color = WHITE
    owner = 'nooneyet'
    speed = 0

    def draw_data_lower_menu (self,The_game_window,The_field,list_of_ingamers):                                         # opravit nema byt metoda ale funkce v screens, vykreslovani
        f_print_ball_details(The_game_window,The_field,self,list_of_ingamers)

    # kontrola pro hrace kdyz nemuze udelat krok, protoze mic nema misto kam se posunout
    # path v instanci je uz novy od metody move od hrace
    #def is_ball_path_clear(self,The_game_window,The_field,list_of_ingamers):                                            #opakujicis se kod pro preponu kolize
    def is_ball_path_clear(self,The_field,list_of_ingamers):
        decision = 1

        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        #  detekce pohybu na hristi, odraz od sten
        if self.rect.center[0] - self.radius + self.velocity[0]  < left :
            decision =0
        if self.rect.center[0] + self.radius + self.velocity[0]  > right :
            decision =0
        if self.rect.center[1] + self.radius + self.velocity[1]  > bottom :
            decision =0
        if self.rect.center[1]  - self.radius + self.velocity[1]  < top :
            decision =0

        # detekce hracu,mic ma v draze dalsiho hrace
        for no_of_ingamers in range (2,len(list_of_ingamers)):
            other_ingamer_position = list_of_ingamers[no_of_ingamers].rect.center
            ingamer_adjescent =  abs (self.rect.center[0] + self.velocity[0] -  other_ingamer_position[0])
            ingamer_opposite =  abs ( self.rect.center[1]  + self.velocity[1]-  other_ingamer_position[1])
            ingamer_hypotensue = sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

            if ingamer_hypotensue <= self.radius + list_of_ingamers[no_of_ingamers].radius  :                          # zkontrolovat porovnani

                decision =0

        return decision

    def reset_owner(self,player):
        if self.owner == player:
            self.owner = 0
            self.color = WHITE
            player.ball_owner_b = False

    def set_owner(self,new_owner):
        new_owner.ball_owner_b = True
        self.owner = new_owner
        self.color = GREEN
        self.field_site = new_owner.field_site

    # pohyb mice,podobny pohybu hrace, ale mic se muze odrazet od prekazek
    def move(self,The_field,list_of_ingamers):                                                #zkontroluj jaka cast move lze udelat pro ingamer a pak jen zdedit

        if debug_mode == 1:
            print('metodaball')

        # 2 je rychlost pri 'driblingu'
        if self.speed > 2 :
            # kdyz krac mic odkopne ,mic ztraci vlatnika
            self.owner = 0
            self.color = WHITE

        step = self.step
        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        #-------------DODELAT bounderies / colisions ----------------------

        # detekce hracu
        for no_of_ingamers in range (1,len(list_of_ingamers)):
            other_ingamer_position = list_of_ingamers[no_of_ingamers].rect.center
            ingamer_adjescent =  abs (self.rect.center[0] + self.velocity[0] -  other_ingamer_position[0])
            ingamer_opposite =  abs ( self.rect.center[1]  + self.velocity[1]-  other_ingamer_position[1])
            ingamer_hypotensue = sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

            if ingamer_hypotensue <= self.radius + list_of_ingamers[no_of_ingamers].radius  :
                                                                                                                    # JEN PRO TESTY ,JINAK POTREBA DODELAT VYPOCET UHLU ODRAZu
                self.velocity[0] = self.velocity[0] * -1
                self.velocity[1] = self.velocity[1] * -1

                # snizeni energie(speed)
                # hodnoty treba otestovat pri hre, zpomaleni obdobne jako pri skutecne hre
                # zpomaleni s projevi jen pri kontaktu mice a hrace, pri kontaktu mice konce pole se energie nemeni
                if self.speed > 100 :
                    self.speed = int( self.speed * 0.8  )
                elif self.speed > 5 and self.speed <= 100  :
                    self.speed = int( self.speed * 0.5  )
                elif self.speed < 5:
                    self.speed = 0

        #  detekce pohybu na hristi, odraz od sten
        if self.rect.center[0] - self.radius + self.velocity[0]  < left :
            self.velocity[0] = self.velocity[0] * -1
        if self.rect.center[0] + self.radius + self.velocity[0]  > right :
            self.velocity[0] = self.velocity[0] * -1
        if self.rect.center[1] + self.radius + self.velocity[1]  > bottom :
            self.velocity[1] = self.velocity[1] * -1
        if self.rect.center[1]  - self.radius + self.velocity[1]  < top :
            self.velocity[1] = self.velocity[1] * -1

        # potvrzeni nove pozice
        self.rect.center =  [self.rect.center[0] + self.velocity[0]  ,self.rect.center[1]  + self.velocity[1]  ]

    # pokud ma mic energii(speed) tak vola metodu move
    def moving(self,The_field,The_reff):
        The_ball = The_reff.list_of_ingamers[0]

        for no_of_ingamers in range (1, len(The_reff.list_of_ingamers)):
            The_reff.list_of_ingamers[no_of_ingamers].ball_owner_b = False

        if self.speed != 0:
            self.speed = self.speed -1
            self.move(The_field,The_reff.list_of_ingamers)
            The_reff.goal_check(The_field,The_ball)
