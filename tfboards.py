
import neural_network
from neural_network import *
import reinforsment_learning
from reinforsment_learning import *
import numpy as np



dat = load_data("training.txt")
daat = load_datalabels("traininglabels.txt")

train_model_tensorflowboard_mdl_1(dat,daat[0],1)
train_model_tensorflowboard_mdl_2(dat,daat[0],1)
