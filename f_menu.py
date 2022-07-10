import pygame
import os.path
from os import path
from threading import  Thread

import screens
from screens import *

import neural_network
from neural_network import *
import reinforsment_learning
from reinforsment_learning import *
import support_functions
from support_functions import *
import xml_f
from xml_f import *




#pygame modul
pygame.init()
from pygame.locals import *

# fonty
TEST_FONT = pygame.font.SysFont("Arial", 5)
MENU_FONT = pygame.font.SysFont("Arial", 18)
CREATENO_FONT = pygame.font.SysFont("Arial", 15)
MENU_FONT_HEADING = pygame.font.SysFont("Arial", 30)
WELCOME_FONT = pygame.font.SysFont("Arial", 40)


def get_font(font_original, resolution):                                              #neni uplne efektivni lip dat do window primo funkci predelat
    ratio = 1
    if font_original == "TEST_FONT":
        font_scaled = pygame.font.SysFont("Arial", 5 * ratio)
    elif font_original == "MENU_FONT":
        font_scaled = pygame.font.SysFont("Arial", 18 * ratio)
    elif font_original == "MENU_FONT_HEADING":
        font_scaled = pygame.font.SysFont("Arial", 30 * ratio)
    elif font_original == "WELCOME_FONT":
        font_scaled = pygame.font.SysFont("Arial", 40 * ratio)
    return font_scaled

#-------------------------------------------------------------------------------class buttons
# trida pro tlacika
class Button():
    def __init__(self):
        self.number = 0         # id tlacitka
        self.x_corner = 0       # souradnice
        self.y_corner = 0
        self.size = [10, 10]     # velikost tlacitka: lenght, hight
        self.name ='n'          # popisek (text) tlacitka
        self.graphic = "notset" # zatim nepouzito priprava pro pixel art
        self.frame = False      # pravidla zobrazeni ramecku
        self.selected = False

    def set_selected_status(self,new_status):                                                       # mel by se menovat set status => vic univerzalni
        self.selected = new_status

    # nastaveni tlacitka
    def set_button_name_number (self,name,number):
        self.name  = name
        self.number = number

    # kontrola kliku na tlacitko
    def is_mouse_over_button (self,mouse_position,screen_ID_lower_screen,menu_on_screen):                                 # pouzit enums na misto cisel<<<
        decision = "nomatch"  # error hodnota
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        screen_ID = screen_ID_lower_screen[0]
        lower_screen_ID = screen_ID_lower_screen[1]

        if mouse_x > self.x_corner and mouse_x < self.x_corner + self.size[0]:
            if mouse_y > self.y_corner and mouse_y < self.y_corner + self.size[1]:
                decision = self.number

                # kontrola pro 2 tlacitka na stejnem miste v ruznych SCREENS
                # > 1 znamena button neni z hlavniho menu
                if  decision > 1:
                    if trunc(decision) == screen_ID:
                        decision == self.number                                                                           # zKONTROLUUUJJJ !!!!!!!!!!!!!!!!!
                    else:
                        if decision == 15.1:
                            decision = 15.1
                        else:
                            if trunc(decision) == 21 and \
                                    screen_ID == Screens.teammanagement.value and \
                                    lower_screen_ID == Screens.teammanagementedit.value:
                                decision == self.number

                            elif (trunc(decision) == 23 or trunc(decision) == 24) and \
                                    screen_ID == Screens.teammanagement.value and \
                                    lower_screen_ID == Screens.teammanagementcreate.value:
                                decision == self.number                                                                      # zKONTROLUUUJJJ !!!!!!!!!!!!!!!!!

                            elif trunc(decision) == 42 and \
                                    screen_ID == Screens.trening.value:
                                decision == self.number
                                                                                                                           # zKONTROLUUUJJJ !!!!!!!!!!!!!!!!!
                            else:
                                decision = "nomatch"

                # pri hre
                if  screen_ID == Screens.ingame.value and trunc(self.number) == 0 and menu_on_screen == False:
                    decision = "nomatch"

        return decision


