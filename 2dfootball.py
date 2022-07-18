import pygame
import sys
import os.path
from os import path
import support_functions
from support_functions import *
import xml_f
from xml_f import *
import f_menu
from f_menu import *
import f_clases
from f_clases import *
import class_ingamer
from class_ingamer import *
import class_player_ball
from class_player_ball import *
import screens
from screens import *

#pygame modul
pygame.init()
from pygame.locals import *                 # zkontrolovat import

clock = pygame.time.Clock()

# vytvoreni okna , hraciho hriste a rozhotciho
The_game_window = game_window()
pygame.display.set_caption(" Flatball ")

key_down = 0                            # ukazatel pro event z klavesnice
was_clicked = 0                         # ukazatel pro event od mysi
position_clicked = [0,0]                # detail pro event od mysi
game_inicialisation = False             # test pred spustenim hry
#game_menu_active = True                # zobrazeni hlavniho menu
game_menu_selcection = 'A'              # zkontroluj
screen_ID_lower_screen = [0,0]          # welcome screen  list  screen_ID a lower_Screen
screen_ID = 0
lower_screen_ID = 0                     # cislo zobrazeni dolni casti okna
selected_player = 'emptynow'            # pro volani vykresleni lower menu
action_for_player = False               # zkontrolovat
#team_management_buffer = "emptynow"     #
screen_ID_buffer = 'emptynow'           # kontrola prepnuti z zapocate hry                    ?pouzito
ball_index = 0

# vytvoreni slozek teamu, nahrani treningu z predesle hry
# pokud prvni spusteni vytvoreni defaultniho teamu
f_teams_folders_check()

The_field = game_field()
The_field.set_field(The_game_window)
The_reff = reff()
                                                                                                    #---- PREDELAT settings data neni treba
if path.exists("setings_data"):
    game_inicialisation = True
else:
    game_inicialisation = False

# vygeneruje tlacitka menu                                                                              #? mozna udelej metodu add_buttons
The_game_window.buttons = create_buttons_instances(The_game_window,The_field)


#testy
#print("----testy-------------------------------")
#print ("The_game_window.window_height",The_game_window.window_height  )
#print ("The_game_window.width",The_game_window.window_width  )
if False:
    for btnloop in range (0,len(The_game_window.buttons)):
        print(vars(The_game_window.buttons[btnloop]))

    print ("The_game_window.menu_line_spacing ", The_game_window.menu_line_spacing)
    print ("The_game_window.window_height",The_game_window.window_height  )
if False:
    print("-fitrening  ",The_reff.coach_team_A.training_areas_player )
    print("-field_bl_corner ",The_field.field_bl_corner )
    print("--testy---------------------------------")



