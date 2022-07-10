from os.path import abspath
from os import getcwd

import tensorflow as tf

from  tensorflow.keras import Sequential
from  tensorflow.keras.layers import Dense
from  tensorflow.keras.models import load_model
import numpy as np
from numpy import exp
from numpy import max
import copy


import platform
from platform import system

def get_os():
    os = platform.system()
    return os

def get_path_home_folder():
    if get_os() == "Windows":
        path_home = abspath(getcwd()) + "\Teams\Home\\"
    else:
        path_home = abspath(getcwd()) + "/Teams/Home/"
    return path_home

def get_path_away_folder():
    if get_os() == "Windows":
        path_away = abspath(getcwd()) + "\Teams\Away\\"
    else:
        path_away = abspath(getcwd()) + "/Teams/Away/"
    return path_away

def get_path_apprun_folder():
    apprun_folder = abspath(getcwd())
    return apprun_folder

def sigmoid(x):
    # kontrola pro velka cisla
    if x > 500 :
        x = 100
    if x < -500:
        x = -500
    calculated =  1 / (1 + exp(-x))
    return calculated
                                                                                            # ! exp a max jsou z numpy ne z math modulu !!
def softmax(x):
    e_x = exp(x - max(x))
    return e_x / e_x.sum()

def load_data(file_name):
    data_list=[]
    file = open(file_name, 'r')
    for line in file:
        line=line.replace("'", "")
        data_list.append(  line.strip() )
    file.close()
    for loop in range (0,len(data_list)):
        data_list[loop]= data_list[loop].replace("'", "")
    return data_list


def create_model_tf2(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(1,13)),
        tf.keras.layers.Dense(5,activation="relu"),
        tf.keras.layers.Dense(5,activation="softmax")
        ])

    model.compile(optimizer="adam",loss='sparse_categorical_crossentropy',metrics=["accuracy"])

    return model

## !
##  TRAIN MDEL zkontrolovat code BO SE SPUSTI AZ PO KONTROLE slozek , tz model bude vzdy existovat !!!!!!!
## !

def train_model(train_data,train_labels,model_ID_h5):
    path = get_path_home_folder()
    model = load_model_from_5h(path +  model_ID_h5  + ".h5")
    try :
        model.fit(train_data, train_labels)
        model.save(path +  model_ID_h5  + ".h5")
    except Exception as e:
        #print("train_data" , train_data)
        #print("train_labels" , train_labels)

        print(e)


def load_model_from_5h(new_model):
    print("mmmodel",new_model )
    model = load_model(new_model)
    return model


def proces_reinforsment_data(player_ID, data_trening, data_labels):
    #print ("data_trening",data_trening )
    #print ("data_labels",data_labels )
    pass

#---------------------  nasledujici funkce jsou pouze pro testy a kontrolu keras modelu  ----------------------------------------

#--------------------------------------------------------------------------------