# --------------------------MENU-----------------------
# vytvoreni instanci tlacitek
# tlacitka pro ostatni volby
def create_buttons_instances(The_game_window,The_field):
    buttons_names_list = all_buttons_names(The_game_window.language)
    buttons_ids = all_buttons_IDs()
    list_buttons_instances = []     # list vsech instanci tridy button pro hru
    ref_buttons_counter = 0         # pocitadlo tlacitek rozhodtico v prubehu hry
    ref_buttons_counter2 = 0
    mngmnt_buttons_counter = 0      # pocitadlo tlacitek team management stranky
    mngmntedit_buttons_counter = 0
    trening_buttons_counter = 0     # pocitadlo tlacitek trenovani teamu
    treningman_buttons_counter = 0
    choose_teams_counter = 0        # pocitadlo tlacitek vyberu teamu do hry
    mngmntaway_buttons_counter = 8
    mngmntcreate_buttons_counter = 0
    column_ration = 1.052 #treba??
    mngmnt_button_height = 22
    mngmnt_button_width = int (The_game_window.mngmt_column_width)
    mngmntcreateNo_buttons_counter_x = 0
    mngmntcreateNo_buttons_counter_y = 0
    shift_mngmntcreateNo_buttons = int (The_game_window.mngmt_column_width*2)

    # generovani tlacitek
    for generating_buttons_loop in range (0,len(buttons_names_list)):
        new_button = Button()
        # format se upravi pro buttons ktere nejsou v menu  (popisek tlacitka se vycentruje )
        button_name_original = buttons_names_list [generating_buttons_loop]
        button_name_centered = center_button_name( button_name_original, 14) if generating_buttons_loop > 15 else button_name_original
        new_button.set_button_name_number (button_name_centered, buttons_ids[generating_buttons_loop])
        new_button.frame = True
        list_buttons_instances.append(new_button)

        ## nastaveni vygenerovaneho tlacitka
        # menu tlacitka
        if trunc(buttons_ids[generating_buttons_loop]) == 0 :
            new_button.frame = False
            new_button.size = [150,18]
            new_button.x_corner = The_game_window.game_menu_x_start
            new_button.y_corner = The_game_window.heading_shift + generating_buttons_loop  * The_game_window.menu_line_spacing

        #  team management tlacitka
        elif trunc(buttons_ids[generating_buttons_loop]) ==  Screens.teammanagement.value:
            new_button.size = [mngmnt_button_width,mngmnt_button_height]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu +  \
                                     mngmnt_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                                    The_game_window.mngmt_text_ratio *  The_game_window.menu_line_spacing
            if new_button.number > 2.40:#players/ teams
                if new_button.number == 2.50:
                    mngmnt_buttons_counter =  mngmnt_buttons_counter + 4
                else:
                    mngmnt_buttons_counter = mngmnt_buttons_counter + 1
            else:
                mngmnt_buttons_counter =  mngmnt_buttons_counter + 1

        #  team managementaway
        elif trunc(buttons_ids[generating_buttons_loop]) ==  Screens.teammanagementaway.value:
            new_button.size = [mngmnt_button_width,mngmnt_button_height]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu +  \
                                     mngmntaway_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                                    The_game_window.mngmt_text_ratio *  The_game_window.menu_line_spacing

            #mngmntaway_buttons_counter = mngmntaway_buttons_counter + 1

        #  team managementedit player tlacitka
        elif trunc(buttons_ids[generating_buttons_loop]) ==  Screens.teammanagementedit.value:
            new_button.size = [mngmnt_button_width,mngmnt_button_height]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu +  \
                                     mngmntedit_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner = 25 *  The_game_window.menu_line_spacing #The_game_window.game_menu_y_end #+ The_game_window.heading_shift *2

            mngmntedit_buttons_counter =  mngmntedit_buttons_counter + 1

        #  team managementcreate player tlacitka
        elif trunc(buttons_ids[generating_buttons_loop]) ==  Screens.teammanagementcreate.value:
            new_button.size = [mngmnt_button_width ,mngmnt_button_height]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu +  \
                                     mngmntcreate_buttons_counter  * new_button.size[0]
            new_button.y_corner = 25 *  The_game_window.menu_line_spacing #The_game_window.game_menu_y_end #+ The_game_window.heading_shift *2

            mngmntcreate_buttons_counter =  mngmntcreate_buttons_counter + 1

        #  team managementcreateNo player tlacitka
        elif trunc(buttons_ids[generating_buttons_loop]) ==  Screens.teammanagementcreateNo.value:
            #mngmntcreateNo_buttons_counter_x = int( 6 ) if buttons_ids[generating_buttons_loop] == 24.01 else int(mngmntcreateNo_buttons_counter_x)

            new_button.size = [int(mngmnt_button_width/3),mngmnt_button_height]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu + shift_mngmntcreateNo_buttons + \
                                     mngmntcreateNo_buttons_counter_x  * The_game_window.mngmt_column_width/3
            new_button.y_corner = (25 + mngmntcreateNo_buttons_counter_y) *  The_game_window.menu_line_spacing

            if mngmntcreateNo_buttons_counter_x == 4:
                mngmntcreateNo_buttons_counter_x = -3
                mngmntcreateNo_buttons_counter_y = 1
            else:
                mngmntcreateNo_buttons_counter_x =  mngmntcreateNo_buttons_counter_x + 1

        # reff behem hry
        elif trunc(buttons_ids[generating_buttons_loop]) == Screens.ingame.value:
            new_button.size = [60,mngmnt_button_height]
            new_button.x_corner = The_field.field_bl_corner [0] +  ref_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_field.field_bl_corner[1] + (ref_buttons_counter2 + 3) * The_game_window.menu_line_spacing
            ref_buttons_counter = ref_buttons_counter + 1
            if ref_buttons_counter == 3:
                ref_buttons_counter = 0
                ref_buttons_counter2 = 2


        # vyber teamu do hry
        elif trunc(buttons_ids[generating_buttons_loop]) == Screens.teamsconfirmation.value:
            new_button.size = [60,mngmnt_button_height]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu + \
                                  choose_teams_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.game_menu_y_end + The_game_window.heading_shift *2
            choose_teams_counter = choose_teams_counter + 1

        # trenovani teamu
        elif trunc(buttons_ids[generating_buttons_loop]) == Screens.trening.value:

            new_button.size = [mngmnt_button_width ,mngmnt_button_height]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu + \
                                     trening_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                                    The_game_window.mngmt_text_ratio *  The_game_window.menu_line_spacing
            trening_buttons_counter = trening_buttons_counter + 2
            if buttons_ids[generating_buttons_loop] != 4.10  :
                new_button.size[0] = 1.6 * mngmnt_button_width

            letter_width = MENU_FONT.size("a")[0]
            frame_charatres_lenght = int(new_button.size[0] / letter_width)
            new_button.name = center_button_name( button_name_original, frame_charatres_lenght)

        # trenovani-manual teamu   # !counter pricita 1/3 !
        elif trunc(buttons_ids[generating_buttons_loop]) == Screens.treningmanual.value:
            lines = 26 if treningman_buttons_counter >= 8 else 25
            if treningman_buttons_counter == 0:
                shift_x = 0
            first_button_x = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu + \
                                     2* The_game_window.mngmt_column_width

            center_button_name( button_name_original, 14) if generating_buttons_loop > 15 else button_name_original
            new_button.size = [int(mngmnt_button_width/3) ,mngmnt_button_height]
            if new_button.number <= 42.02 or new_button.number == 42.09 :
                new_button.size[0] = mngmnt_button_width

            new_button.x_corner = first_button_x + shift_x
            new_button.y_corner =  lines *  The_game_window.menu_line_spacing

            shift_x = shift_x + new_button.size[0]
            if treningman_buttons_counter == 7 :
                shift_x = The_game_window.mngmt_column_width

            treningman_buttons_counter = treningman_buttons_counter + 1


        # zobrazeni menu
        elif trunc(buttons_ids[generating_buttons_loop]) == Screens.help.value:
            new_button.frame = True
            new_button.size = [100,22]
            new_button.x_corner = 0
            new_button.y_corner = 0

        # integer kontrola
        new_button.x_corner = int(new_button.x_corner)
        new_button.y_corner = int(new_button.y_corner)

    # vraci list vsech tlacitek
    return list_buttons_instances


