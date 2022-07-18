
import support_functions
from support_functions import *


def player_trening_info_log(player,action,run_to_save):
    print("cooridnates ",player.rect.center," path_target " ,player.path_target ," action ",action ," run_to_save " ,run_to_save)


def player_toBall_info_log(player,The_ball):
    distanceToBall = pythagoras_distance(player.rect.center, The_ball.rect.center) - player.radius - The_ball.radius
    print("distanceToBall ",distanceToBall  )
