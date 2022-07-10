import f_menu
from f_menu import *


# -------------------------------------------SCREENS---------------------------------------------------

def draw_teams_for_game(The_game_window,The_field,The_reff):
    shift_from_menu = The_game_window.mngmt_shift_from_menu
    table_line_spacing = int(1.8 * The_game_window.menu_line_spacing)
    column_width = 1* The_game_window.mngmt_column_width
    lines = 14
    columns = 10

    table_top = The_game_window.heading_shift
    table_left = shift_from_menu + The_game_window.game_menu_x_end
    table_bottom = table_top + lines * table_line_spacing
    table_right = table_left + columns * column_width

    team_shift_y = 7 * table_line_spacing  # nazev teamu + 6*hrac = 7
    draw_columns = True

    header = MENU_FONT_HEADING.render('Teams for game', 1, GREY)
    The_game_window.surface.blit(header,(table_left, 0.1 * The_game_window.menu_line_spacing))
    headings = f_teams_for_game_headings_text(The_game_window.language)

    for teams_loop in range (0,2):
        draw_columns = True
        team_name = MENU_FONT.render("Team " + The_reff.teams_for_game[teams_loop][0][0] + "    *"  \
                                    + The_reff.teams_for_game[teams_loop + 2] + "*", 1, GREY)

        The_game_window.surface.blit(team_name,(table_left ,table_line_spacing  \
                                                + table_top + teams_loop * team_shift_y))

        pygame.draw.lines(The_game_window.surface, GREY_LINES, True, \
                                ((table_left, table_top + teams_loop * team_shift_y), \
                                 (table_right, table_top + teams_loop * team_shift_y)), 1)

        pygame.draw.lines(The_game_window.surface, GREY_LINES, True, \
                                ((table_right, table_bottom), (table_left, table_bottom)), 2)

        # lines
        for player_loop in range (1,6):  # 1 nazev teamu +  5 hracu  => 6 radku
            pygame.draw.lines(The_game_window.surface, GREY_LINES, True, \
                                ((table_left, (player_loop+1) * table_line_spacing + table_top + teams_loop * team_shift_y ), \
                                 (table_right, (player_loop+1) * table_line_spacing + table_top + teams_loop * team_shift_y )), 1)

            player = MENU_FONT.render( The_reff.teams_for_game[teams_loop][player_loop][0]   , 1, GREY)
            The_game_window.surface.blit(player, (table_left, (player_loop + 1) * table_line_spacing + table_top + teams_loop * team_shift_y))

            # columns
            for player_column in range (0,columns):
                name_shift = 1 if player_column == 1 else 0
                if draw_columns == True:
                    pygame.draw.lines(The_game_window.surface, GREY_LINES, True, \
                                        ((table_left + (name_shift + player_column) * column_width, table_top), \
                                         (table_left + (name_shift + player_column) * column_width, table_bottom)), 1)

                    a_header = MENU_FONT.render(headings[player_column], 1, GREY)
                    The_game_window.surface.blit(a_header,(player_column * column_width + table_left, table_top + teams_loop * team_shift_y))

            draw_columns = False
            pygame.draw.lines(The_game_window.surface, GREY_LINES, True,((table_right, table_top), \
                                                                         (table_right, table_bottom)), 2)



# teams selection pro hru  MOZNA UZIT PRO STATS???
def draw_stats(The_game_window,The_reff):
    # hodnoty musi by ulozeny v 'window' aby slo vypocitat polohu mysi => spustit metodu/funkci
    list_of_ingamers = The_reff.list_of_ingamers
    lines = 21  # pocet zobrazenych radku
    column_width = int (1.5 * The_game_window.mngmt_column_width)
    table_line_spacing = int (1.2 * The_game_window.menu_line_spacing)
    columns = 7
    text_ratio = The_game_window.selection_game_text_ratio
    shift_from_menu = The_game_window.mngmt_shift_from_menu

    # hranice tabulky teamu
    table_top = The_game_window.heading_shift
    table_left = shift_from_menu + The_game_window.game_menu_x_end
    table_bottom = table_top +  lines * table_line_spacing
    table_right = table_left + columns * column_width

    text = f_stats_text(The_game_window.language)

    The_game_window.surface.blit(text[0],( table_left  ,  0.1 * The_game_window.menu_line_spacing ))

    ## Vykresleni tabulky
    # Rect(left, top, width, height)
    pygame.draw.rect(The_game_window.surface, RED, ( table_left, table_top, \
                                                    columns * column_width, \
                                                     lines * table_line_spacing),1)

    # radky
    shift = 0
    for row_loop in range (0,lines):
        shift = shift + table_line_spacing
        pygame.draw.lines(The_game_window.surface, GREY_LINES, True,((table_left, table_top + shift), \
                                                                        (table_right, table_top + shift)), 1)

    # sloupce
    shift = 0
    for colmn_loop in range (0, columns):
        table_headngs_rendered = MENU_FONT.render(text[1][colmn_loop], 1, GREY)
        The_game_window.surface.blit(table_headngs_rendered, (table_left + shift + column_width/4 , table_top)) # posun 1/4 sirka boxu
        shift = shift + column_width
        pygame.draw.lines(The_game_window.surface, GREY_LINES, True,((table_left + shift, table_top), \
                                                                     (table_left + shift, table_bottom)), 1)

    column_teams_shift =  table_line_spacing
    player_line_shift = 0
    leter_shift_from_boarder = 5    # odsazeni od hran tabulky
    font_diference = 1              # rozdil mezi fontem a linkou

    all_teams = The_reff.coach_team_A.loaded_teams_xml + The_reff.coach_team_B.loaded_teams_xml

    # tisk teamu a hracu
    # domaci teamy 10 slotu , + 2 sloty hoste   => 12, jina barva pro vybrany team
    for teams_loop in range (0,len(all_teams)):

        if all_teams[teams_loop] != SavingType.empty_team_slot.value:  # n prvni char z "none"
            team_color = GREY_LINES
            if all_teams[teams_loop][0][1] != "original" :
                team_color = RED
            team_details = MENU_FONT.render("TEAM " + all_teams[teams_loop][0][0], 1, team_color)
        else:
            team_details = MENU_FONT.render( "  --  ", 1, GREY)
        The_game_window.surface.blit(team_details, (table_left + leter_shift_from_boarder, \
                                                table_top + player_line_shift + column_teams_shift))

        player_line_shift = player_line_shift +  table_line_spacing   # *3 team ma jen jmeno a musi se posunout 3 linie dolus

        column_teams_shift = column_teams_shift + table_line_spacing
        player_line_shift = 0