# tisk urciteho n-tlacitka z seznamu tlacitek
def draw_button_No(The_game_window,button_no):
    # pokud tlacitko nema grafiku(obrazek) vykresli se jako text s rameckem
    if The_game_window.buttons[button_no].graphic == "notset":

        # ramecek tlacitka
        # pozice_x,pozive_y,delka,vyska
        if The_game_window.buttons[button_no].frame == True :

            if True:
                rectangle_details = [The_game_window.buttons[button_no].x_corner + 2 ,The_game_window.buttons[button_no].y_corner, \
                                    The_game_window.buttons[button_no].size[0] - 4, The_game_window.buttons[button_no].size[1] - 2]

                button_background = pygame.draw.rect(The_game_window.surface, GREY_BUTTONS, rectangle_details, 0, 5)

        button_name = MENU_FONT.render(The_game_window.buttons[button_no].name, 1, GREY)
        The_game_window.surface.blit(button_name,(The_game_window.buttons[button_no].x_corner, \
                                                    The_game_window.buttons[button_no].y_corner))


# vykresli hlavni menu
def draw_main_menu(The_game_window):
    # pocet tlacitek hlavniho menu
    MAIN_MENU_BUTTONS = 17

    # menu nadpis
    menu_heading = "GAME MENU"
    menu_menu_heading_pages = MENU_FONT_HEADING.render(menu_heading, 1, GREEN_FIELD)
    The_game_window.surface.blit(menu_menu_heading_pages,(The_game_window.game_menu_x_start, 0.25 * The_game_window.menu_line_spacing))

    # Loop pro vypsani celeho menu
    for menu_loop in range(0,MAIN_MENU_BUTTONS):
        draw_button_No(The_game_window, menu_loop)

        if menu_loop <10:
            # TESTY kontrola vykreslovani
            test_print_x = TEST_FONT.render("x", 1, RED)
            The_game_window.surface.blit(test_print_x, (The_game_window.game_menu_x_start, \
                                                        menu_loop * The_game_window.menu_line_spacing + The_game_window.heading_shift))


