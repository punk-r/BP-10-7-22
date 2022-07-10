from random import randint
import pygame
from pygame.locals import *
from threading import  Thread
import time
import copy

import xml_f
from xml_f import *
import f_menu                                                                          # ne vsechny metody potrebujou okno jako parametr zkontroluj
from f_menu import *
import neural_network
from neural_network import *
import class_ingamer
from class_ingamer import *
import class_player_ball
from class_player_ball import *
import support_functions
from support_functions import *
import screens
from screens import *



clock = pygame.time.Clock()

'''
Tridy :

        game_window - okno hry , surafec pro kresleni grafiky
        game_field  - hodnoty pro vykreslenu hraciho hriste
        class_coach - trener, vyhodnocuje trening, urcuje strategii hry
        reff        - rozhotci, potvrzuje hrace do hry ,kterou pote kontroluje

'''

#--------------------------------------------------------------------------------------------class game_window
# trida pro okno aplikace
class game_window():
    window_width = 1280
    window_height = 720
    surface = pygame.display.set_mode((window_width,window_height), pygame.RESIZABLE)
    screen_size_type = "none"                                                                            # uzite?
    items_on_surface = 0                                                                                 #   MOZNA NEBUDE POUZITE???
    game_menu_x_start = 5                       # hranice pro hlavni menu
    game_menu_x_end = int (window_width / 6)
    game_menu_y_end = int (window_height * 4/ 5 )
    menu_line_spacing = int( window_height / 34.2 )   # nastaveni pro hlavni menu
    heading_shift = 2 * menu_line_spacing
    menu_on_screen = True
    language = "CZ"
    lab_mode_b = 0
    # nastavni okna, tabulky, team manegmentu, vyberu hracudo hry
    team_detail_lines = 6                       # 1 x nazev + 5 hracu teamu
    mngmt_column_width = int(0.48 *  game_menu_x_end  )                                                           #udelat pomerem z ruznych velikosti okna
    mngmt_teams_on_page = 10
    mngmt_text_ratio = 3                        # zvetseni pisma ku menu fontu
    selection_game_text_ratio = 2               # zvetseni pisma ku menu fontu
    mngmt_shift_from_menu = int( 1.1 *  menu_line_spacing)
    buttons = []

    def resize_values(self):                                                                                 # je metoda treba????????????????????
        self.game_menu_x_end = int (self.window_width / 6)
        self.game_menu_y_end = int (self.window_height * 4/ 5)
        self.menu_line_spacing = int(self.window_height / 34.2)
        self.heading_shift = 2 *self.menu_line_spacing
        self.mngmt_column_width = int(0.48 *  self.game_menu_x_end  )
        self.mngmt_shift_from_menu = int( 1.1 * self.menu_line_spacing)

    def swap_language(self):
        if self.language == "CZ" :
            self.language = "NOTCZ"
        else:
            self.language = "CZ"

    def set_window_size(self,new_size,The_field):

        self.window_width = new_size[0]
        self.window_height = new_size[1]
        self.surface = pygame.display.set_mode((self.window_width,self.window_height),pygame.RESIZABLE)
        The_field.set_field(self)

#--------------------------------------------------------------------------------------------class game_field
# trida pro hraci pole
class game_field():
    type ="notSpecified"       # pro ruzna vykreslovani hriste,zatim NEVYUZITO
    goals_height = 100         # velikosti branek
    goals_width = 10            # velikosti branek
    #field_bl_window = [0,0]    # ram pro hraci hriste,hotnoty sou nastaveny pri set field
    #lab_mode_b = 1             # zobrazeni pomocnych vypoctu
    field_width = 0            # hotnoty sou nastaveny pri set field
    field_height = 0           # hotnoty sou nastaveny pri set field
    field_bl_corner = [0,0]    # hranice hracih o hriste,hotnoty sou nastaveny pri set field
    gap = 15
    longest_distance = 0

    # nastaveni dle hodnot aplikace
    def set_field (self,game_window):
        field_gap_to_window = 20
        #self.field_bl_window[0] = int ( 1/6 * game_window.window_width  )
        #self.field_bl_window[1] = int ( 4/5 * game_window.window_height  )

        #self.field_bl_corner[0] = int ( 1/6 * game_window.window_width + self.gap )
        self.field_bl_corner[0] = int (field_gap_to_window)
        self.field_bl_corner[1] = int ( 4/5 * game_window.window_height - self.gap/2 )

        self.field_width = int ( 0.95 * game_window.window_width )
        self.field_height = int ( 0.7 * game_window.window_height )
        self.goals_height = 0.2 * self.field_height
        self.longest_distance = int( pythagoras_distance (self.field_bl_corner,  \
                                                      (self.field_bl_corner[0]+ self.field_width, self.field_bl_corner[1] - self.field_height  )))

'''
# nacte teamy z xml
The_reff.load_data_from_xml()

'''