# --------------MAIN GAME LOOP-------------
while True:

    for event in pygame.event.get():                                                                              # opravit ball a reff indexy sou hardcoded v loop ne uplne supr reseni
        if event.type == QUIT:
            The_reff.pause_game()#The_game_window,The_field)
            sys.exit()
        if event.type == VIDEORESIZE:                                                         # <<<<<<>>>>>>>   udelat jako jednu metodu  'resize request check'
            if event.w > 1140 and event.h > 620:
                The_game_window.surface = pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)
                The_game_window.set_window_size([event.w,event.h],The_field)
                The_game_window.resize_values()
                The_game_window.buttons = create_buttons_instances(The_game_window,The_field)                         #   delaji se nove buttons?? nemaji se jen resize?
            else:
                if event.w < 1140:
                    The_game_window.surface = pygame.display.set_mode((The_game_window.window_width,The_game_window.window_height),pygame.RESIZABLE)
                if event.h < 620:
                    The_game_window.surface = pygame.display.set_mode((The_game_window.window_width,The_game_window.window_height),pygame.RESIZABLE)


        #-------------------- KLAVESNICE ------------------
        if event.type == KEYDOWN:                                                                # !!! events udelat lip loop se opakuje ,mozna events jako samsotatna knihovna ?
            key = pygame.key.get_pressed()

            if key[K_SPACE]:    # mozna dodelat 2 klavesy kick/ pass

                for no_of_ingamers in range (1,len(The_reff.list_of_ingamers)):

                    if The_reff.list_of_ingamers[no_of_ingamers].selected_b == True and \
                       The_reff.list_of_ingamers[0].owner == The_reff.list_of_ingamers[no_of_ingamers] :

                        ball_angle = The_reff.list_of_ingamers[no_of_ingamers].calculate_angle_to_other_object(The_reff.list_of_ingamers[0].rect.center)
                        vision_angle = The_reff.list_of_ingamers[no_of_ingamers].path_target
                        diff_ball_to_vision = abs (ball_angle - vision_angle )

                        # pokud se hrac diva jinam nezli kop,mic dostane min energie  70%
                        if diff_ball_to_vision > 20:
                            The_reff.list_of_ingamers[0].speed = int (200 * 0.7)
                        else:
                            The_reff.list_of_ingamers[0].speed = 200

                        '''
                        ukladani dat pro trening, screen_ID = 8
                        data pro nejjednodusi keras model
                        0: otoc +10 stupnu
                        1: otoc -10 stupnu
                        2: krok
                        3: kop do mice
                        4: bez akce
                        '''
                        if screen_ID == Screens.intrening.value and \
                           The_game_window.menu_on_screen == False and \
                           The_reff.list_of_ingamers[no_of_ingamers].team_type == "H":

                            The_reff.list_of_ingamers[no_of_ingamers].send_data_to_coach(3,The_reff.list_of_ingamers,The_field)


            # klavesa uzita jen pro trening n =>'no action'
            if key[K_e] and screen_ID == Screens.intrening.value and \
               The_game_window.menu_on_screen == False:

                # selected_player = list_of_ingamers[4]                                                            #testy vykresli detail hrace mozna pouzit
                for no_of_ingamers in range (1,len(The_reff.list_of_ingamers)):
                    if The_reff.list_of_ingamers[no_of_ingamers].selected_b == True and \
                       The_reff.list_of_ingamers[no_of_ingamers].team_type == "H":

                        The_reff.list_of_ingamers[no_of_ingamers].send_data_to_coach(4,The_reff.list_of_ingamers,The_field)

            # krok
            if key[K_w]:
                key_down = True


            # ukonceni treningu
            if key[K_p]:
                if screen_ID == Screens.intrening.value:
                    if The_reff.coach_team_A.active_trening == True :
                        The_reff.coach_team_A.active_trening = False
                    else:
                        The_reff.coach_team_B.active_trening = False

                    # spust vyhodnoceni dat?
                    # smazat ingamer krom mice a reff
                    screen_ID = Screens.trening.value

        if event.type == KEYUP:                                                                                  # !!!!!!!!!!kontrola events udelat lip loop se opakuje
            key_down = False


        # ----------------------- MYS ---------------------
        if event.type == MOUSEBUTTONDOWN:
            was_clicked = 1
            position_clicked = pygame.mouse.get_pos()
            selected_player = "emptynow"
            if screen_ID == Screens.ingame.value: #funkcnost aktivni jen pri hre
                for no_of_ingamers in range (0,len(The_reff.list_of_ingamers)):
                    #pridej kontrolu pro trening,nelze select odthers      # pride kontrolu pri hre human/pc musi u teamu human by vzdy jeden hrac oznaceny
                    if The_reff.list_of_ingamers[no_of_ingamers].is_selected_by_click (position_clicked) == True and \
                        The_reff.list_of_ingamers[no_of_ingamers].team_type != "AI":#nelze oznacit AI team

                        The_reff.list_of_ingamers[no_of_ingamers].set_selected(True)
                        selected_player = The_reff.list_of_ingamers[no_of_ingamers]
                    else:
                        The_reff.list_of_ingamers[no_of_ingamers].set_selected(False)


            # nove rozestaveni pro trening
            if screen_ID == Screens.intrening.value and event.button == 3 :
                The_reff.coach_team_A.move_players_for_new_training_run (The_field,The_reff.list_of_ingamers)


        if event.type == MOUSEMOTION:                                                       # jen pri hre ? jinak neni potreba??zkontroluj
            position_over = pygame.mouse.get_pos()
            over_x = position_over[0]
            over_y = position_over[1]
            # set_path se nenastavuje prvnim dvou clenum reff a ball, reff se nehybe a ball dostava koordinace od metod
            for no_of_ingamers in range (1,len(The_reff.list_of_ingamers)):
                if The_reff.list_of_ingamers[no_of_ingamers].selected_b == True and The_reff.list_of_ingamers[no_of_ingamers].team_type == "H" :
                    new_angle = The_reff.list_of_ingamers[no_of_ingamers].calculate_angle_to_other_object(position_over)
                    original_target = The_reff.list_of_ingamers[no_of_ingamers].path_target
                    if round(-original_target + new_angle ) >= 0:                                                                       #zkontroluj znamenko
                        angle_done = 0 # +10 stupnu pootoceni
                    else:
                        angle_done = 1 # -10 stupnu pootoceni
                    The_reff.list_of_ingamers[no_of_ingamers].set_path_target(new_angle)

                    if screen_ID == Screens.intrening.value and \
                      The_game_window.menu_on_screen == False and \
                      The_reff.list_of_ingamers[no_of_ingamers].reinforsment == False and \
                      The_reff.list_of_ingamers[no_of_ingamers].team_type == "H":

                        The_reff.list_of_ingamers[no_of_ingamers].send_data_to_coach( angle_done,The_reff.list_of_ingamers,The_field  )


                    #zapamatuj kde je vyber menu podle toho volej co se ma stat metoda/funcke

    # musi byt mimo event aby se mohl hrac pohybovat pri stisknutem W
    if key_down == True:

        for no_of_ingamers in range (1,len(The_reff.list_of_ingamers)):
            if The_reff.list_of_ingamers[no_of_ingamers].selected_b == True :

                The_reff.list_of_ingamers[no_of_ingamers].move(The_field,The_reff.list_of_ingamers)

                if screen_ID == Screens.intrening.value and \
                   The_game_window.menu_on_screen == False  and  \
                   The_reff.list_of_ingamers[no_of_ingamers].team_type == "H":

                    # data tracking , action krok
                    The_reff.list_of_ingamers[no_of_ingamers].send_data_to_coach(2,The_reff.list_of_ingamers,The_field)

    if was_clicked == 1:
        screen_ID_buffer = screen_ID                                                                                     #-----dej do mousedown    ??              # pridat test value z kontroly slozek a soboru na zacatku => kdyz nok nespusti se hra ale eerrror message

        for button_index in range (0,len(The_game_window.buttons)):
            button_ID = The_game_window.buttons[button_index].is_mouse_over_button (position_clicked,screen_ID_lower_screen, The_game_window.menu_on_screen)

            if button_ID != "nomatch":
                screen_ID_lower_screen = f_menu_selected(button_ID,The_game_window,The_field,The_reff,screen_ID_lower_screen)   # zkontroluj kdyz ma screeen id je potreba podminka??
                screen_ID = screen_ID_lower_screen[0]
                lower_screen_ID = screen_ID_lower_screen[1]

                # pri odchodu z hry nebo treningu maji hraci pause                                              # elegantneji udelat metodu pause pro reff
                if (screen_ID_buffer == Screens.ingame.value or screen_ID_buffer == Screens.intrening.value) and trunc(button_ID) != Screens.ingame.value:
                    if screen_ID != Screens.ingame.value or screen_ID != Screens.intrening.value:
                        for no_of_ingamers in range (1 , len(The_reff.list_of_ingamers)):
                            The_reff.list_of_ingamers[no_of_ingamers].game_status = "pause"


        # vyber radku
        if  screen_ID == Screens.trening.value or screen_ID == Screens.teammanagement.value or screen_ID == Screens.teammanagementaway.value:
            The_reff.coach_team_A.calculate_slot_index(position_clicked,The_game_window)
            The_reff.coach_team_B.calculate_slot_index(position_clicked,The_game_window)

        was_clicked = 0

    ###------------------konec kontroly eventu--------------------------------------------------------------

    #record training data                                                                                   # predelano na metody zkontroluj
    if action_for_player == True:
        #record data
        #reset
        action_for_player = False

    '''
    # posune mic v pripade ze ma nejakou energii (speed)                                                     #  --?? patri do screen hry/treningu ne jen tak !!!!
    The_ball.moving(The_game_window,The_field,list_of_ingamers)
    '''
    The_game_window.surface.fill(BLACK)

    # vykresli pozadovanou obrazovku
    if screen_ID == Screens.welcome.value:                                                                                       # dat do menu knihovny?  opravid indexy a jmena podle wordu
        draw_weclome(The_game_window)

    if screen_ID == Screens.teammanagement.value: # team nanagement
        draw_team_managemet(The_game_window,The_field,The_reff,screen_ID)                     # staci ferr nebo all ingamers?zkontroluj
        f_print_teammngmt_buttons(The_game_window)

        if lower_screen_ID == Screens.teammanagementedit.value:
            f_print_edit_player_buttons(The_game_window)
        elif lower_screen_ID == Screens.teammanagementcreate.value:
            f_print_create_player_buttons(The_game_window,The_reff.coach_team_A)
            f_print_createPlr_details(The_game_window,The_reff.coach_team_A.trainig_code,False )

        if lower_screen_ID != Screens.teammanagementcreate.value:
            f_print_player_details_off_game(screen_ID,The_reff,The_game_window)

    # away team
    if screen_ID == Screens.teammanagementaway.value:
        draw_team_managemet(The_game_window,The_field,The_reff,screen_ID)                     # staci ferr nebo all ingamers?zkontroluj
        f_print_teammngmtaway_buttons(The_game_window)
        f_print_player_details_off_game(screen_ID,The_reff,The_game_window)

    if screen_ID == Screens.teamsconfirmation.value: # vyber tymu do hry
        draw_teams_for_game(The_game_window,The_field,The_reff)
        f_print_teams_for_game_buttons (The_game_window)


    if screen_ID == Screens.trening.value : # vyber teamu a hrace pro trening
        if lower_screen_ID == Screens.trainingautomateddone.value:
            f_print_treningman_buttons(The_game_window,Screens.trainingautomated.value)
            f_print_RE_trening_done(The_game_window)

        draw_team_managemet(The_game_window,The_field,The_reff,screen_ID)
        f_print_trening_buttons(The_game_window)
        f_print_player_details_off_game(screen_ID,The_reff,The_game_window)
        draw_trening_mini_filed(The_game_window, The_reff , The_field)
        #print ("lower_screen_ID",lower_screen_ID)
        if lower_screen_ID >= Screens.treningmanual.value and \
            lower_screen_ID <= Screens.trainingautomated.value:

            f_print_treningman_buttons(The_game_window,lower_screen_ID)

    if screen_ID == Screens.trainingoffscreen.value:
        f_print_trening_progress(The_game_window,The_field,The_reff.coach_team_A,The_reff.coach_team_B)
        draw_trening_off_screen(The_game_window)

    if screen_ID == Screens.stats.value:#stats
        draw_stats(The_game_window,The_reff)

                                                                                                             # 2 krat podminka pro stejny screen????
    if screen_ID == Screens.ingame.value or screen_ID == Screens.intrening.value : # hriste (hra / trening)
        # TE£ST VSE V JEDNOM VLAKNU
        #The_reff.coach_team_A.move_around_team(The_field,The_reff.list_of_ingamers)
        #The_reff.coach_team_B.move_around_team(The_field,The_reff.list_of_ingamers)
        # /TE£ST VSE V JEDNOM VLAKNU

        if The_game_window.menu_on_screen == True:
            draw_paused_game(The_game_window)

        # posune mic v pripade ze ma nejakou energii (speed)
        The_reff.list_of_ingamers[ball_index].moving(The_field,The_reff)                                             # zastavi se pri paused game????

        draw_5aside_field (The_game_window,The_field,screen_ID)

        if selected_player != "emptynow" :                                                                   # potrebuju promenou selected player??zkontroluj
            selected_player.draw_data_lower_menu (The_game_window,The_field,The_reff.list_of_ingamers)
                                                                                                            # delam 2 x redraw ??? v loop a taky v metode
        if screen_ID == Screens.intrening.value :
            f_print_trening_progress(The_game_window,The_field,The_reff.coach_team_A,The_reff.coach_team_B)
            draw_field_sectors(The_game_window,The_field)
            draw_field_subsectors(The_game_window,The_field)
            if lower_screen_ID != Screens.trainingautomated.value:
                f_print_help_trening(The_game_window)

            if True :  # testy
                draw_training_area (The_game_window,The_reff.coach_team_A.testdata1,BLUE)
                draw_training_area (The_game_window,The_reff.coach_team_A.testdata2,GREY_LINES)
                #draw_training_area_surface (The_game_window,The_reff.coach_team_A.testdata1,BLUE)
                #draw_training_area_surface (The_game_window,The_reff.coach_team_A.testdata2,GREY_LINES)

            for no_of_ingamers in range (1,len(The_reff.list_of_ingamers)):                                            # vyresit elegantneji , selected bud eporad stejny hrac , mozna ulozit do trenera
                if The_reff.list_of_ingamers[no_of_ingamers].selected_b == True :
                    The_reff.list_of_ingamers[no_of_ingamers].draw_data_lower_menu (The_game_window,The_field,The_reff.list_of_ingamers)
        else:
            The_reff.draw_ingamer(The_game_window)
            The_reff.draw_data_lower_menu(The_game_window,The_field)

        for no_of_ingamers in range (0,len(The_reff.list_of_ingamers)):
            The_reff.list_of_ingamers[no_of_ingamers].draw_ingamer(The_game_window)



    if screen_ID == Screens.help.value : # napoveda
        f_print_help(The_game_window)

    if screen_ID == Screens.error.value :
        draw_error(The_game_window)


    # vykresli game menu & rozdeleni obrazovky, pri zapase je neaktivni
    if The_game_window.menu_on_screen == True :
        The_game_window.surface.fill(BLACK,(0,0,The_game_window.game_menu_x_end,The_game_window.game_menu_y_end))
        draw_main_menu(The_game_window)
        draw_menu_lines_ID_3(The_game_window,screen_ID)
        print_check_pin(The_game_window)
    else:
        if screen_ID != Screens.help.value:
            draw_menu_lines_ID_4(The_game_window)    # napoveda je jen jedno okno
        #draw_menu_icon(The_game_window)
        f_print_dysplay_menu_button(The_game_window)


    #pygame.display.update()
    pygame.display.flip()
    clock.tick(60)                                                                                              #60 pro normalni hru jinak pro testy