'''
PLAN VYPRACOVANI
Rozdeleni okna aplikace 4x ruzne plochy (4 x ID area)
 ___________________         ___________________
| 1 | 3             |       | 4                 |
|   |               |       |                   |
|___|_______________|   =>  |___________________|
| 2                 |       | 2                 |
|___________________|       |___________________|

'''

# okno rozdeleno na 3 casti
def draw_menu_lines_ID_3(The_game_window,screen_ID):
    #rozdeleni obrazovky aplikace
    pygame.draw.rect(The_game_window.surface, WHITE, \
                        (0, 0, The_game_window.window_width, The_game_window.window_height), 1)
    pygame.draw.lines(The_game_window.surface, GREY, \
                        True, ((The_game_window.game_menu_x_end, 0), \
                       (The_game_window.game_menu_x_end, The_game_window.game_menu_y_end)), 1)

    if screen_ID == Screens.trening.value:
        line_lenght = The_game_window.game_menu_x_end + 7.5*The_game_window.mngmt_column_width \
                        + The_game_window.mngmt_shift_from_menu
    else:
        line_lenght =  The_game_window.window_width

    pygame.draw.lines(The_game_window.surface, GREY, \
                       True, ((0 ,The_game_window.game_menu_y_end),  \
                       (line_lenght, The_game_window.game_menu_y_end)), 1)

# zapas => menu je ukryto - okno rozdeleno na 2 casti
def draw_menu_lines_ID_4(The_game_window):
    #rozdeleni obrazovky aplikace
    pygame.draw.rect(The_game_window.surface, WHITE , (0, 0, The_game_window.window_width, The_game_window.window_height), 1)
    pygame.draw.lines(The_game_window.surface,  GREY, True, ((0, The_game_window.game_menu_y_end ),  \
                                                             (The_game_window.window_width, The_game_window.game_menu_y_end)), 1)


