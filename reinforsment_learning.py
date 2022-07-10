import tensorflow as tf
import numpy as np

from  tensorflow.keras import Sequential
from  tensorflow.keras.layers import Dense
from  tensorflow.keras.models import load_model
from  tensorflow.keras.optimizers import Adam
from gym import Env
from gym.spaces import Discrete, Box


#-from tf_agents.networks import q_network
#-from tf_agents.agents.dqn import dqn_agent

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

import time

import neural_network
from neural_network import *

import copy
import pygame

import support_functions
from support_functions import *

import screens
from screens import *

pygame.init()
from pygame.locals import *

##  ------DQN -----
##  soucet rewards za akci kterou provedeme

GREY = (192,192,192)
MENU_FONT = pygame.font.SysFont("Arial", 18)

def f_print_RE_trening_repetition_sequence(The_game_window, trening_repetition_sequence):
    text_progress =  f_RE_trening_repetition_sequence()
    The_game_window.surface.blit(text_progress,(The_game_window.game_menu_x_end + 80 + 10 *trening_repetition_sequence, 2 * The_game_window.menu_line_spacing))
    text_labels = f_RE_trening_repetition_sequence_percentage(The_game_window.language)
    The_game_window.surface.blit(text_labels,(The_game_window.game_menu_x_end ,  The_game_window.menu_line_spacing))

def f_RE_trening_repetition_sequence():
    text = "null"
    text = MENU_FONT.render('I', 1, GREY)
    return  text

def f_RE_trening_repetition_sequence_percentage(language):
    text = "null"
    if language == "CZ":
        text = MENU_FONT.render('trenovano 0%         100%    OBRAZOVKA UZAMKNUTA', 1, GREY)
    else:
        text = MENU_FONT.render(' traned   0%         100%    SCREEN LOCKED', 1, GREY)
    return  text


#---------------------  DQN KERAS AGENTS, Gym environment  ----

class TrainingEnvironment (Env):

    def __init__(self ):
        self.action_space = Discrete(5)
        self.observation_space = Box(low = np.array([-0.1,-0.1 ,-0.1   ,1,4,5,6,7,8,9,1,1,11]), \
                                      high= np.array([0.36,0.36,5,5,4,5,6,7,8,9,1,1,11]))
        self.state = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.episode_ended = False
        self.The_field = None
        self.list_of_ingamers=None
        self.trained_player=None
        self.do_render = False


    def load_data (self, list_of_ingamers, trained_player, The_field,The_game_window,The_reff, render):
        self.The_field = The_field
        self.list_of_ingamers= list_of_ingamers
        self.trained_player= trained_player
        self.The_game_window= The_game_window
        self.The_reff = The_reff
        self.do_render = render
        self.state = np.array( trained_player.get_NN_data(The_field,list_of_ingamers))

    def Xstep(self,action):
        info = {}
        return self.state, 2, False, info

    # action number from 0 to 4
    def step(self,action):
        ball_index = 0
        done = False
        list_of_ingamers = self.list_of_ingamers
        trained_player = self.trained_player
        The_field = self.The_field

        turn_angle = 22

        state_previouse = copy.deepcopy(self.state)

        # oprava pro uhly kdyz presahnou 360   /    0
        if action == 0:
            if (trained_player.path_target + turn_angle) >= 360:                                    #  opakovany kod jak u class hrace
                uhel = (trained_player.path_target + turn_angle) - 360
            else:
                 uhel =   (trained_player.path_target + turn_angle)
            trained_player.set_path_target(uhel)
        elif action == 1:
            if (trained_player.path_target - turn_angle) <= 0:
                uhel = (trained_player.path_target - turn_angle) + 359
            else:
                uhel = (trained_player.path_target - turn_angle)
            trained_player.set_path_target(uhel)
        elif action == 2:
            trained_player.move(The_field,list_of_ingamers)
        elif action == 3 and list_of_ingamers[ball_index].owner == trained_player:
            list_of_ingamers[ball_index].speed = 200   #testovaci kop
        else:
            pass

        #-aktualizace stavu
        self.state = np.array( trained_player.get_NN_data(self.The_field,self.list_of_ingamers))

        ##-- Vyhodnoceni
        #-neni brankar
        if self.state[3] != PlayerType.GK.value:
            # priblizuje se mici
            if self.state[2] < state_previouse[2]:
                reward = 2
                if list_of_ingamers[0].owner == trained_player:
                    if  trained_player.path_target > 120 and  trained_player.path_target < 240:
                        reward = 10
                        done = True
            else:
                # uhel k mici je skoro i uhel hrace
                if self.state[1] > trained_player.path_target -20  and self.state[1] < trained_player.path_target +20:
                    reward = 1
                else:
                    reward = -1


        info = {}

        if self.do_render == True:
            self.render()
            time.sleep(.01)

        return self.state, reward, done, info

    def render(self):

        #-print(  "-------------------------------------render  ")
        self.The_game_window.surface.fill(BLACK)

        self.list_of_ingamers[0].moving(self.The_field,self.The_reff)                                             # zastavi se pri paused game????
        #f_print_RE_trening_inprogress(self.The_game_window)
        draw_5aside_field (self.The_game_window,self.The_field,44)  # ENUM trainingautomated = 44
        for no_of_ingamers in range (0,len(self.list_of_ingamers)):
            self.list_of_ingamers[no_of_ingamers].draw_ingamer(self.The_game_window)


        f_print_RE_trening_repetition_sequence(self.The_game_window, self.The_reff.coach_team_A.trening_repetition_sequence)

        pygame.display.flip()

    def reset(self):                                                                           #jak gol reff resetovat hru movehrace pro novy game
        self.The_reff.coach_team_A.move_players_for_new_training_run (self.The_field,self.The_reff.list_of_ingamers)
        self.state = np.array( self.trained_player.get_NN_data(self.The_field,self.list_of_ingamers))
        return  self.state