#--------------------------------------------------------------------------------------------class coach
# trida trenera
class class_coach ():
    def __init__(self,team):
        self.team_play_at = team              # urcuje zda je tym domaci nebo ne ,pro nedomaci team se nezobrazuji detaily
        self.loaded_teams_xml = []
        for loop in range (0,10):
            self.loaded_teams_xml.append(SavingType.empty_team_slot.value)
        self.load_data_from_xml()

    # buffers pro vyber teamu v 'team management'
    selected_slot_team_management = [-1,-1]
    selected_slot_team_management_buffer = [-1,-1]
    data_trening = []                   # hrac zasle svoje data, ktere trener vyhodnocuje. vse se uklada do data trening a data labels
    data_labels = []
    active_trening = False              # ukazatel treningu nebo zapasu
    trening_sesion_total_runs = 5000    # 5000  celkovy pocet uceni pro spusteny trening
    RE_trening_sesion_runs = 10000
    trening_repetition_sequence = 1
    trening_repetition_total = 1
    automated_trening_type = False      # true jestli je spusten zautomatizovy trening
    training_areas_ball = [[False,True,False],[False,True,False]]     # hriste rozdeleno na 9 sektoru
    training_areas_player = [[False,True,False],[False,True,False]]
    trainig_code = [True,True, True, True, True, True, True, True, False, True, True , True , True ]
    team_players = [0,0,0,0,0]
    testdata1 = [0,0,2,2 ]
    testdata2 = [0,0,2,2 ]


    def team_reset_graphic(self):
        for players_loop in range (0,5):
            self.team_players[players_loop].reset_graphic()

    # nacte data pro teamu a hrace z xml
    def load_data_from_xml(self):

        # nacteni teamu do seznamu
        list_of_teams = []

        if self.team_play_at == "Home":
            for filename in os.listdir( get_path_home_folder() ):
                if not filename.endswith('.xml'): continue
                list_of_teams.append(filename)
        else:
            for filename in os.listdir( get_path_away_folder() ):
                if not filename.endswith('.xml'): continue
                list_of_teams.append(filename)

        # !!zatim se ukazuje jen 10teamu
        if len(list_of_teams) > 10:
            show_teams = 10
        else :
            show_teams =  len(list_of_teams)

        if self.team_play_at == "Home":
        # domaci teamy
            for teams_loop in range (0,show_teams):
                team_name = list_of_teams[teams_loop]
                self.loaded_teams_xml[teams_loop] =  f_read_from_xml (get_path_home_folder() + team_name )
        else:
            # hoste
            for teams_loop in range (0,show_teams):
                team_name = list_of_teams[teams_loop]
                self.loaded_teams_xml[teams_loop] =  f_read_from_xml (get_path_away_folder() + team_name )

    def set_game_status_to_all(self,new_status):
        for teams_loop in range (0,5):
            self.team_players[teams_loop].game_status = new_status


    # ulozi data z treningu
    def process_data(self,player,action,run_to_save):
        reset_loop = 0

        # po dosazeni max runs se data vyhodnoti
        if len(self.data_trening) < self.trening_sesion_total_runs:

            self.data_trening.append([run_to_save])
            # labels
            self.data_labels.append(action)

        else:
            # manual training (supervised)
            if self.automated_trening_type != True:
                #print ("The self.data_trening eight",self.data_trening)
                #print ("The self.data_labelsht",self.data_labels)
                train_model([self.data_trening], [self.data_labels], player.ID )

                '''
                player.save_trening_time (self.RE_trening_sesion_runs)
                for save_loop  in range (0,len(self.loaded_teams_xml)):
                    if self.loaded_teams_xml[save_loop][0][1] == "original":
                        create_xml_file ( self.loaded_teams_xml[save_loop] )
                '''

            else:
                self.set_game_status_to_all("pause")
                proces_reinforsment_data(player.ID,self.data_trening,self.data_labels)
                processed_training = self.data_trening
                processed_labels =self.data_labels
                #train_model(processed_training, processed_labels, processed_training, processed_labels, player.ID)

            self.reset_training_arrays()
            self.update_trening_time(player.ID, 1)
            #start trainkeras model
            #print(  "po",player.model  )

    def  update_trening_time(self,player_ID,new_time):
        #print ("player_ID",self.team_play_at)
        #print ("player_ID",player_ID)
        for team_loop in range (0,10):
            for loop_pl in range (1,6):
                if self.loaded_teams_xml[team_loop] != SavingType.empty_team_slot.value and \
                   self.loaded_teams_xml[team_loop][loop_pl] != SavingType.empty_player_slot.value:
                    if self.loaded_teams_xml[team_loop][loop_pl][1] == player_ID:
                        # index 4 = trening_time
                        self.loaded_teams_xml[team_loop][loop_pl][4] = str( int( self.loaded_teams_xml[team_loop][loop_pl][4]) + new_time)
                        create_xml_file(self.loaded_teams_xml[team_loop])

    # zmena souradnic pro hrace v prubehu treningu
    def move_players_for_new_training_run (self,The_field,list_of_ingamers):

        vertical_max    = The_field.field_bl_corner [1]
        vertical_min    = The_field.field_bl_corner [1] - The_field.field_height
        horizontal_min  = The_field.field_bl_corner [0]
        horizontal_max  = The_field.field_bl_corner [0] + The_field.field_width
        The_field_rect_format = [horizontal_min, vertical_min, \
                                 The_field.field_width, \
                                 The_field.field_height]

        ball_index = 0

        ball_field_ratio = calculate_trening_area_ratio (self.training_areas_ball)
        ball_field_area = calculate_trening_area_coordinates (ball_field_ratio,The_field_rect_format,"horisontal")

        player_field_ratio = calculate_trening_area_ratio ( self.training_areas_player)
        player_field_area = calculate_trening_area_coordinates (player_field_ratio,The_field_rect_format,"horisontal")
        # testy
        self.testdata1 = player_field_area
        self.testdata2 = ball_field_area

        list_of_ingamers[ball_index].set_position (randint( ball_field_area[0], ball_field_area[0] + ball_field_area[2]), \
                                                   randint( ball_field_area[1], ball_field_area[1] + ball_field_area[3]))

        for no_of_ingamers in range (1,len(list_of_ingamers)): #mic a hraci jsou posunuti na novou pozici
            if list_of_ingamers[no_of_ingamers].selected_b == False and  \
                list_of_ingamers[no_of_ingamers].reinforsment == False   :
                pass
                '''
                list_of_ingamers[no_of_ingamers].set_position (randint(horizontal_min, horizontal_max), \
                                                               randint(vertical_min, vertical_max))
                '''
            else:
                list_of_ingamers[no_of_ingamers].set_position (randint( player_field_area[0], player_field_area[0] + player_field_area[2]), \
                                                               randint( player_field_area[1], player_field_area[1] + player_field_area[3]))


    def set_managementcreateNo(self,index):
        if self.trainig_code[index] == True:
            self.trainig_code[index] = False
        else:
            self.trainig_code[index] = True

    def get_selected_createNos(self):
        counter = 0
        for loop in range (0,len(self.trainig_code)):
            if self.trainig_code[loop] == True:
                counter = counter + 1
        return counter

    def reset_training_arrays (self):
        self.data_trening = []
        self.data_labels = []

    def save_training(self):                                                                                        # pro testy, aplikace neuklada data do txt
        #time = datetime.now()
         # dd/mm/YY H:M:S
        #dt_string = time.strftime("%d-%m-%Y_%H-%M-%S")
        #file_name = 'SaveGeme_' + dt_string + '.txt'
        file_name_testing = 'training.txt'
        with open(file_name_testing, 'w') as f:
            for write_loop in range (0,len(self.data_trening)):
                f.write( str(self.data_trening[write_loop]))
                f.write( '\n')

        file_name_testing = 'traininglabels.txt'
        with open(file_name_testing, 'w') as f:
            for write_loop in range (0,len(self.data_labels)):
                f.write( str(self.data_labels[write_loop]))
                f.write( '\n')



    def move_around_team (self,The_field,list_of_ingamers):
        while list_of_ingamers[1].game_status ==  "game" and list_of_ingamers[6].game_status == "game" :
            for move_around_loop in range (1,len(list_of_ingamers)):
                if list_of_ingamers[move_around_loop].team_coach == self and list_of_ingamers[move_around_loop].reinforsment == False:
                    list_of_ingamers[move_around_loop].move_round_once(The_field,list_of_ingamers)
    '''
     >>>>>>>>>>>> RE TESTING    vypnute move around   <<<<<<<<<<<<<

    def move_around_team (self,The_field,list_of_ingamers):
        pass


    '''

    '''

    PRIDAT METODY PRO KONTROLU TEAMU ,na misto po jednom hraci
        - zmena   strategy ....

    '''


    def create_new_player(self):
        # slot jsou souradnice
        # 0 index je cislo teamu z seznamu celkem misto 10 teamu
        # 1 index je poradi hrace v teamu                                                                                         #pridej kontrolu pro zakaz kopirovani prazdneho slotu
        to_slot   = self.selected_slot_team_management

        # slot hracu, zaporne hodnoty error stavy
        if  to_slot[1] >0 :

            if self.loaded_teams_xml [to_slot[0]] == SavingType.empty_team_slot.value:
                # pro prazny slot teamu se vytvori sablona , A = asci 65
                self.loaded_teams_xml [to_slot[0]] = [[chr(65 + to_slot[0] ),"updated","notselected"]]                    #dodelat random nazev  teamu

                for loop_pl in range (1,6):
                    self.loaded_teams_xml[to_slot[0]].append(SavingType.empty_player_slot.value)

            # nastavi team na status updated => hrac neni ulozeny do xml file
            self.loaded_teams_xml [to_slot[0]][0][1] = "updated"

            # [pl_name, pl_ID,pl_position,skills_level,trening_time]   ,player id dle datetime stamp
            new_player = [players_names (randint( 0,96 )), \
                            time.strftime("%d%m%H%M%S"), \
                            "1", \
                            str(self.get_selected_createNos()), \
                            "0", \
                            copy.deepcopy(self.trainig_code)]

            self.loaded_teams_xml [to_slot[0]] [to_slot[1]] = new_player
            #print (   self.loaded_teams_xml [to_slot[0]]     )
            #print (new_player)
            # vytvoreni modelu dle 'skills' hrace, pocet vstupu neural network
            # model = create_model( self.get_selected_createNos()  )
            model = create_model_tf2( self.get_selected_createNos()  )
            # ulozeni dle hracova ID, date stampt ktery zaruci ze model se neulozi duplikovany                                                                    # nebude konstanta
            model.save( get_path_home_folder() + self.loaded_teams_xml [to_slot[0]] [to_slot[1]] [1]  + ".h5")

        self.selected_slot_team_management = [-1,-1] # reset bufferu


    ## 3 metody pro team managemet hraci jdou mazat a kopirovat
    # smazat hrace v team management
    def delete_player_from_slot(self):
        team_index = self.selected_slot_team_management[0]
        player_index = self.selected_slot_team_management[1]
        # kontrola  slot neni prazdny a je pro hrace
        if player_index > 0:
            # team slot neni prazdny len("none") = 4
            if self.loaded_teams_xml[team_index] != SavingType.empty_team_slot.value : # slot ma ulozeny team
                self.loaded_teams_xml [team_index][player_index] = SavingType.empty_player_slot.value                                                           #pridej team neni original
                # nastavi team na status updated => hodnoty nactene ve hre se lisi od hodnot ulozenych v xml souboru
                self.loaded_teams_xml [team_index][0][1] = "updated"
                self.loaded_teams_xml [team_index][0][2] = "unselected"


    def copy_player_from_slot(self):
        position_copy = copy.deepcopy(self.selected_slot_team_management)
        self.selected_slot_team_management_buffer =  copy.deepcopy(position_copy)

    def paste_player_from_other_slot(self):
        # slot jsou souradnice
        # 0 index je cislo teamu z seznamu celkem misto 10 teamu
        # 1 index je poradi hrace v teamu                                                                                         #pridej kontrolu pro zakaz kopirovani prazdneho slotu
        from_slot = self.selected_slot_team_management_buffer
        to_slot   = self.selected_slot_team_management

        # slot hracu, zaporne hodnoty error stavy  , nelze kopirovat prazdny slot
        if to_slot[1] >0 and from_slot[1] >0 and \
            self.loaded_teams_xml [from_slot[0]] != SavingType.empty_team_slot.value and \
            self.loaded_teams_xml [from_slot[0]][from_slot[1]] != SavingType.empty_player_slot.value :

            if self.loaded_teams_xml [to_slot[0]] == SavingType.empty_team_slot.value:  # 4 = len(none)
                # pro prazny slot teamu se vytvori sablona
                # A = asci 65
                self.loaded_teams_xml [to_slot[0]] = [[chr(65 + to_slot[0] ),"updated","notselected"]]                    #dodelat random nazev  teamu

                for loop_pl in range (1,6):
                    self.loaded_teams_xml[to_slot[0]].append(SavingType.empty_player_slot.value)


            # nastavi team na status updated => hodnoty nactene ve hre se lisi od hodnot ulozenych v xml souboru
            self.loaded_teams_xml [to_slot[0]][0][1] = "updated"

            self.loaded_teams_xml [to_slot[0]] [to_slot[1]] = copy.deepcopy(self.loaded_teams_xml [from_slot[0]] [from_slot[1]])

            # player id dle datetime stamp
            self.loaded_teams_xml [to_slot[0]] [to_slot[1]] [1] = time.strftime("%d%m%H%M%S")


            # vytvoreni modelu dle 'skills' hrace, pocet vstupu neural network
            # model = create_model(   self.loaded_teams_xml [to_slot[0]] [to_slot[1]][3]   )
            model = create_model_tf2(   self.loaded_teams_xml [to_slot[0]] [to_slot[1]][3]   )
            # ulozeni dle hracova ID, date stampt ktery zaruci ze model se neulozi duplikovany                                                                    # nebude konstanta
            model.save( get_path_home_folder() + self.loaded_teams_xml [to_slot[0]] [to_slot[1]] [1]  + ".h5")

        self.selected_slot_team_management_buffer = [-1,-1] # reset bufferu

    def can_edit_player(self):
        player_selected = False
        team_index = self.selected_slot_team_management[0]
        player_index = self.selected_slot_team_management[1]
        if  player_index > 0 and self.loaded_teams_xml[team_index] != SavingType.empty_team_slot.value : # slot ma ulozeny team, je vybran hrac
            if self.loaded_teams_xml [team_index][player_index] != SavingType.empty_player_slot.value : # slot hrace neni prazdny
                player_selected = True
        return player_selected                                  # rename player selected no sence

    def edit_player_position(self,new_position):
        team_index = self.selected_slot_team_management[0]
        player_index = self.selected_slot_team_management[1]
        if self.can_edit_player() == True :
            self.loaded_teams_xml [team_index][0][1] = "updated"
            self.loaded_teams_xml [team_index][player_index][2] = new_position


    def reset_selected_slot_team_management(self):
        self.selected_slot_team_management = [-1,-1]
        self.selected_slot_team_management_buffer = [-1,-1]

    # ulozi team do xml
    def save_team_from_teammngmt_table(self):
        all_players_check = 1 # kontrola hrac x5 v teamu jinak se team neulozi
        team_index = self.selected_slot_team_management[0]
        player_index = self.selected_slot_team_management[1]
        checked_team = self.loaded_teams_xml[team_index]

        if checked_team != SavingType.empty_team_slot.value: #pokud prazdny slot metoda nic nevykona
            for check_team_loop in range (1,5):
                if len(checked_team [check_team_loop] ) == SavingType.empty_player_slot.value:                                       # 4 = len(none)   opakovani kodu zlepsit
                    all_players_check = 0

            if all_players_check == 1 and player_index == 0: #oznacen je team ne hrac
                # potvrdi ulozeni teamu
                self.loaded_teams_xml[team_index][0][1] = "original"
                create_xml_file(  checked_team)




    # vypocita slot z team management tabulky z souradnic mysi
    def calculate_slot_index(self,position_clicked,The_game_window):

        # hodnoty musi by ulozeny v 'window' aby slo vypocitat polohu mysi => spustit metodu/funkci
        lines = The_game_window.team_detail_lines
        column_width = The_game_window.mngmt_column_width
        teams_on_page = The_game_window.mngmt_teams_on_page
        text_ratio = The_game_window.mngmt_text_ratio
        shift_from_menu = The_game_window.mngmt_shift_from_menu

        # hranice tabulky teamu
        table_top = The_game_window.heading_shift
        table_left = shift_from_menu + The_game_window.game_menu_x_end
        table_bottom = table_top + text_ratio * lines * The_game_window.menu_line_spacing
        table_right = table_left + teams_on_page * column_width

        if position_clicked[0] > table_left and position_clicked[0] < table_right:
            if position_clicked[1] > table_top and position_clicked[1] < table_bottom:
                self.selected_slot_team_management[0] =  int( (position_clicked[0] - table_left ) // column_width )
                self.selected_slot_team_management[1] =  int ( (position_clicked[1] - table_top ) // (text_ratio * The_game_window.menu_line_spacing ) )
    '''
    # nacte teamy z slozky z predchozich her
    def save_H_team_available_to_list (self,new_teams):
        self.H_teams_available_list = new_teams
                                                                                                #metody smazat nepouzite
    def save_A_team_available_to_list (self,new_teams):
        self.A_teams_available_list = new_teams
    '''

    # zmeni team na selected ,pro vyber teamu pro hru
    def choose_team_from_selection(self):
        team = self.selected_slot_team_management[0]

        # dvakrat vybrany team
        if self.loaded_teams_xml[team] != SavingType.empty_team_slot.value:
            #team neni vybran
            if self.loaded_teams_xml[team][0][2] == "notselected" and self.loaded_teams_xml[team][0][1] == "original":
                self.loaded_teams_xml[team][0][2] = "selected"
            else:
                self.loaded_teams_xml[team][0][2] = "notselected"


    def set_training_areas_player(self,change_input_index):  # change_input_index cislo 0 do 5
        buffer = copy.deepcopy(self.training_areas_player)
        index = int(change_input_index)
        if change_input_index <3:
            self.training_areas_player[0][index] = not self.training_areas_player[0][index]
        else:
            self.training_areas_player[1][index - 3] = not self.training_areas_player[1][index - 3]

        # area je vzdy jeden celek ,nelze oznacit dve oddelene casti
        if  self.training_areas_player[0] == [True,False,True]  or \
              self.training_areas_player[1] == [True,False,True]:
            self.training_areas_player = buffer


    def set_training_areas_ball(self,change_input_index):  # change_input_index cislo 0 do 5
        buffer = copy.deepcopy(self.training_areas_ball)
        index = int(change_input_index)
        if change_input_index <3:
            self.training_areas_ball[0][index] = not self.training_areas_ball[0][index]
        else:
            self.training_areas_ball[1][index - 3] = not self.training_areas_ball[1][index - 3]

        # area je vzdy jeden celek ,nelze oznacit dve oddelene casti
        if  self.training_areas_ball[0] == [True,False,True]  or \
              self.training_areas_ball[1] == [True,False,True]:
            self.training_areas_ball = buffer


#--------------------------------------------------------------------------------------------class reff
# trida rozhodciho
class reff ():
    def __init__(self):
            self.coach_team_A = class_coach("Home")                # rozhodci ma prehled o cele hre i o trenerech
            self.coach_team_B = class_coach("Away")

    position = [0,0]
    teams_for_game  = [" "," ","H","H"]        # oznacene 2 teamy pro hru a jejich nastaveni
    radius = 15                                 # velikost
    #lab_mode_b = 1                              # laboratory mode, odemkne nektera nastaveni
    game_type = "none"                          # typ hry: pause/match/none
    selected_b = False                          # ukazatel zda je ingamer oznaceny                      zkontroluj ,mely by byt uz z ingamer tridy!!
    score  = [0,0]                              # pocitadlo golu
    time  = 0                                   # odpocet casu
    color_check  = 0                            # hodnoty pro nastaveni hry zatim epouzito
    set_color  = 0
    was_clicked  = 0                            # reff byl oznacen pri hre
    #stop_game  = 0                                                                                            # ? uzito ??
    #pause_game   = 0                           # puse pro zapocatou hru
    team_type = "neutral"                       # ???  zkontroluj
    H_teams_available_list = []                 # home teams   ASI NENI treba pouzit list vsech teamu co sou k dispozici (loaded_teams_xml)
    A_teams_available_list = []                 # away teams  ASI NENI TREBA
    list_of_ingamers = [ ball([10,10])         ]    # ball+ players


    def load_teams_for_game_to_slot(self):
        save_index = 0
        all_teams = self.coach_team_A.loaded_teams_xml + self.coach_team_B.loaded_teams_xml
        for team_no in range (0,len(all_teams)):
            if all_teams[team_no] != SavingType.empty_team_slot.value:
                if all_teams[team_no][0][2] == "selected":
                    if save_index == 0:
                        self.teams_for_game[0] = all_teams[team_no]
                        save_index = 1
                    else:
                        self.teams_for_game[1] = all_teams[team_no]
                        break
        '''
        print(self.teams_for_game[0])
        print(self.teams_for_game[1])
        print(self.teams_for_game[2])
        print(self.teams_for_game[3])
        '''

    def set_teams_type_for_game(self,type):
        self.teams_for_game[2] = "AI"
        self.teams_for_game[3] = "AI"

        if type == "H/AI":
            self.teams_for_game[2] ="H"
        elif type == "AI/H":
            self.teams_for_game[3] ="H"
        elif type == "H/H":                    # pouze pro manualni staticky trening
            self.teams_for_game[2] = "H"
            self.teams_for_game[3] = "H"

    def reset_teams_buffer_for_game(self):
        self.teams_for_game  = [" "," ","AI","H"]
        for teams_reset_loop  in range (0,12):
            if len(self.loaded_teams_xml [teams_reset_loop] ) != SavingType.empty_player_slot.value:  # 4 = len(none)
                if self.loaded_teams_xml[teams_reset_loop][0][2] == "selected" :
                    self.loaded_teams_xml[teams_reset_loop][0][2] = "notselected"


    # povrzeni teamu do treningu
    def start_training(self):                                                                                               # POJMENOVANI SPATNE ma byt check trening , start trening mate s start game
        # trening lze zacit pokud jso oznaceny sloty s existujicimi teamy (lze vybrat trening i teamu sama k sobe)
        #    => slot nesmi byt prazdny nebo staus jiny nez original
        # teamy maji status original => nemaji zmenu ktera neni ulozena, maji 5 ulozenych hracu
        # vybran team a hrac (hracuv team je automaticky vybran jako druhy pro trening)

        # prvni index je team , druhy je hrac
        # priklad  index_team_a =[0,0]  je oznacen team 0 ,  [1,2]  znamena team na indexu 1 a jeho hrac na indexu 2
        index_team_b = self.coach_team_A.selected_slot_team_management
        index_team_a = self.coach_team_A.selected_slot_team_management_buffer

        player_selected_ID = "none"
        start_training_check = False
        #print("gfgfgfgfgf",index_team_a,index_team_b )
        # oba teamy existuji
        if self.coach_team_A.loaded_teams_xml [index_team_a[0]] != SavingType.empty_player_slot.value  and  \
            self.coach_team_A.loaded_teams_xml [index_team_b[0]]  != SavingType.empty_player_slot.value:  # 4 = len("none")

            # oznacen hrac a team
            if  (index_team_a[1] == 0 or index_team_b[1] == 0)  and \
                (index_team_a[1] != 0 or index_team_b[1] != 0):
                #print("gfgfgfgfgf     teams_for_game")
                #print(self.teams_for_game )
                # status teamu je original
                #print ("aaa",  self.coach_team_A.loaded_teams_xml    )
                if  self.coach_team_A.loaded_teams_xml[index_team_a[0]][0][1] == "original" and \
                    self.coach_team_A.loaded_teams_xml[index_team_b[0]][0][1] == "original"  :                               #zkontroluj podmnku

                    #player # ID
                    if index_team_a[1] != 0:
                        player_selected_ID = self.coach_team_A.loaded_teams_xml[index_team_a[0]][index_team_a[1]][1]
                    else:
                        player_selected_ID = self.coach_team_A.loaded_teams_xml[index_team_b[0]][index_team_b[1]][1]

                    self.set_game_status_to_self("none")
                    start_training_check = True

                    self.teams_for_game[0] = self.coach_team_A.loaded_teams_xml[index_team_a[0]]
                    self.teams_for_game[1] = self.coach_team_A.loaded_teams_xml[index_team_b[0]]

        #  ??? vyuzit self.teams_for_game[0] = "Ooo,Error :("      pro informaci hraci o spatnem vstupu  , udelat print funkci pro error

        return [start_training_check,player_selected_ID  ]

    # spocte vsechny selected teams
    def count_selected_teams(self):
        master_list = self.coach_team_A.loaded_teams_xml + self.coach_team_B.loaded_teams_xml
        teams_selected = 0
        # kontrola ze 2 teamy jsou oznaceny
        for check_loop in range (0,len(master_list)):
            # team slot neni prazdny len("none") = 4
            if master_list[check_loop] != SavingType.empty_team_slot.value :
                if master_list[check_loop][0][2] == "selected":
                    teams_selected = teams_selected + 1
        return  teams_selected

    # zkontroluje zda jsou oznaceny pouze dva teamy
    def check_selected_teams(self):
        teams_selected = self.count_selected_teams()

        # ulozi 2x jmeno vybranych teamu
        if  teams_selected == 2 or teams_selected == 1:
            self.teams_for_game[0] = " "
            self.teams_for_game[1] = " "
            saving_index = 0
            for save_loop in range (0,len(self.loaded_teams_xml)):
                if self.loaded_teams_xml[save_loop] != SavingType.empty_team_slot.value:
                    if self.loaded_teams_xml[save_loop][0][2] == "selected":
                        self.teams_for_game[saving_index] = self.loaded_teams_xml[save_loop][0][0]
                        saving_index = saving_index + 1

        elif teams_selected > 2:
            self.teams_for_game[0] = "2!"
            self.teams_for_game[1] = "1!"

        elif  teams_selected == 0:
            self.teams_for_game[0] = " "
            self.teams_for_game[1] = " "


    # kontrola pro vstreleny gol
    def goal_check(self,The_field,The_ball):
        decision_goal = 0

        goal_top    = The_field.field_bl_corner[1] - The_field.field_height/2 - The_field.goals_height/2
        goal_bottom = The_field.field_bl_corner[1] - The_field.field_height/2 + The_field.goals_height/2

        field_right  = The_field.field_bl_corner[0] + The_field.field_width
        field_left   = The_field.field_bl_corner[0]

        if False:
            print (' .goal_top',goal_top)
            print ('goal_bottom',goal_bottom)
            print ('field_rightt',field_right)
            print ('field_left',field_left)
            print ('ball',The_ball.rect.center)
            print("game_fieldwth"  ,The_field.field_width )
            print("game_fieldhght"  ,The_field.field_height )

        # kontrola pozice mice ku branam
        if The_ball.rect.center[1] - The_ball.radius < goal_bottom  and The_ball.rect.center[1]  + The_ball.radius > goal_top:

            # rozdil 1 - mic se zastavi pixel pred carou
            if The_ball.rect.center[0] - The_ball.radius - 1  <= field_left  :
                self.score [0] = self.score [0]  + 1
                self.game_reset (The_field,The_ball)

            elif The_ball.rect.center[0] + The_ball.radius + 1  >= field_right :
                self.score [1] = self.score [1]  + 1
                self.game_reset (The_field,The_ball)


    # resetovani mice
    def game_reset (self,game_field,The_ball):
        The_ball.speed = 0
        The_ball.color = WHITE
        The_ball.set_position    (randint( 400,800 ), randint(100 ,500 ) )


    def draw_ingamer (self,game_window):                                                                      #zmen na draw ref??
        if self.selected_b == True:
            color = YELLOW_SELECTED_ITEMS
        else :
            color = WHITE

        # Rozhodci se vykresluje jako bilo-cerny kruh
        # pomocny vypocet
        rectangle_for_drawing = [ self.position[0] - self.radius , self.position[1] - self.radius ,2 * self.radius , 2* self.radius ]
        # arc(surface, color, rect, start_angle, stop_anglenline)
        pygame.draw.arc(game_window.surface, color, rectangle_for_drawing, radians (90) ,  radians (180), self.radius)
        pygame.draw.arc(game_window.surface, color, rectangle_for_drawing, radians (270) ,  radians (360), self.radius)
        pygame.draw.circle(game_window.surface, color, ( self.position[0] ,self.position[1]) ,self.radius, 1)


    def set_selected (self,new_status):                                                                              #reff potomek ingamer??? opakuje se dost metod pri reff jako nezdedena trida
        # hrac muze byt oznaceny pouze pokud je v team_type "human"
        if new_status == True :
            if self.team_type != "AI":
                self.selected_b = True
        else:
            self.selected_b = False

    # jestli je item oznacen mysi nastavi se na selected , dle podminek set_selected
    def is_selected_by_click (self,position_clicked):
        x_limits = [  self.position[0] - self.radius   ,  self.position[0] + self.radius    ]
        y_limits = [  self.position[1] - self.radius   ,  self.position[1] + self.radius    ]

        if is_clikced_on_circle(x_limits,y_limits,position_clicked) == True:
            return True
        else:
            return False


    def read_selected (self):
        return self.selected_b

    # vygenerovani zapasu / treningu
    def start_match (self,The_field,called_at_begining,teams_threds):                           # potreba?called_at_begining ?
        #print ("startmatch",self.game_type )
        thread_team_A = teams_threds[0]
        thread_team_B = teams_threds[1]
        ball_index = 0

        # nelze spustit vice her
        if self.game_type != "none" :
            return

        self.game_type = "game"

        # pro trening
        vertical_max    = The_field.field_bl_corner [1]
        vertical_min    = The_field.field_bl_corner [1] - The_field.field_height
        horizontal_min  = The_field.field_bl_corner [0]
        horizontal_max  = The_field.field_bl_corner [0] + The_field.field_width
        team_A_slot = self.teams_for_game [0] # ulozi jmeno teamu
        team_B_slot = self.teams_for_game [1] # ulozi jmeno teamu

        # set pro hru nastaveni pozice rozhotciho  a mice pro zacatek hry
        self.position = [  int( horizontal_max / 2 + self.radius ) , int(vertical_min  - self.radius )  ]
        self.list_of_ingamers[ball_index].radius = 7
        self.list_of_ingamers[ball_index].rect.center = [int( horizontal_max / 2 + self.radius ), int(vertical_max / 2)   ]
        self.list_of_ingamers[ball_index].set_path_target(180)

        self.load_teams_for_game_to_slot()
        all_teams = [self.teams_for_game[0] , self.teams_for_game[1]]
                                                                                                            # pridat kontrolu teamu,
        # input ma tvar : [team_name,5x [pl_name, pl_ID,pl_position,trening_type,trening_time]]
        shift_x = The_field.field_bl_corner[0] + The_field.field_width*0.2
        team_switch = 0
        ingamer_saving_loop = 1 # 2 protoze index 0 je eff index 1 je ball
        for teams_lops in range (0,2):    # vybere 'selected' teamy z listu vsech teamu

            if True : # puvodni kontrola neni treba , start_match se vola uz s kontrolovanyma hodnotama

                shift_y = The_field.field_bl_corner[1] * 0.3
                for players_loop in range (1,6):   # index 0 je nazev teamu
                    # vypsani teamu a hracu,prvni column je pro popisky
                    #print("team/players_loop" , teams_lops," "    ,players_loop)
                    #print(       "numbr"    , int( all_teams[teams_lops][players_loop][3]) )
                    if teams_lops < 10 :
                        full_path = get_path_home_folder()
                    else:
                        full_path = get_path_away_folder()

                    new_player_ID = all_teams[teams_lops][players_loop][1]
                    new_player = player ([int(shift_x),int(shift_y)])
                    new_player.path_target = 180
                    new_player.game_status = "game"
                    new_player.set_path_target(180)
                    new_player.ID = new_player_ID
                    new_player.name = all_teams[teams_lops][players_loop][0]
                    new_player.player_type =  all_teams[teams_lops][players_loop][2]
                    new_player.skills_level = int(all_teams[teams_lops][players_loop][3])
                    new_player.trening_time = all_teams[teams_lops][players_loop][4]
                    new_player.skills_set =   all_teams[teams_lops][players_loop][5]
                    #print (new_player.skills_set)

                    # nastaveni v zavislosti na teamu
                    if team_switch == 0:
                        new_player.team_type = self.teams_for_game[2]
                        new_player.team = all_teams[teams_lops][0][0]
                        new_player.field_site = "left"
                        new_player.set_coach(self.coach_team_A)
                        new_player.set_graphic("player_a.png")
                        self.coach_team_A.team_players[players_loop -1] = new_player
                    else:
                        new_player.team_type = self.teams_for_game[3]
                        new_player.team = all_teams[teams_lops][0][0]
                        new_player.color = RED
                        new_player.field_site = "right"
                        new_player.set_coach(self.coach_team_B)
                        new_player.set_graphic("player_b.png")
                        self.coach_team_B.team_players[players_loop -1] = new_player

                    new_player.model= load_model( full_path +  new_player_ID + ".h5")   # zmenin na file dle ID hrace
                    if new_player.skills_level == 4:
                        pass
                        #print(new_player.model.summary())
                    '''
                    x = 1 #pro testy
                    if x == 1:
                        thread_new_player =  Thread (target = new_player.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
                        thread_new_player.start()
                    '''
                    shift_y = shift_y + The_field.field_height * 0.1
                    # vytvareni teamu po spusteni hry / vytvareni teamu prepisuje predchozi hru
                    if len(self.list_of_ingamers) == 11:
                        self.list_of_ingamers[ingamer_saving_loop] = new_player
                        ingamer_saving_loop = ingamer_saving_loop + 1
                    else:
                        self.list_of_ingamers.append(new_player)

                team_switch = 1
                shift_x = The_field.field_bl_corner[0] + The_field.field_width*0.8

        if thread_team_A:#testy
            print ("   start treads       ")
            thread_A_team =  Thread (target = self.coach_team_A.move_around_team   ,args =  (The_field,self.list_of_ingamers))
            thread_A_team.start()
        if thread_team_B:
            thread_B_team =  Thread (target = self.coach_team_B.move_around_team   ,args =  (The_field,self.list_of_ingamers))
            thread_B_team.start()
        if False:#a player
            thread_A_team_player =  Thread (target = self.list_of_ingamers[3].move_round   ,args =  (The_field,self.list_of_ingamers))
            thread_A_team_player.start()

    # nastavi novy game_status sobe
    def set_game_status_to_self(self,new_status):
        self.game_type = new_status

    # nastavi  game_status  vsem hracum
    def set_game_status_to_players(self):
        for no_of_ingamers in range (1,len(self.list_of_ingamers)):
            self.list_of_ingamers[no_of_ingamers].game_status = self.game_type

    def pause_game(self):#,The_game_window,The_field):                                                    #   potrebuje vsechny vstupy??
        self.set_game_status_to_self("pause")
        self.set_game_status_to_players()


    def unpause_game(self,The_game_window,The_field):
        self.set_game_status_to_self("game")
        self.set_game_status_to_players()
        thread_A_team =  Thread (target = self.coach_team_A.move_around_team   ,args =  (The_field,self.list_of_ingamers))
        thread_A_team.start()
        thread_B_team =  Thread (target = self.coach_team_B.move_around_team   ,args =  (The_field,self.list_of_ingamers))
        thread_B_team.start()




    '''
    def restart_players(self,The_game_window,The_field,list_of_ingamers):                   #zkontroluj je pouzito
        self.start_match (The_game_window,The_field,list_of_ingamers,False)
    '''

    def draw_data_lower_menu (self,The_game_window,The_field):                           # zkontroluj pro je metoda dyz se muze vykreslovat jak ostatni
        f_print_score(self.score,The_game_window,The_field)
