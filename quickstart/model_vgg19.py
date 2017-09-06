from __future__ import print_function
import numpy as np

# from keras.models import Sequential, Model
# from keras.layers import Dense, Dropout, Activation, Flatten, Input
# from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
# from keras.utils import np_utils
# from keras.optimizers import SGD, Adagrad
# from keras.callbacks import EarlyStopping,ModelCheckpoint

from keras import backend as K
K.set_image_dim_ordering('th')

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, Input
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.utils import np_utils
from keras.optimizers import SGD, Adagrad
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras import initializers


import matplotlib
import time
import cPickle

import h5py
from keras.utils.io_utils import HDF5Matrix

from keras import backend as K
import os



def set_keras_backend(backend):

    if K.backend() != backend:
        os.environ['KERAS_BACKEND'] = backend
        reload(K)
        assert K.backend() == backend

set_keras_backend("theano")


# from XtrainYtrain import getRequestCities, xtrainYtrainGenerator
# from XtestYtest import xtestYtestGenerator
# from walk import dataLabel
# from topImageWalk import topClassic

def vgg19(X_train):
	t_start = time.time()
	print (X_train.shape)

	batch_size = 16
	nb_classes = 46
	nb_epoch = 150

	# input image dimensions
	img_rows, img_cols = 187, 100

	# cities = getRequestCities()
	nb_city = nb_classes

	# X_train, Y_train = xtrainYtrainGenerator(cities, nb_city)
	# X_test, Y_test = xtestYtestGenerator(cities, nb_city)
	# X_train, Y_train = dataLabel(nb_city)
	

	# cPickle.dump((X_train, Y_train), open('train_test.p', 'w'))
	# X_train, Y_train = cPickle.load(open('train_test.p', 'r'))

	X_train = X_train.reshape(X_train.shape[0], 3, img_rows, img_cols)
	# X_test = X_test.reshape(X_test.shape[0], 3, img_rows, img_cols)
	X_train = X_train.astype('float32')
	# X_test = X_test.astype('float32')
	X_train /= 255
	# X_test /= 255

	t_generateArray = time.time()
	# print('Generating Array Time:{}'.format(t_generateArray - t_start))
	# print('X_train shape:', X_train.shape)
	# print(X_train.shape[0], 'train samples')
	# # print(X_test.shape[0], 'test samples')

	# # convert class vectors to binary class matrices
	# # Y_train = np_utils.to_categorical(y_train, nb_classes)
	# # Y_test = np_utils.to_categorical(y_test, nb_classes)

	# print ('X_train shape:', X_train.shape)
	# # print ('Y_train shape:', Y_train.shape)

	inputs = Input(shape=(3, img_rows, img_cols))
	pad0 = ZeroPadding2D((1, 1))(inputs)
	conv1 = Convolution2D(64, 3, 3, activation='relu',init='glorot_uniform')(pad0)
	pad1 = ZeroPadding2D((1, 1))(conv1)
	conv2 = Convolution2D(64, 3, 3, activation='relu',init='glorot_uniform')(pad1)
	pool1 = MaxPooling2D((2, 2), strides=(2, 2))(conv2)

	pad2 = ZeroPadding2D((1, 1))(pool1)
	conv3 = Convolution2D(128, 3, 3, activation='relu',init='glorot_uniform')(pad2)
	pad3 = ZeroPadding2D((1, 1))(conv3)
	conv4 = Convolution2D(128, 3, 3, activation='relu',init='glorot_uniform')(pad3)
	pool2 = MaxPooling2D((2, 2), strides=(2, 2))(conv4)

	pad4 = ZeroPadding2D((1, 1))(pool2)
	conv5 = Convolution2D(256, 3, 3, activation='relu',init='glorot_uniform')(pad4)
	pad5 = ZeroPadding2D((1, 1))(conv5)
	conv6 = Convolution2D(256, 3, 3, activation='relu',init='glorot_uniform')(pad5)
	pad6 = ZeroPadding2D((1, 1))(conv6)
	conv7 = Convolution2D(256, 3, 3, activation='relu',init='glorot_uniform')(pad6)
	pad7 = ZeroPadding2D((1, 1))(conv7)
	conv8 = Convolution2D(256, 3, 3, activation='relu',init='glorot_uniform')(pad7)
	pool3 = MaxPooling2D((2, 2), strides=(2, 2))(conv8)

	pad8 = ZeroPadding2D((1, 1))(pool3)
	conv9 = Convolution2D(512, 3, 3, activation='relu',init='glorot_uniform')(pad8)
	pad9 = ZeroPadding2D((1, 1))(conv9)
	conv10 = Convolution2D(512, 3, 3, activation='relu',init='glorot_uniform')(pad9)
	pad10 = ZeroPadding2D((1, 1))(conv10)
	conv11 = Convolution2D(512, 3, 3, activation='relu',init='glorot_uniform')(pad10)
	pad11 = ZeroPadding2D((1, 1))(conv11)
	conv12 = Convolution2D(512, 3, 3, activation='relu',init='glorot_uniform')(pad11)
	pool4 = MaxPooling2D((2, 2), strides=(2, 2))(conv12)

	pad12 = ZeroPadding2D((1, 1))(pool4)
	conv13 = Convolution2D(512, 3, 3, activation='relu',init='glorot_uniform')(pad12)
	pad13 = ZeroPadding2D((1, 1))(conv13)
	conv14 = Convolution2D(512, 3, 3, activation='relu',init='glorot_uniform')(pad13)
	pad14 = ZeroPadding2D((1, 1))(conv14)
	conv15 = Convolution2D(512, 3, 3, activation='relu',init='glorot_uniform')(pad14)
	pad15 = ZeroPadding2D((1, 1))(conv15)
	conv16 = Convolution2D(512, 3, 3, activation='relu',init='glorot_uniform')(pad15)
	pool5 = MaxPooling2D((2, 2), strides=(2, 2))(conv16)

	flatten = Flatten()(pool5)
	dense1 = Dense(1024, activation='relu',init='glorot_uniform')(flatten)
	dropout1 = Dropout(0.5)(dense1)
	dense2 = Dense(1024, activation='relu',init='glorot_uniform')(dropout1)
	dropout2 = Dropout(0.5)(dense2)
	dense3 = Dense(nb_classes, activation='softmax')(dropout2)  # neuron number


	model = Model(input=inputs, output=dense3)

	sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)

	model.compile(loss='categorical_crossentropy',
		              optimizer=sgd)
		              # metrics=['accuracy'])

	print('Loading weights......')
	model.load_weights('./weights/Best_ModelAPI_SGD_weights.h5')
	print("Loaded model from disk")
	predict = model.predict(X_train, batch_size=batch_size, verbose=0)
	# pre_class=model.predict_classes(X_train, batch_size=batch_size, verbose=1)
	# pre_proba=model.predict_proba(X_train, batch_size=batch_size, verbose=1)

	return predict