# volani funkce/metody dle volby z menu(tlacitek)
def f_menu_selected(position_clicked,The_game_window,The_field,The_reff,screen_ID_lower_screen):
    #print (position_clicked)
    #print ( trunc(position_clicked))
    screen = screen_ID_lower_screen[0]
    lower_screen = screen_ID_lower_screen[1]
    button_selected = position_clicked

    for index_button_loop in range (0,len(The_game_window.buttons)):
        if The_game_window.buttons[index_button_loop].number == button_selected:
            index_selected_button = index_button_loop
            break

    ## tlacitka zacinajici indexem 0 => hlavni menu
    if  trunc(button_selected) == 0 and The_game_window.menu_on_screen == True:

        # trener
        if  button_selected == 0.10:  #testy
            draw_5aside_field(The_game_window,The_field,Screens.intrening.value)
            draw_field_sectors(The_game_window,The_field)
            draw_field_subsectors(The_game_window,The_field)
            screen = Screens.intrening.value
            The_game_window.menu_on_screen = False

        elif  button_selected == 0.11:
            The_reff.coach_team_A.reset_selected_slot_team_management()
            screen = Screens.teammanagement.value

            #testy

            for llloptest in range(0,10):
                if The_reff.coach_team_A.loaded_teams_xml[llloptest] != SavingType.empty_team_slot.value:
                    for llloptest2 in range(0,6):
                        pass
                        #print (The_reff.coach_team_A.loaded_teams_xml[llloptest][llloptest2])

        elif  button_selected == 0.12:
            The_reff.coach_team_A.reset_selected_slot_team_management()
            screen = Screens.trening.value
        elif  button_selected == 0.13:
            The_reff.coach_team_B.reset_selected_slot_team_management()
            screen = Screens.teammanagementaway.value
        elif  button_selected == 0.14:
            screen = Screens.stats.value
        # reff
        elif  button_selected == 0.20: #testy
            '''
            The_reff.teams_for_game = ["C","B","H","H"]
            teams_threds = [False,False]
            called_at_begining = True
            The_reff.start_match (The_field, called_at_begining, teams_threds)
            The_game_window.menu_on_screen = False
            screen = Screens.ingame.value
            '''
            pass

        elif  button_selected == 0.21:
            pass
        elif  button_selected == 0.22:
            #The_reff.set_teams_type_for_game("H/H")
            #The_reff.coach_team_A.loaded_teams_xml[0][0][2] = "selected"
            #The_reff.coach_team_A.loaded_teams_xml[1][0][2] = "selected"
            if The_reff.count_selected_teams() != 2:
                screen = Screens.error.value                                        #oprav na   draw_teams_selection_error
            else:
                The_reff.load_teams_for_game_to_slot()
                screen = Screens.teamsconfirmation.value

        elif  button_selected == 0.23:
            pass
        elif  button_selected == 0.24:
            if The_reff.game_type != "none":
                #screen = Screens.ingame.value # zpet na zapas pokud nebyl ukoncen
                The_game_window.menu_on_screen = False
        # nastaveni
        elif  button_selected == 0.30:
            pass
        elif  button_selected == 0.31:
            The_game_window.swap_language()
            The_game_window.buttons = create_buttons_instances(The_game_window,The_field)
        elif  button_selected == 0.32:
            #The_game_window.set_window_size(The_field)                                # testovaci hodnoty
            pass
        # lab mode
        elif  button_selected == 0.40:
            pass
        elif  button_selected == 0.41:
            pass
        elif  button_selected == 0.42:
            pass
        elif  button_selected == 0.5: #napoveda
            The_game_window.menu_on_screen = False
            screen = Screens.help.value

    ## tlacitka  hry pro reff
    if trunc(button_selected) == Screens.ingame.value :
        if  button_selected == 71.10 :
            The_reff.pause_game()#The_game_window,The_field)
            screen = Screens.ingame.value
        if  button_selected == 71.20 :
            The_reff.unpause_game(The_game_window,The_field)
        if  button_selected == 71.30 :#testy
            print("gamestatsus"  ,"teamtype"   ,"team"  )
            for no_of_ingamers in range (1,len(The_reff.list_of_ingamers)):#testy
                print(The_reff.list_of_ingamers[no_of_ingamers].game_status, \
                The_reff.list_of_ingamers[no_of_ingamers].team_type , \
                The_reff.list_of_ingamers[no_of_ingamers].team )


    ## tlacitka  team management
    if  trunc(button_selected) == Screens.teammanagement.value  and screen == Screens.teammanagement.value:
        if  button_selected == 2.10 :
            The_reff.coach_team_A.delete_player_from_slot()
        if  button_selected == 2.20 :
            The_reff.coach_team_A.copy_player_from_slot()
        if  button_selected == 2.30 :
            The_reff.coach_team_A.paste_player_from_other_slot()
        if  button_selected == 2.40 :#edit
                The_game_window.buttons[index_button_loop].set_selected_status(True)
                The_game_window.buttons[index_button_loop + 1].set_selected_status(False)
                lower_screen = Screens.teammanagementedit.value
        if  button_selected == 2.50 :#create
                if The_game_window.buttons[index_button_loop].selected == False:
                    The_game_window.buttons[index_button_loop].set_selected_status(True)
                    The_game_window.buttons[index_button_loop - 1].set_selected_status(False)
                    lower_screen = Screens.teammanagementcreate.value
                else:
                    The_game_window.buttons[index_button_loop].set_selected_status(False)
                    The_game_window.buttons[index_button_loop - 1].set_selected_status(True)
                    lower_screen = "notset"

        if  button_selected == 2.60 :
            The_reff.coach_team_A.choose_team_from_selection()
        if  button_selected == 2.70 :
            The_reff.coach_team_A.save_team_from_teammngmt_table()

    ## tlacitka  team managementedit
    if  trunc(button_selected) == Screens.teammanagementedit.value  and screen == Screens.teammanagement.value \
            and lower_screen == Screens.teammanagementedit.value :

        if  button_selected == 21.10 :#GK
            The_reff.coach_team_A.edit_player_position(1)
        if  button_selected == 21.20 :#r def
            The_reff.coach_team_A.edit_player_position(2)
        if  button_selected == 21.30 :#l def
            The_reff.coach_team_A.edit_player_position(3)
        if  button_selected == 21.40 :#midd
            The_reff.coach_team_A.edit_player_position(4)
        if  button_selected == 21.50 :#strker
            The_reff.coach_team_A.edit_player_position(5)

    ## tlacitka  team managementcreate
    if  trunc(button_selected) == Screens.teammanagementcreate.value  and screen == Screens.teammanagement.value \
            and lower_screen == Screens.teammanagementcreate.value :

        if  button_selected == 23.10 :
            The_reff.coach_team_A.create_new_player() #vytv hrace
        if  button_selected == 23.20 :
            The_reff.coach_team_A.create_new_player()

    ## tlacitka  team managementcreateNo
    if  trunc(button_selected) == Screens.teammanagementcreateNo.value  and screen == Screens.teammanagement.value \
        and lower_screen == Screens.teammanagementcreate.value :
        string_number = str (button_selected)
        dot_index = string_number.index('.')
        if button_selected ==24.1:
            result =int(string_number[dot_index +1] + "0")
        else:
            result =int(string_number[dot_index +1] + string_number[dot_index +2])
        print(result,"eeee ")

        The_reff.coach_team_A.set_managementcreateNo(result-1) # button jsou od 1 ale list rozhodciho od 0


    ## tlacitka  team management
    if  trunc(button_selected) == Screens.teammanagementaway.value  and screen == Screens.teammanagementaway.value:
        if  button_selected == 22.10 :
            The_reff.coach_team_B.choose_team_from_selection()


    ## tlacitka  vyber teamu do hry
    if  trunc(button_selected) == Screens.teamsconfirmation.value and screen == Screens.teamsconfirmation.value:
        if  button_selected == 7.10 :
            The_reff.set_teams_type_for_game("H/AI")
        if  button_selected == 7.20 :
            The_reff.set_teams_type_for_game("AI/H")
            pass
        if  button_selected == 7.30 :
            The_reff.set_teams_type_for_game("AI/AI")
            pass
        if  button_selected == 7.40 :
            #hra lze zacit pouze s 2 teamy
            if  The_reff.count_selected_teams() == 2:
                teams_threds = [True, True]
                called_at_begining = True
                The_reff.start_match (The_field, called_at_begining, teams_threds)
                The_game_window.menu_on_screen = False
                screen = Screens.ingame.value
        if  button_selected == 7.50 :#reset  pro reff ze muze zacit nova hra

            The_reff.set_game_status_to_self("none")
            print(The_reff.game_type)
            The_reff.set_game_status_to_players()


    ## tlacitka  vyber teamu do treningu
    if  trunc(button_selected) == Screens.trening.value  and screen == Screens.trening.value:
        if  button_selected == 4.10 :
            The_reff.coach_team_A.copy_player_from_slot() #ulozi trenovaneho hrace do bufferu

        # trening h/h
        if  button_selected == 4.20 :
            The_reff.set_teams_type_for_game("H/H")
            lower_screen = Screens.treningmanual.value
        # trening h/AI
        if  button_selected == 4.30 :
            The_reff.set_teams_type_for_game("AI/H")
            lower_screen = Screens.trainingoffscreen.value
        # trening AI/AI
        if  button_selected == 4.40 :
            The_reff.set_teams_type_for_game("AI/AI")
            The_reff.coach_team_A.automated_trening_type = True
            The_reff.coach_team_B.automated_trening_type = True
            lower_screen = Screens.trainingautomated.value


    ## tlacitka  vyber teamu do treningu
    if  trunc(button_selected) == Screens.treningmanual.value  and screen == Screens.trening.value:
        start_training_check = [False,"empty"]

        #zacne trening
        if  button_selected == 42.01 :
            start_training_check = The_reff.start_training()
            # vyhodnoceni
            if start_training_check[0] == True:
                # prvni team je trenovany
                teams_threds = [False,False]
                called_at_begining = True
                The_reff.start_match (The_field, called_at_begining, teams_threds)
                The_reff.set_game_status_to_players()
                for rest_loop in range (1,len(The_reff.list_of_ingamers)):
                     The_reff.list_of_ingamers[rest_loop].reset_graphic()

                RE_started = False
                for ingamers_loop in range (1,len(The_reff.list_of_ingamers)):                                              #!!!udelat metodu bude treba  3x
                    # nastavi trenovaneho hrace
                    if The_reff.list_of_ingamers[ingamers_loop].ID == start_training_check[1]:

                        The_game_window.menu_on_screen = False
                        screen = Screens.intrening.value

                        if The_reff.teams_for_game[2] == "AI" and The_reff.teams_for_game[3] == "AI":

                            The_reff.list_of_ingamers[ingamers_loop].reinforsment = True

                            The_game_window.surface.fill(BLACK,(The_game_window.game_menu_x_end,The_game_window.game_menu_y_end +5, 300,100))
                            The_game_window.surface.blit(MENU_FONT.render(' TRENING .... :)', 1, GREY),(The_game_window.game_menu_x_end, 30 * The_game_window.menu_line_spacing))
                            pygame.display.flip()

                            coach = The_reff.list_of_ingamers[ingamers_loop].team_coach
                            coach.move_players_for_new_training_run (The_field,The_reff.list_of_ingamers)

                            # The_reff.list_of_ingamers[ingamers_loop].set_selected(False)

                            # reinforsment
                            trained_player =  The_reff.list_of_ingamers[ingamers_loop]
                            trained_player.reinforsment = True
                            trained_player_ID = trained_player.ID

                            The_reff.list_of_ingamers[0].reinforsment = True  #  ball

                            The_RE_env = TrainingEnvironment()
                            The_RE_env.load_data (The_reff.list_of_ingamers, trained_player, The_field, The_game_window, The_reff, True)
                            model = The_reff.list_of_ingamers[ingamers_loop].model
                            actions = 5 # hrac muze udelat 5 akci

                            for ingamers_loop in range (0, coach.trening_repetition_total):

                                run_RE_trening(model, actions, The_RE_env, trained_player_ID, coach.RE_trening_sesion_runs )
                                coach.trening_repetition_sequence = coach.trening_repetition_sequence + 1

                            # reset screenu po treningu
                            screen = Screens.trening.value
                            The_game_window.menu_on_screen = True
                            lower_screen = Screens.trainingautomateddone.value
                            full_path = get_path_home_folder()
                            trained_player.model= load_model( full_path +  trained_player_ID + ".h5")
                            coach.update_trening_time(trained_player_ID, training_runs)
                            '''
                            trained_player.save_trening_time (coach.RE_trening_sesion_runs)
                            for save_loop  in range (0,len(coach.loaded_teams_xml)):
                                if coach.loaded_teams_xml[save_loop][0][1] == "original":
                                    create_xml_file(coach.loaded_teams_xml[save_loop])
                            '''

                        else:
                            The_reff.list_of_ingamers[ingamers_loop].reinforsment = False
                            The_reff.list_of_ingamers[ingamers_loop].set_selected(True)
                        The_reff.list_of_ingamers[ingamers_loop].team_coach.active_trening = True
                        The_reff.list_of_ingamers[ingamers_loop].team_coach.reset_training_arrays()
                    #screen = Screens.intrening.value
                    #screen = Screens.trainingoffscreen.value

        #print (  "---check --   plr ",  The_reff.coach_team_A.training_areas_player )
        #print (  "---check --   bll ",  The_reff.coach_team_A.training_areas_ball )

        # trening area
        if button_selected >= 42.03 and  button_selected <= 42.08:
            The_reff.coach_team_A.set_training_areas_player((round((button_selected - 42.03),2)) * 100)

        if button_selected >= 42.10 and  button_selected <= 42.15:
            The_reff.coach_team_A.set_training_areas_ball((round((button_selected - 42.10),2)) * 100)

        #print (  "button_selected " ,button_selected )
        #print (  "button_selected " ,button_selected )
        #print (  "--- --           ---- " ,round((button_selected - 42.10),2) * 100)
        #print (  "---check --   plr ",  The_reff.coach_team_A.training_areas_player )
        #print (  "---check --   bll ",  The_reff.coach_team_A.training_areas_ball )

    ## zobrazeni schovaneho menu
    if  trunc(button_selected) == Screens.help.value :
        if  button_selected == 15.10:
            The_game_window.menu_on_screen = True
            if screen == Screens.help.value:
                screen = Screens.welcome.value

    # vraci novou obrazovku dle menu nebo tlacitek                                                                                       # spustit hru
    return [screen,lower_screen]