def build_agent_keras (model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit = 500, window_length = 1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,  \
                    nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2,batch_size=1)
    return dqn


def run_RE_trening(model, actions, env,player_ID,trening_runs):

    dqnAgent_created = build_agent_keras (model, actions)
    dqnAgent_created.compile(Adam(learning_rate=1e-3) , metrics=['mae'])

    dqnAgent_created.fit(env, nb_steps=trening_runs, visualize=False, verbose=1 )

    path = get_path_home_folder()
    model.save(path +  str(player_ID)  + ".h5")



#---------------------  DQN TF AGENTS  ----
def build_TF_DQNagent():
    q_net = q_network.QNetwork(
      train_env.observation_spec(),
      train_env.action_spec(),
      fc_layer_params=(100,))

    agent = dqn_agent.DqnAgent(
      train_env.time_step_spec(),
      train_env.action_spec(),
      q_network=q_net,
      optimizer=optimizer,
      td_errors_loss_fn=common.element_wise_squared_loss,
      train_step_counter=tf.Variable(0))

    agent.initialize()

    return agent

'''

def run_RE_trening_tf():
    q_net = q_network.QNetwork(train_env.observation_spec(), train_env.action_spec(), fc_layer_params=(100,))
    agent = dqn_agent.DqnAgent(train_env.time_step_spec(),train_env.action_spec(),q_network=q_net, \
                               optimizer=optimizer,td_errors_loss_fn=common.element_wise_squared_loss, \
                                train_step_counter=tf.Variable(0))


    return agent


'''


#---------------------  nasledujici funkce jsou pouze pro testy a kontrolu keras modelu  ----


'''
JEEEEDEEEEEE

def testmodel(new_shape):
    model = tf.keras.Sequential([
        #tf.keras.layers.Flatten(input_shape=(1,13)),
        #tf.keras.layers.Input(shape=(13, )),
        tf.keras.layers.Flatten(input_shape=(1,13)),
        tf.keras.layers.Dense(5,activation="relu"),
        tf.keras.layers.Dense(5,activation="softmax")
        ])

    model.compile(optimizer="adam",loss='sparse_categorical_crossentropy',metrics=["accuracy"])

    return model





xxx=  [[   [[0,1,2,5,4,5,6,7,8,9,1,1,11]],[[0,1,2,5,4,5,6,7,8,9,1,1,11]]  ]]
print(  "shap-", np.shape(xxx))
xmodel = testmodel(13)
print(  "2---model.summary -", xmodel.summary())
xmodel.fit( xxx   ,    [[1,0]] )
print(" predikt "  , xmodel.predict(    [[[[0,1,2,5,4,5,6,7,8,9,1,1,11]]]]     ))

The_RE_env =TrainingEnvironment()
print(  "2---observation_space -")

ymodel = testmodel(13)
print(  "2---model.summary -", ymodel.summary())

dqnAgent_created = build_agent_keras (ymodel, 5)
dqnAgent_created.compile(Adam(learning_rate=1e-3) , metrics=['mae'])
dqnAgent_created.fit(The_RE_env, nb_steps=10, visualize=False, verbose=1 )

'''