def draw_team_managemet(The_game_window,The_field,The_reff,screen_ID):
    # hodnoty musi by ulozeny v 'window' aby slo vypocitat polohu mysi => spustit metodu/funkci
    list_of_ingamers = The_reff.list_of_ingamers
    lines = The_game_window.team_detail_lines                               #nema byt ulozene v wnindow ale primo tady
    column_width = The_game_window.mngmt_column_width       #int(1.052 * The_game_window.mngmt_column_width)
    teams_on_page = The_game_window.mngmt_teams_on_page
    text_ratio = The_game_window.mngmt_text_ratio
    shift_from_menu = The_game_window.mngmt_shift_from_menu

    # hranice tabulky teamu
    table_top = The_game_window.heading_shift
    table_left = shift_from_menu + The_game_window.game_menu_x_end
    table_bottom = table_top + text_ratio * lines * The_game_window.menu_line_spacing
    table_right = table_left + teams_on_page * column_width

    # texty
    screen_headeing = teammanagmnt_text_heading(The_game_window.language,screen_ID)
    secreen_details = teammanagmnt_text_buttons(The_game_window.language,screen_ID)

    if screen_ID == Screens.teammanagement.value or screen_ID == Screens.trening.value :
        coach = The_reff.coach_team_A
    elif screen_ID == Screens.teammanagementaway.value:
        coach = The_reff.coach_team_B

    The_game_window.surface.blit(screen_headeing, (table_left,  0.1 * The_game_window.menu_line_spacing))
    The_game_window.surface.blit(secreen_details[0], (table_left,  21.5 * The_game_window.menu_line_spacing))
    if screen_ID != Screens.trening.value:
        The_game_window.surface.blit(secreen_details[1], (table_left + 8 * column_width, 21.5 * The_game_window.menu_line_spacing))
    if screen_ID == Screens.teammanagementaway.value:
        The_game_window.surface.blit(secreen_details[2], (table_left , 23 * The_game_window.menu_line_spacing ))
    if  screen_ID == Screens.trening.value:
        The_game_window.surface.blit(secreen_details[3], (table_left + 2 * column_width, 21.5 * The_game_window.menu_line_spacing))
    ## Vykresleni tabulky
    # Rect(left, top, width, height)
    pygame.draw.rect(The_game_window.surface, RED, (table_left, table_top,  \
                                teams_on_page * column_width,text_ratio * lines * The_game_window.menu_line_spacing), 1)

    # line(surface, color, start_pos, end_pos, width)
    shift = 0
    for row_loop in range (0,lines):
        shift = shift + text_ratio * The_game_window.menu_line_spacing
        pygame.draw.lines(The_game_window.surface, GREY_LINES, True,((table_left ,table_top + shift ), \
                                                                        (table_right ,table_top + shift)), 1)

    shift = 0
    for row_loop in range (0,teams_on_page):
        shift = shift + column_width
        pygame.draw.lines(The_game_window.surface, GREY_LINES, True, ((table_left + shift, table_top), \
                                                                        (table_left + shift, table_bottom)), 1)

    # zvyrazneni oznaceneho slotu pro vyber , 0.99  0.98 jsou pomery tabulky abe se barvy neprekryvaly
    if coach.selected_slot_team_management[0] >= 0:
        pygame.draw.rect(The_game_window.surface, GREEN, (table_left + coach.selected_slot_team_management[0] * column_width, \
                                                          table_top + coach.selected_slot_team_management[1] * text_ratio * The_game_window.menu_line_spacing, \
                                                          column_width * 0.99, \
                                                          text_ratio  * The_game_window.menu_line_spacing * 0.99), 1)

    # team management screen slot kopiruje , training screen slot jen zvirazni
    if screen_ID == Screens.teammanagement.value:
        color_second_selection = RED
    else:
        color_second_selection = GREEN

    if coach.selected_slot_team_management_buffer[0] >= 0:
        pygame.draw.rect(The_game_window.surface, color_second_selection, \
                                    (table_left + coach.selected_slot_team_management_buffer[0] * column_width, \
                                     table_top + coach.selected_slot_team_management_buffer[1] * text_ratio * The_game_window.menu_line_spacing, \
                                     column_width * 0.98, \
                                     text_ratio  * The_game_window.menu_line_spacing * 0.98), 1)


    ## Vykresleni tabulky
    column_teams_shift = 0
    player_line_shift = 0
    leter_shift_from_boarder = 5 # odsazeni od hran tabulky
    font_diference = 1           # rozdil mezi fontem a linkou

    for teams_loop in range (0,10):

        # zvirazni team s neulozenou zmenou
        team_color = GREY
        if coach.loaded_teams_xml[teams_loop] != SavingType.empty_team_slot.value \
                and coach.loaded_teams_xml[teams_loop][0][1] != "original" :

            team_color = RED

        players_data =  coach.loaded_teams_xml[teams_loop]
        for players_loop in range (0,6):  # 1 nazev teamu +  5 hracu  => 6 radku
            if players_data != SavingType.empty_team_slot.value :

                # >1 players
                if players_loop >= 1:
                    for player_details in range (0,4):                       # !!!! PRIZPUSOBIT OPODLE POCTU DETAILS NA HRACE
                        # ID se nezobrazuje
                        if players_data[players_loop] != SavingType.empty_player_slot.value:
                            name_atring = players_data[players_loop][0]
                            space_index = name_atring.find(" ", 0, len(name_atring))
                            name = name_atring[0:space_index]
                            surname = name_atring[space_index:len(name_atring)]

                            if  player_details == 0:#name
                                data = MENU_FONT.render(name, 1, team_color)
                            elif player_details == 2:#player_type
                                data = MENU_FONT.render(surname, 1, team_color)
                            elif player_details == 3:#trening inputs
                                #data = MENU_FONT.render( players_data[players_loop][player_details], 1, team_color)
                                data = MENU_FONT.render(player_type_text(int(players_data[players_loop][2])), 1, team_color)

                            if player_details!=1:# id se nevykresli
                                The_game_window.surface.blit(data, \
                                            (table_left + column_teams_shift + leter_shift_from_boarder, table_top +  player_line_shift))
                                player_line_shift = player_line_shift + The_game_window.menu_line_spacing

                        # prazdny slot
                        else:
                            if player_details!=1:# id se nevykresli
                                player_line_shift = player_line_shift + The_game_window.menu_line_spacing


                # < 1 team
                else:
                    team_name = MENU_FONT.render("Team " + coach.loaded_teams_xml[teams_loop][0][0], 1, GREY)
                    The_game_window.surface.blit(team_name, \
                                            (table_left + column_teams_shift + leter_shift_from_boarder, table_top +  player_line_shift))

                    # vykresleni oznaceneho teamu se neprovede pri treningu
                    if screen_ID != Screens.trening.value:
                        if coach.loaded_teams_xml[teams_loop][0][2] == "selected":

                            draw_green_tick([table_left + int(0.2*column_width)+column_teams_shift + leter_shift_from_boarder, \
                                             table_top + int(2.5*The_game_window.menu_line_spacing )],The_game_window)

                    player_line_shift = player_line_shift +3* The_game_window.menu_line_spacing   # *3 team ma jen jmeno a musi se posunout 3 linie dolu

        column_teams_shift = column_teams_shift + column_width
        player_line_shift = 0