#-----------------------------------------------------------TEXTY--------------------------------------------------------

def all_buttons_names(app_language):
    if app_language == "CZ":
        menu_list = ["TRENER","  -Trener domacich","  -Trening  ","  -Trener hostu","  -Stats","ROZHODCI ",  "  -Delka utkani", "  -Potvrdit teamy ", "  -Nastaveni hriste ","  -Zpet na hriste",  \
                    "NASTAVENI ","  -Language / Jazyk", "  -Velikost okna","LAB ", "  -zapnout lab mod","  -vypnout grafiku" ,"Napoveda "]
        team_management_buttons = ["smazat" ,"kopirovat","vlozit","upravit","novy hrac","un/select","ulozit"]
        edit_player = [" GK "  ,"R def"  ,"L def"  ," Mid"  ,"Striker"   ]
        create_player = ["Generovat"  ,"level:    "  ]
        create_player_No = [ "  1","  2","  3","  4","  5","  6","  7","  8","  9"," 10"," 11"," 12"," 13"   ]
        team_managementaway_buttons = [" un/select ", ]
        trening_buttons = ["potvrd","  staticky" ," Manualni ", " automaticky"]
        treningman_buttons = ["start","hrac zone", "  A","  B", "  C",   "  1","  2","  3","mic zone", "  A","  B", "  C",   "  1","  2","  3"]
        confirm_teams_for_game = ["H/AI" , "AI/H", "AI/AI","zacithru", "ukoncit rozehranou hru"]
        reff_at_game_buttons = ["pause", "unpause"," grid "," 3 "," 4 "]
        back_to_menu = ["MENU "]
    else:
        menu_list = ["COACH ","  -Coach home team","  -Training  ","  -Coach opponents","  -Stats","REFF ","  -Match lenght", "  -Teams for game  ", "  -Field settings ","  -back to game field", \
                    "SETTINGS ","  -Language / Jazyk", "  -Resolution","LAB ",  "  -Lab mode on/off","  -Graphic on/off" ,"HELP    "]
        team_management_buttons = ["smazat" ,"kopirovat","vlozit","upravit","novy hrac","un/select","ulozit"]
        edit_player = ["GK"  ,"R def"  ,"L def"  ,"Mid"  ,"Striker"   ]
        create_player = ["  GO"  ,"level:    "  ]
        create_player_No = [ "1","2","3","4","5","6","7","8","9 ","10","11","12","13"   ]
        team_managementaway_buttons = [" un/select ", ]
        trening_buttons = ["select","MN stat trng h/h" ,"MN dyn trng h/ai ", " AUT starttrenng ai/ai"]
        treningman_buttons = ["ssstart","hrac zone", "  A","  B", "  C",   "  1","  2","  3" , "msic zone", "  A","  B", "  C",   "  1","  2","  3"]
        confirm_teams_for_game = ["H/AI" , "AI/H", "AI/AI","start game", "cancel started game"]
        reff_at_game_buttons = ["pause", "unpause"," grid "," 3 "," 4 "]
        back_to_menu = ["MENU "]

    # tlacitka krom menu
    other_buttns_list = team_management_buttons + edit_player + create_player + create_player_No + team_managementaway_buttons + \
                            trening_buttons + treningman_buttons + confirm_teams_for_game + reff_at_game_buttons + back_to_menu
    # vsechny tlacitka
    buttons_names_list = menu_list + other_buttns_list

    return buttons_names_list


