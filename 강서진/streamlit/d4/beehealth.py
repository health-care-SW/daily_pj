import os
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import glob
import PIL
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras import layers
import tensorflow as tf

from io import StringIO

## 데이터프레임
bees = pd.read_csv('bee_data.csv',
                    index_col=False, parse_dates={'datetime':[1,2]},
                    dtype={"subspecies":'category',"health":'category',"caste":'category'})

bees = bees.replace({'location':'Athens, Georgia, USA'}, 'Athens, GA, USA')

# ---------------------------------------
# 이미지 & 레이블 전처리
# ---------------------------------------
img_folder = 'archive\\bee_imgs\\bee_imgs\\'
files = glob.glob(img_folder+'*.png')

x_data = []
y_data = []

for img_path in files:
  img = PIL.Image.open(img_path)

  # 이미지 파일명 추출
  img_name = img_path.split('\\')[-1]

  img = img.convert('RGB')
  img = img.resize((64, 64))
  np_img = np.array(img)
  x_data.append(np_img)

  # health 레이블 읽어와 y에 저장
  hp = bees['health'].values[bees.index[(bees['file']==img_name)][0]]
  y_data.append(hp)

x_data = np.array(x_data)
y_data = np.array(y_data)

# y는 string이므로 정수로 변환
health_dict = {'healthy':0, 'few varrao, hive beetles':1, 'Varroa, Small Hive Beetles': 2, 'ant problems':3, 'hive being robbed':4, 'missing queen':5}
new_y_data = []

for item in y_data:
  y_int = health_dict[item]
  new_y_data.append(y_int)

new_y_data = np.array(new_y_data)

# ---------------------------------------
# train data, test data 나누기
# ---------------------------------------
x_train, x_test, y_train, y_test = train_test_split(x_data, new_y_data, test_size=0.2)
x_train, x_test = x_train/255.0, x_test/255.0

# ---------------------------------------
# 모델 쌓기
# ---------------------------------------
input_img = layers.Input(shape=(64,64,3)) # input 크기: 64, 64, 3 

tower_1= layers.Conv2D(64, (1,1), padding = 'same', activation = 'relu')(input_img)

tower_2= layers.Conv2D(64, (1,1), padding = 'same', activation = 'relu')(input_img)
tower_2= layers.Conv2D(64, (3,3), padding = 'same', activation = 'relu')(tower_2)

tower_3= layers.MaxPooling2D((3,3), padding = 'same', strides = (1,1))(input_img)
tower_3= layers.Conv2D(64, (3,3), padding = 'same', activation = 'relu')(tower_3)

tower_4= layers.Conv2D(64, (1,1), padding = 'same', activation = 'relu')(input_img)
tower_4= layers.Conv2D(64, (3,3), padding = 'same', activation = 'relu')(tower_4)
tower_4= layers.Conv2D(64, (3,3), padding = 'same', activation = 'relu')(tower_4)

concat_layer = layers.concatenate([tower_1, tower_2, tower_3, tower_4], axis = 3) #axis 3번째 값을 기준으로 합친다 
flat_layer = layers.Flatten()(concat_layer)
output = layers.Dense(6, activation = 'softmax')(flat_layer) # 마지막 층: 6개 => health의 상태: 6종류

model = tf.keras.models.Model(input_img, output)

model.summary()

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# ---------------------------------------
# 학습 돌리기
# ---------------------------------------
# history = model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs = 20)

model.save("model.h5")