# print team management tlacitka
def f_print_teammngmt_buttons(The_game_window):
    counter = 0
    dims_taken = False
    button_location = [0,0]
    button_size = [0,0]
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.teammanagement.value:
            draw_button_No(The_game_window, loop)
            if dims_taken == False:
                dims_taken = True
                button_location  = [The_game_window.buttons[loop].x_corner , The_game_window.buttons[loop].y_corner]
                button_size = The_game_window.buttons[loop].size   # lenght, high

    counter = 5
    counter2 = 8

    pygame.draw.rect(The_game_window.surface, GREY_LINES, ( button_location[0], \
                                            button_location[1] -5, counter * button_size[0], 2 ),1)
    dot2 = pygame.draw.rect(The_game_window.surface, GREY_LINES, \
                                            (button_location[0] + button_size[0] /4, button_location[1]  - 10, 10, 5),3)            #PROC SE MENUJOU DOt??????  zkontroluj
    The_game_window.surface.fill(GREY_LINES,dot2)

    pygame.draw.rect(The_game_window.surface, GREY_LINES, \
                                            (button_location[0] + counter2 * button_size[0], \
                                            button_location[1] - 5, 2 * button_size[0] , 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES, \
                                            (button_location[0] + counter2 * button_size[0] + button_size[0] /4, \
                                            button_location[1]- 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)



# print team managementaway tlacitka
def f_print_teammngmtaway_buttons(The_game_window):
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.teammanagementaway.value:
            draw_button_No(The_game_window, loop)
            button_location  = [The_game_window.buttons[loop].x_corner, The_game_window.buttons[loop].y_corner]
            button_size = The_game_window.buttons[loop].size   # lenght, high

    counter = 1
    counter2 = 8
    pygame.draw.rect(The_game_window.surface, GREY_LINES, \
                                        (button_location[0] - counter2 * button_size[0], \
                                         button_location[1] - 5, 5 * button_size[0], 2 ),1)
    dot2 = pygame.draw.rect(The_game_window.surface, GREY_LINES, \
                                        (button_location[0] - counter2 * button_size[0] + button_size[0] /4, \
                                        button_location[1]  - 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot2)

    pygame.draw.rect(The_game_window.surface, GREY_LINES, \
                                        (button_location[0] ,  button_location[1] -5,  button_size[0], 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES, \
                                        (button_location[0] +  button_size[0] /4, button_location[1] - 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)


# print vyber teamu  pro hru tlacitka
def f_print_teams_for_game_buttons (The_game_window):
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.teamsconfirmation.value:
            draw_button_No(The_game_window, loop)

# tisk score, reff details pri hre                                                          #FFFFOOONNNNTTTNNNEWWWW
def f_print_score(score,The_game_window,The_field):
    show_score = get_font("WELCOME_FONT" ,The_game_window.window_height).render(str(score), 1, GREY)
    The_game_window.surface.blit(show_score,(The_field.field_bl_corner [0] + 0.92 * The_field.field_width / 3, \
                                             The_field.field_bl_corner[1] + The_game_window.menu_line_spacing))
    reff_header = MENU_FONT.render("Reff menu:", 1, GREY)
    The_game_window.surface.blit(reff_header,(The_field.field_bl_corner [0]  , \
                                              The_field.field_bl_corner[1] + The_game_window.menu_line_spacing ))

    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.ingame.value:
            draw_button_No(The_game_window, loop)

# print trening tlacitka
def f_print_trening_buttons(The_game_window):
    dims_taken = False
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.trening.value:
            draw_button_No(The_game_window, loop)
            if dims_taken == False:
                dims_taken = True
                button_location  = [The_game_window.buttons[loop].x_corner , The_game_window.buttons[loop].y_corner ]
                button_size = The_game_window.buttons[loop].size   # lenght, high
    counter = 1
    counter2 = 4

    pygame.draw.rect(The_game_window.surface, GREY_LINES, (button_location[0], button_location[1] -5, counter * button_size[0], 2 ),1)
    dot2 = pygame.draw.rect(The_game_window.surface, GREY_LINES, ( button_location[0] + button_size[0] /4,button_location[1]  - 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot2)

    pygame.draw.rect(The_game_window.surface, GREY_LINES, (button_location[0] + 2 * button_size[0] , \
                                                            button_location[1] -5, 5.5 * button_size[0] , 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES, (button_location[0] + 2 * button_size[0] + button_size[0] /4 , \
                                                                    button_location[1]- 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)




# trening manual
def f_print_treningman_buttons(The_game_window,lower_screen_ID):
    dims_taken = False
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.treningmanual.value:
            draw_button_No(The_game_window, loop)
            if dims_taken == False:

                dims_taken = True

                if lower_screen_ID == Screens.trainingautomated.value :
                    button_shift = 2
                elif  lower_screen_ID == Screens.trainingoffscreen.value :
                    button_shift = 1
                else:
                    button_shift = 0

                start_button_location  = [The_game_window.buttons[loop].x_corner , The_game_window.buttons[loop].y_corner ]
                selected_button_location = The_game_window.buttons[loop].x_corner + button_shift * 2 * The_game_window.buttons[loop].size[0] 
                button_size = The_game_window.buttons[loop].size   # lenght, high

    counter = 1
    pygame.draw.rect(The_game_window.surface, GREY_LINES, ( start_button_location[0]  , start_button_location[1] -5, 5.5 * button_size[0] , 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES, ( selected_button_location + button_size[0] /4 , start_button_location[1]- 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)


# print zobraz  menu button
def f_print_dysplay_menu_button(The_game_window):
    index = len(The_game_window.buttons)  -1
    draw_button_No(The_game_window,index)

# print edit hrace
def f_print_edit_player_buttons(The_game_window):
    counter = 0
    dims_taken = False
    button_location = [0,0]
    button_size = [0,0]
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.teammanagementedit.value:
            draw_button_No(The_game_window, loop)
            if dims_taken == False:
                dims_taken = True
                button_location  = [The_game_window.buttons[loop].x_corner , The_game_window.buttons[loop].y_corner ]
                button_size = The_game_window.buttons[loop].size   # lenght, high
            counter = counter + 1

    pygame.draw.rect(The_game_window.surface, GREY_LINES, ( button_location[0], button_location[1] -5, counter * button_size[0], 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES, (button_location[0] + (counter - 2) * button_size[0] + button_size[0] /4, \
                                                                button_location[1]  - 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)

# print create hrace
def f_print_create_player_buttons(The_game_window,coach_team_A):
    counter = counter2 = 0
    dims_taken =  False
    button_location = [0,0]
    button_size = button_size2 = [0,0]
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.teammanagementcreate.value:
            draw_button_No(The_game_window, loop)
            if dims_taken == False:
                dims_taken = True
                button_location  = [The_game_window.buttons[loop].x_corner , The_game_window.buttons[loop].y_corner ]
                button_size = The_game_window.buttons[loop].size   # lenght, high
            counter = counter + 1

    # cisla vstupu pro vtvoreni hrace
    for loop2 in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop2].number) == Screens.teammanagementcreateNo.value:
            draw_button_No(The_game_window, loop2)

    pygame.draw.rect(The_game_window.surface, GREY_LINES, ( button_location[0], button_location[1] -5,int(5* The_game_window.mngmt_column_width), 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES, \
                                        (button_location[0] + 4 * The_game_window.mngmt_column_width + The_game_window.mngmt_column_width /4 , \
                                         button_location[1]  - 10, 10, 5),3)

    The_game_window.surface.fill(GREY_LINES,dot)

    #sum vybranych skills
    skills_sums = coach_team_A.get_selected_createNos()
    skills_sums_rendered = MENU_FONT.render(str(skills_sums), 1, GREY)
    The_game_window.surface.blit( skills_sums_rendered ,(int(The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu  \
                                                                + 1.5 * The_game_window.mngmt_column_width), \
                                                                 25 * The_game_window.menu_line_spacing))

'''
#player je vstup ve tvaru [pl_name, pl_ID,pl_position,trening_type,trening_time]
def draw_edited_player_details (player,The_game_window):
    player_name = MENU_FONT.render(player[0], 1, GREY)
    The_game_window.surface.blit(player_name,(The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu , \
                                              The_game_window.game_menu_ y_end + The_game_window.menu_line_spacing ))



'''

def f_print_createPlr_details(The_game_window,trainig_code,is_player):
    shift_x = 0
    shift_y = 0
    text = f_create_player_text(The_game_window.language)
    #print (trainig_code)
    for text_loop in range (0,len(text)):
        a = trainig_code[text_loop]
        color_print = GREEN if (a == True or a == 'True') else RED

        skill_detail = CREATENO_FONT.render(text[text_loop], 1, GREY)
        pygame.draw.circle(The_game_window.surface, color_print, (The_game_window.mngmt_shift_from_menu  + shift_x - 5 , \
                                                                  The_game_window.game_menu_y_end + int(0.5* The_game_window.menu_line_spacing) \
                                                                  + The_game_window.menu_line_spacing * shift_y), 2, 2)

        The_game_window.surface.blit(skill_detail,(The_game_window.mngmt_shift_from_menu  + shift_x, \
                                                   The_game_window.game_menu_y_end + The_game_window.menu_line_spacing * shift_y))

        shift_y = shift_y + 1
        if text_loop == 6 or text_loop == 12 :
            shift_x = shift_x + 3*The_game_window.mngmt_column_width
            shift_y = 0

# print hodnoty z treningu - pocet uskutecnenych  a planovanych 'runs'
def f_print_trening_progress(The_game_window,The_field,coach_team_A,coach_team_B):

    if coach_team_A.active_trening == True:
        trening_progress = len (coach_team_A.data_labels)
        max_trening_progress = coach_team_A.trening_sesion_total_runs
    else:
        trening_progress = len (coach_team_B.data_labels)
        max_trening_progress = coach_team_B.trening_sesion_total_runs

    show_trening_progress = MENU_FONT.render(str(max_trening_progress), 1, GREY)
    The_game_window.surface.blit(show_trening_progress,(The_field.field_bl_corner [0], \
                                 The_field.field_bl_corner[1] + The_game_window.menu_line_spacing ))

    show_max_trening_progress = MENU_FONT.render(str(trening_progress), 1, GREY)
    The_game_window.surface.blit(show_max_trening_progress,(The_field.field_bl_corner [0], \
                                 The_field.field_bl_corner[1] + 2 * The_game_window.menu_line_spacing ))



def f_print_player_details_off_game(screen_ID,The_reff,The_game_window):

    coach = The_reff.coach_team_B if screen_ID == Screens.teammanagementaway.value else  The_reff.coach_team_A

    if  coach.selected_slot_team_management[1] > 0 :
        team = coach.selected_slot_team_management[0]
        player = coach.selected_slot_team_management[1]
        if coach.loaded_teams_xml[team] !=  SavingType.empty_team_slot.value and \
             coach.loaded_teams_xml[team][player] != SavingType.empty_player_slot.value:

            player = coach.loaded_teams_xml[team][player]
            shift_vertikal = The_game_window.game_menu_y_end
            shift_horisontal = 6 * The_game_window.mngmt_column_width                                                                                               #nejak lip definovat  hodnotu
            list_of_tags =[ "pl_name: ", "pl_ID: ","type: ","skills: ","trening_time: "]

            for data_index in range (0,5):
                data = CREATENO_FONT.render(  list_of_tags[data_index] + player[data_index], 1, GREY)
                The_game_window.surface.blit(data,( shift_horisontal, shift_vertikal ))
                shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing

            # tisk skils set
            f_print_createPlr_details(The_game_window,player[5],True)

# tisk detailu hrace pri hre
def f_print_player_details(The_game_window,The_field,player,list_of_ingamers):
    shift_vertikal = 0
    shift_horisontal = 300                                                                                              #nejak lip definovat  hodnotu
    list_of_tags = ["angle: ","ball angle: ","ball distance(cntr-cntr)","velocity: ","site,team: ","sumskils: ","name: "]
    list_of_data =[str(round(player.path_target)), \
                   str(round(player.calculate_angle_to_other_object(list_of_ingamers[1].rect.center))), \
                   str(round(pythagoras_distance (player.rect.center,list_of_ingamers[1].rect.center))), \
                   str(player.velocity), \
                   player.field_site +" , "+ player.team , \
                   str(player.skills_level), \
                   player.name ]

    for data_index in range (0,len(list_of_data)):
        data = MENU_FONT.render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, GREY)
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0] +200+ shift_horisontal, \
                                            The_game_window.game_menu_y_end  + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing

    list_of_tags2 = ["position: ",  "ID: ","sector: ","posix: " ,"posiy: " ,"feidx :","feidy :"]
    list_of_data2 =[player_type_text(int(player.player_type)) , \
                   player.ID, \
                   str(calculate_sector(1,player.field_site,player.rect.center,[ The_field.field_width,The_field.field_height], The_field.field_bl_corner)), \
                   str(player.rect.center[0]), \
                   str(player.rect.center[1]), \
                   str(The_field.field_width), \
                    str(The_field.field_height)]
    #print(str(calculate_sector(player.position,[ The_field.field_width,The_field.field_height])))
    #print(The_field.field_width,The_field.field_height)
    shift_vertikal = 0
    for data_index in range (0,len(list_of_data2)):
        data = MENU_FONT.render(  list_of_tags2[data_index] + list_of_data2[data_index]   , 1, GREY)
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0] + 3*shift_horisontal  , \
                                            The_game_window.game_menu_y_end  + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing




'''
#test prints                                                                                            #testy souradnic
def print_test_x(The_game_window):
    xx = MENU_FONT.render( "XX"  , 1, red)
    The_game_window.surface.blit(xx,(300, 650 ))
    #print("xx")
'''


# vizualizace keras.modelu                                                                                          # pouzita pri testovani asi nebude v hre uzita
def f_print_model_live(The_game_window,The_field,player,list_of_ingamers,live_data,model_values):
    data = [0,0,0,0]
    data = calculate_live_model(live_data,model_values)
    data.append([ "otoc","-otoc","krok","kop" ,"nic" ])
    x_shift = 300
    shift_vertikal = 0

    for list_index in range (0,len(data)):
        for inner_list_index in range (0,len(data[list_index])):
            if list_index < len(data)-1:
                data_print = MENU_FONT.render(  str(round(data[list_index][inner_list_index],4)  ) , 1, GREY)
            else:
                data_print = MENU_FONT.render(  data[list_index][inner_list_index] , 1, GREY)
            The_game_window.surface.blit(data_print,(The_field.field_bl_corner [0] + x_shift, \
                                                    The_field.field_bl_corner[1] + The_game_window.menu_line_spacing + shift_vertikal ))
            shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing

        x_shift = x_shift + 100
        shift_vertikal = 0


# tisk nastaveni/hodnot balonu (uzito pro kontrolu metod )                                                                        # pouzita pri testovani asi nebude v hre uzita
def f_print_ball_details(The_game_window,The_field,ball,list_of_ingamers):
    shift_vertikal = 0
    list_of_tags = ["angle: ","owner: ","velocty: ","site: "]
    list_of_data =[str(round(ball.path_target)), \
                   str(ball.owner), \
                   str(ball.velocity), \
                   str(ball.field_site) ]


    for data_index in range (0,len(list_of_data)):
        data = MENU_FONT.render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, GREY)
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0], The_field.field_bl_corner[1] + The_game_window.menu_line_spacing + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing


# tisk uvitaci plochy
def draw_weclome(The_game_window):
    if The_game_window.language == "CZ":
        welcome = WELCOME_FONT.render('Flatball vitejte', 1, GREY)
    else:
        welcome = WELCOME_FONT.render('Flatball welcome', 1, GREY)

    The_game_window.surface.blit(welcome,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))

def draw_trening_off_screen(The_game_window):
    if The_game_window.language == "CZ":
        welcome = WELCOME_FONT.render('trening', 1, GREY)
    else:
        welcome = WELCOME_FONT.render('trening', 1, GREY)

    The_game_window.surface.blit(welcome,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))


# tisk uvitaci plochy
def draw_teams_selection_error(The_game_window):
    if The_game_window.language == "CZ":
        error = WELCOME_FONT.render('Zkontrolujte vybrane teamy, flatball se hraje v 2 !', 1, GREY)
    else:
        error = WELCOME_FONT.render('Required 2 teams for the game!', 1, GREY)

    The_game_window.surface.blit(error,(The_game_window.game_menu_x_end +10 , The_game_window.window_height * 0.3))


# error  screen
def draw_error(The_game_window):
    if The_game_window.language == "CZ":
        error = WELCOME_FONT.render('Ooo error, neco je spatne ', 1, GREY)
    else:
        error = WELCOME_FONT.render('Ooo error, something is wrong', 1, GREY)

    The_game_window.surface.blit(error,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))

# tisk paused game
def draw_paused_game(The_game_window):
    if The_game_window.language == "CZ":
        paused = WELCOME_FONT.render('Hra pozastavena', 1, GREY)
    else:
        paused = WELCOME_FONT.render('Game paused', 1, GREY)

    The_game_window.surface.blit(paused,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))


# pomocna funkce, pythagorovo pravidlo
def pythagoras_distance (location_1,location_2):                                                                            #stejna funkce v 2 modulech Zkontroluj
    ingamer_adjescent =  abs (location_1[0]  -  location_2[0])
    ingamer_opposite =  abs (location_1[1] -  location_2[1])
    ingamer_hypotensue = sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

    return ingamer_hypotensue

# napoveda


def f_print_help_trening(The_game_window):
    text =  f_help_trening_text(The_game_window.language)
    The_game_window.surface.blit(text,(The_game_window.game_menu_x_end, The_game_window.menu_line_spacing))


def f_print_RE_trening_inprogress(The_game_window):
    text =  f_RE_trening_inprogress_text(The_game_window.language)
    The_game_window.surface.blit(text,(The_game_window.game_menu_x_end, 20 * The_game_window.menu_line_spacing))


def f_print_RE_trening_done(The_game_window):
    text =  f_RE_trening_done_text(The_game_window.language)
    The_game_window.surface.blit(text,(The_game_window.game_menu_x_end, 30 * The_game_window.menu_line_spacing))

def f_print_RE_trening_started(The_game_window):
    text =  f_RE_trening_started_text(The_game_window.language)
    The_game_window.surface.blit(text,(The_game_window.game_menu_x_end, 30 * The_game_window.menu_line_spacing))

def f_print_help(The_game_window):
    helpText="none"
    if The_game_window.language == "CZ":
        help_heading = MENU_FONT_HEADING.render('NAPOVEDA', 1, GREY)
    else:
        help_heading = MENU_FONT_HEADING.render('GAME GUIDE', 1, GREY)
    The_game_window.surface.blit(help_heading, (The_game_window.window_width * 0.4 , 0.5 * The_game_window.menu_line_spacing))

    helpText = f_help_text(The_game_window.language)                                                                                                                    #end line

    for loop_help_print in range (0,len(helpText)):
        help_line = helpText[loop_help_print]
        help_line_rendered = MENU_FONT.render( help_line, 1, GREY)
        The_game_window.surface.blit(help_line_rendered,( The_game_window.game_menu_x_start + 50, \
                                                        1 * The_game_window.menu_line_spacing + loop_help_print * The_game_window.menu_line_spacing ))
'''
# icona pro zobrazeni menu
def draw_menu_icon(The_game_window):
    for loop_menu_icon in range (1,4):
        icon_line_rendered = WELCOME_FONT.render( "-", 1, GREY)
        The_game_window.surface.blit(icon_line_rendered,( The_game_window.game_menu_x_start , -15 + 6 * loop_menu_icon   ))
'''


def print_check_pin(The_game_window):
    helpText="none"
    if The_game_window.language == "CZ":
        check_pin_text = MENU_FONT.render('check_pin , info_message', 1, GREY)
    else:
        check_pin_text = MENU_FONT.render('check_pin', 1, GREY)

    The_game_window.surface.blit(check_pin_text,( The_game_window.game_menu_x_start , 21 * The_game_window.menu_line_spacing ))



#
#-------------------------------------------------------texty--------------------------------------------------------------

def f_stats_text (language):
    text = [0,0]
    if language == "CZ":
        text[0] = MENU_FONT_HEADING.render('stats vitejte', 1, GREY)
        text[1] = ["team","trenovano" ,"trening" ,"prum skills" , "zapasu", "vyher", "vybrano","trenovano" ,"trening" ,"prum skills" , "zapasu", "vyher", "vybrano"]
    else:
        text[0] = MENU_FONT_HEADING.render('stats teams for game', 1, GREY)
        text[1] =["team","trenovano" ,"trening" ,"prum skills" , "zapasu", "vyher", "vybrano","trenovano" ,"trening" ,"prum skills" , "zapasu", "vyher", "vybrano"]
    return text

def f_teams_for_game_headings_text (language):
    if language == "CZ":
        text = [" "," " ,"note_b" ,"note_c" , "note_d", "note_e", "selected","note_a" ,"note_b" ,"note_c" , "note_d", "note_e", "selected"]
    else:
        text = [" "," " ,"note_b" ,"note_c" , "note_d", "note_e", "selected","note_a" ,"note_b" ,"note_c" , "note_d", "note_e", "selected"]
    return text

def teammanagmnt_text_heading (language,screen_ID):
    screen_headeing = "none"
    if language == "CZ":
        if screen_ID == Screens.teammanagement.value:
            screen_headeing = MENU_FONT_HEADING.render('Team management', 1, GREY)
        elif screen_ID == Screens.trening.value:
            screen_headeing = MENU_FONT_HEADING.render('Team trening', 1, GREY)
        elif screen_ID == Screens.teammanagementaway.value:
            screen_headeing = MENU_FONT_HEADING.render('Team managementaway', 1, GREY)
    else:
        if screen_ID == Screens.teammanagement.value:
            screen_headeing = MENU_FONT_HEADING.render('Team management', 1, GREY)
        elif screen_ID == Screens.trening.value:
            screen_headeing = MENU_FONT_HEADING.render('Team training', 1, GREY)
        elif screen_ID == Screens.teammanagementaway.value:
            screen_headeing = MENU_FONT_HEADING.render('Team managementaway', 1, GREY)

    return  screen_headeing



def teammanagmnt_text_buttons (language,screen_ID):
    text = [ "none" ,  "none",  "none" ,  "none"  ]
    if language == "CZ":
        if True :                                                      # screen_ID == Screens.teammanagement.value:
            text[0] = MENU_FONT.render(' HRAC', 1, GREY)
            text[1] = MENU_FONT.render(' team ', 1, GREY)
            text[2] = MENU_FONT.render('Souperovy hraci zmnena nepovolena', 1, GREY)
            text[3] = MENU_FONT.render(' trening ', 1, GREY)
    else:
        if True :                                                        #screen_ID == Screens.teammanagement.value:
            text[0] = MENU_FONT.render('Player', 1, GREY)
            text[1] = MENU_FONT.render('team ', 1, GREY)
            text[2] = MENU_FONT.render('Opponets team update not allowed ', 1, GREY)
            text[3] = MENU_FONT.render(' trening ', 1, GREY)
    return  text



def f_help_text(language):
    if language == "CZ":
        helpText =[' ', \
                    'TRENER   ', \
                    ' -Team management: hra ma ulozen jeden vytvoreny team hrac můze byt kopirovan do noveho teamu, jakmile je 5 hracu v teamu zmena musi  ', \
                    '   byt ulozena a to oznacenim jmena teamu a tlacitkem ulozit zmeny, v pripade kopirovani hrace do prazdneho  teamu se novy team vytvori automaticky', \
                    ' -Stats: staistika hracu a teamu ', \
                    ' -Trening: trenovany hrac je oznacen a potvrzen  (team A), pote musi byt oznacen tym proti kteremu se bude trenovat ( team B ), prozatim jen', \
                    '   manualni trening je funkcni ( H / H) prave tlacitko mysi vytvori nove rozestaveni pro trening , klavesa -p- ukonci trening', \
                    '   trening ma vliv na hrace pouze po dostazeni 5000 akci, kdy je trening vyhodnocen pote se muze v treningu pokracovat pocet akci', \
                    '   je vyobrazen pod hrsitem  kotrola hrace pri hre je vysvetlena nize', \
                    '   ' , \
                    'ROZHODCI  ', \
                    ' -Delka utkani  ', \
                    ' -Potvrzeni teamu do hry: teamy jsou vytvoreny v  -team management- mohou byt vybrany do zapasu, cervene oznacene teamy nejsou uplne ', \
                    '   rozhodci je bude ignorovat ,oznaceny hrac je  ovladan  mysi ta urcuje smer a klavesa -w-  je krok,mezernikem je proveden kop do mice  ', \
                    ' -Nastaveni hriste  ', \
                    ' -Zpet na zapas   ', \
                    'NASTAVENI  ', \
                    ' -lokalize  ', \
                    ' -velikost okna aplikace  ', \
                    'LAB MODE  ', \
                    ' -zapnout lab mode  ', \
                    ' -vypnout grafikku  ', \
                    'NAPOVDEA  ']

    else:
        helpText =['FLATBALL', \
                    '  ', \
                    '  ', \
                    'TEAM MANAGEMENT', \
                    '  default created one non trained team ,user can copy players to new slots or later to created teams ' \
                    '  change has to be saved, save can be done if selected team and team has 5 players' , \
                    '  user needs cleck on player .use copy button than select new slot and select paste button ', \
                    '  new team is automaticaly generated if player is paste to non team slot' , \
                    '  ', \
                    'Training ', \
                    '  user has to select a player (his team is team A) ' , \
                    '  than need select team (will be team B for the training match)' , \
                    '  it is posible to select own team as opossite team (should be working fine ) ' ,
                    '  for now only non automised training is available ( H / H)' ,
                    '  left mouse selection will create new match situation , key -p- will end training  ' , \
                    '  training will affect a player if 5000 runs is hit than training can continue or be end' , \
                    '  for player control guide see part -match- below ' , \
                    '  ', \
                    'Teams confirmation for game  ', \
                    '  teams created and saved in -team management- are available for game selection   ', \
                    '  if teams is displayed red than team update  was not saved or doesnt have 5 players      ', \
                    '  MATCH  for now is available only at mod human vs AI ', \
                    '  AI players are non selectable , team of user is controled by AI but one of the player can be selected ' , \
                    '  selected player can be controlled by user: mouse gives direction of move, -w- key makes a step ,-space- kicks a ball if owned ' , \
                    '   ', \
                    '  ', \
                    '  ']

    return helpText


def teams_names (index):
    team = "null"
    list=["team1", "t2", "t3",  "t4" ,"t54", "ta" ,"tr", "tw" ,"uyy" , \
         "t74t" ,"t58t" ,"t4" ,"t75t" ,"tpt" ,"ttd" ,"dt" ]

    if index >=0 and index < len(list):
        team =  list[index]

    return team

def players_names (index):
    player_name = "null"
    list=["Max Aarons","Rolando Aarons","Tammy Abraham","Che Adams","Adrián Mcdowel","Adrián Bernabé","Adrien Silva","Dan Adshead", \
        "Nathan Aké","Marc Albrighton","Toby Alderweireld","Aleix García","Trent Alexander-Arnold","Albian Ajeti","Pierre Aubameyang", \
        "Alisson Lee","Tom Allan","Dele Alli","Miguel Almirón","Steven Alzate","Daniel Amartey","Ethan Ampadu","Joseph Anang", \
        "André Gomes","Andreas Pereira","Michail Antonio","Stuart Armstrong","Arnau Puigmal","Daniel Arzani","Christian Atsu", \
        "Serge Aurier","Jordan Ayew","Ayoze Pérez","Abdul Rahman Baba","Daniel Bachmann","Eric Bailly","Leighton Baines", \
        "Fabián Balbuena","George Baldock","Folarin Balogun","Tudor Băluţă","Beni Baningime","Phil Bardsley","Ross Barkley","Ashley Barnes", \
        "Harvey Barnes","Chris Basham","Lewis Bate","Michy Batshuayi","Jack Bearne","Jan Bednarek","Ryan Bennett","Josh Benson", \
        "Nabil Bentaleb","Christian Benteke","Sander Berge","Steven Bergwijn","Bernardo Rosa","Bernardo Silva","Ryan Bertrand", \
        "Muhamed Bešić","Philip Billing","Yves Bissouma","Tolaji Bola","Yannick Bolasie","Willy Boly","Artur Boruc","Sofiane Boufal", \
        "Jarrod Bowen","Morgan Boyes","Robbie Brady","Jarrad Branthwaite","Claudio Bravo","Armando Broja","David Brooks","Josh Brownhill", \
        "Bruno Fernandes","Bruno Jordão","Emiliano Buendia","Dan Burn","Matt Butcher","David Button","Oskar Buur","Sam Byram", \
        "Willy Caballero","Gary Cahill","Jake Cain","Dominic Lewin","Leonardo Campana","Todd Cantwell","Étienne Capoue", \
        "Guido Carrillo","Andy Carroll","Scott Carson","Lewis Cass"]

    if index >=0 and index < len(list):
        player_name =  list[index]

    return player_name


def f_help_trening_text(language):
    text = "null"
    if language == "CZ":
        text = MENU_FONT.render(' space kick , w  step, e no action,p end trening ,mys pravy  plrs nova pozice', 1, GREY)
    else:
        text = MENU_FONT.render('ukukukspace kick  w  step e no action:D p end trening mys pravy  plrs nova pozice', 1, GREY)

    return  text


def f_RE_trening_inprogress_text(language):
    text = "null"
    if language == "CZ":
        text = MENU_FONT.render(' trening_inprogress ted probiha', 1, GREY)
    else:
        text = MENU_FONT.render('trening_inprogress', 1, GREY)

    return  text


def f_RE_trening_done_text(language):
    text = "null"
    if language == "CZ":
        text = MENU_FONT.render(' trening_inprogress hotovo', 1, GREY)
    else:
        text = MENU_FONT.render('trening_done', 1, GREY)

    return  text

def f_RE_trening_started_text(language):
    text = "null"
    if language == "CZ":
        text = MENU_FONT.render(' trening_inprogress hstarted', 1, GREY)
    else:
        text = MENU_FONT.render('trening_started', 1, GREY)

    return  text

def f_create_player_text(language):
    text = [0,0,0,0,0,0,0]
    if language == "CZ":
        text =["1 angle to own goal" , \
             "2 angle to ball", \
             "3 distance to ball", \
             "4 player type (GK,striker,etc)", \
             "5 qvadrant sektory 3 & 3=> 9 ", \
             "6 je z teamu nejblize mici", \
             "7 tactic", \
             "8 strategy", \
             "9 message", \
             "10 team je u balonu ball", \
             "11 je v view nejaky hrac ?", \
             "12 game status", \
             "13 game type"]
    else:
        text =["1 angle to own goal" , \
             "2 angle to ball", \
             "3 distance to ball", \
             "4 player type (GK,striker,etc)", \
             "5 qvadrant (zatim  3 & 3) 9 ", \
             "6 je z teamu nejblize mici", \
             "7 tactic", \
             "8 strategy", \
             "9 message", \
             "10 team je u balonu ball", \
             "11 je v view nejaky hrac ?nastav vzdalenost?", \
             "12 game status", \
             "13 game type"]

    return  text