def all_buttons_IDs():
    '''
    ID zacinajici 0 je pro hlavni menu, cislovani odpovida kategoriim & podkategoriim v menu
    ID zacinajici cislem odpovidaji scren enums pro ktere je tlacitko aktivni
    '''
    buttons_ids = [ 0.10, 0.11, 0.12, 0.13, 0.14, 0.20, 0.21, 0.22, 0.23, 0.24, 0.30, 0.31, 0.32, 0.40 , 0.41, 0.42, 0.50, \
                    2.10, 2.20, 2.30, 2.40, 2.50, 2.60, 2.70, \
                    21.10, 21.20, 21.30, 21.40, 21.50,  \
                    23.10, 23.20, \
                    24.01, 24.02, 24.03, 24.04, 24.05, 24.06, 24.07, 24.08, 24.09, 24.10, 24.11, 24.12, 24.13,  \
                    22.10, \
                    4.10, 4.20, 4.30 , 4.40, \
                    42.01, 42.02, 42.03, 42.04, 42.05, 42.06, 42.07, 42.08, 42.09 ,42.10, 42.11, 42.12, 42.13, 42.14,42.15,   \
                    7.10, 7.20, 7.30, 7.40, 7.50, \
                    71.10, 71.20, 71.30, 71.40, 71.50, \
                    15.10 ]

    return buttons_ids
