from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
import os.path                                  #oprait import
from os import path
import neural_network
from neural_network import *
from random import randint
import copy
import screens
from screens import *


def create_new_default_player(ID,position):
    #                ukazkovy hrac [pl_name, pl_ID,pl_position(type),skills_level,trening_time,skills_set]]
    player = [players_names (randint( 0,96 )), ID, position, "13", "0", create_new_skills_set(13)]
    return player

# ukazkovy team, ulozen pri prvnim spusteni hry
# input ma tvar : [team_name,5x [ukazkovy hrac]]
def create_new_default_team():
    team =[["Default","original","notselected"],create_new_default_player("1","1"), \
                                                create_new_default_player("2","2"), \
                                                create_new_default_player("3","3"), \
                                                create_new_default_player("4","4"), \
                                                create_new_default_player("5","5")]
    return team

def create_new_skills_set(loop_no):
    list  = []
    for loop in range (0,loop_no):
        list.append(True)
    return list

# vytvori xml file z dat teamu/hrace
def create_xml_file(team_data):
    # input ma tvar : [[team_name,team_detail_1,team_detail_2],5x player]

    root = Element("team")
    tree = ElementTree(root)

    team_name = Element("team_name")
    root.append(team_name)
    team_name.text = team_data[0][0]
                                                                                # pridat data pro statistiku?asi na konec
    # 1 protoze vstup ma prvni clen jmeno teamu
    for loop in range (1,len(team_data)):
        root2 = Element("player")
        tree2 = ElementTree(root2)
        root.append(root2)
                                                                                # pak pridat osobnost hrace
        plr_name = Element("plr_name")
        player_ID = Element("player_ID")
        player_type = Element("player_position")
        trening_type = Element("skills_level")
        trening_time = Element("trening_time")
        skills_set = Element("skills_set")

        root2.append(plr_name)
        plr_name.text = team_data[loop][0]
        root2.append(player_ID)
        player_ID.text = team_data[loop][1]
        root2.append(player_type)
        player_type.text= team_data[loop][2]
        root2.append(trening_type)
        trening_type.text= team_data[loop][3]
        root2.append(trening_time)
        trening_time.text= team_data[loop][4]
        root2.append(skills_set)
        skills_set.text= str(team_data[loop][5])

    tree.write(open( get_path_home_folder() + team_data[0][0] + '.xml','wb'))

# funkce vrati list hodnot ctenych z xml pro team
# vystup: [[team_name,team_detail_1,team_detail_2],5x player]
def f_read_from_xml(file):
    player_No = 1
    team_details = [ ["team_details","original","notselected"],"pl1","pl2","pl3","pl4","pl5"]
    mytree = etree.parse(file)
    myroot = mytree.getroot()
    team_details[0][0] = myroot[0].text
    for player in myroot.findall('player'):
        team_details[player_No] = [player.find('plr_name').text, \
                                 player.find('player_ID').text, \
                                 player.find('player_position').text, \
                                 player.find('skills_level').text, \
                                 player.find('trening_time').text , \
                                 player.find('skills_set').text]
        team_details[player_No][5] = eval( team_details[player_No][5] )

        player_No =  player_No + 1

    return team_details

# zkontroluje teams folder a popripade jej vytvori
# pri prvnim spusteni vytvori default hodnoty pro Tensorflow model
def f_teams_folders_check():
    main_folder = abspath(getcwd())
                                                                                #rozdel na dve funkce volane az pozdeji nacist data , vykresli data!!!!!!
    if path.exists("Teams"):
        pass
    else:
        os.mkdir("Teams")
        os.chdir("Teams")
        os.mkdir("Home")
        os.mkdir("Away")
        os.mkdir("Archive")

        default_team = create_new_default_team()

        os.chdir(main_folder)
        create_xml_file (default_team)

        # defaults models
        for players_loop in range (1,len(default_team)):           #zacina 1, prvni prvek je jmeno teamu
            model_inputs = int(default_team[players_loop][3])
            #print("model_inputssss", model_inputs)
            model = create_model_tf2( model_inputs  )                                                                                     # nebude konstanta
            model.save(get_path_home_folder() + default_team[players_loop][1]  + ".h5")

#
#f_read_from_xml("TEST_parsing.xml")
