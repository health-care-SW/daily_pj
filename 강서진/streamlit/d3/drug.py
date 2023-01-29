import os

os.add_dll_directory(r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin")

import json
import pandas as pd
import glob
import PIL as pil
from PIL import Image
import numpy as np
import tensorflow
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPool2D, Dropout, BatchNormalization,LeakyReLU
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, Callback, EarlyStopping, ReduceLROnPlateau
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

pd.set_option('display.max_columns', None)

labelpath1 = "drug\\라벨링데이터\\경구약제조합 5000종\\"
datapath1 = "drug\\원천데이터\\경구약제조합 5000종\\TS_4_조합\\"

def pathfinder1():
    labelpath2 = glob.glob(labelpath1+"*")
    labelpath3 = []
    for i in labelpath2:
        path = glob.glob(i+'\*')
        labelpath3.append(path)

    labelpath4 = []
    for j in labelpath3:
        for k in j:
            jsondir = glob.glob(k+'\*')
            labelpath4.append(jsondir)

    labelpath = [ i for innerlist in labelpath4 for i in innerlist ]
    return labelpath

def pathfinder2():

    datapath2 = glob.glob(datapath1+'*')
    datapath3 = []

    for i in datapath2:
        path = glob.glob(i+'\*')
        datapath3.append(path)
    
    datapath4 = []
    for j in datapath3:
        for k in j:
            if 'index' not in k:
                datapath4.append(k)

    return datapath4

labelpath = pathfinder1() # 라벨 데이터 경로, 5466개 - 24 = 5442개
datapath = pathfinder2() # 이미지 데이터 경로, 1500개 - 6 = 1494개

# check_lbl = [i.split("\\")[-1][:-5] for i in labelpath] # 5466개
# check_img = [i.split("\\")[-1][:-4] for i in datapath] # 1500개

# falselabel = []
# json은 있고 이미지는 없는 거 걸러내기
# for i in check_lbl:
#     if i not in check_img:
        # print(i)
        # check_lbl.remove(i)
        # falselabel.append(i)
# print(len(check_lbl)) #5454개
# print(len(falselabel))


# print()
# falseimg = []
# 이미지는 있고 json은 없는 거 걸러내기
# for i in check_img:
    # if i not in check_lbl:
        # print(i)
        # check_img.remove(i)
        # falseimg.append(i)
# print(len(check_img)) # 1497개
# print(len(falseimg))

# for i in labelpath:
#     if i.split("\\")[-1][:-5] not in check_lbl:
#         labelpath.remove(i)
# print(len(labelpath))

# for i in datapath:
#     if i.split("\\")[-1][:-4] not in check_img:
#         datapath.remove(i)
# print(len(datapath))


def get_json(labelpath): # len(bbox) == 4 인 파일만 json df로 저장
    label1 = open(labelpath[0], 'r', encoding='utf-8')
    label1 = json.load(label1)

    img1, ant1 = label1.get('images'), label1.get('annotations')

    img1 = pd.json_normalize(img1[0])
    ant1 = pd.json_normalize(ant1[0])

    img1 = img1[['file_name','dl_mapping_code','dl_name']]      
    img1['bbox'] = ant1['bbox']
    # print(len(img1['bbox'][0]))

    for i in labelpath[1:]:
        label = open(i, 'r', encoding='utf-8')
        label = json.load(label)
        img, ant = label.get('images'), label.get('annotations')
        
        timg = pd.json_normalize(img[0])
        tant = pd.json_normalize(ant[0])

        timg = timg[['file_name','dl_mapping_code','dl_name']]

        timg['bbox'] = tant['bbox']

        if len(timg['bbox'][0]) != 4:
            continue

        img1 = pd.concat([img1, timg], ignore_index=True)
        img1.to_csv('drug\\drug.csv', sep=',', encoding="utf-8")
    return img1
# print(len(a)) # 5450개
# a = get_json(labelpath) # csv로 세이브

df = pd.read_csv('drug\\drug.csv', encoding='utf-8') # 5426개
files = df['file_name'].values


def pathfinder3():
    realdatapath = []
    for file in files:
        folder_name = file.split('_')[0]

        path = datapath1 +folder_name+'\\'+file
        realdatapath.append(path)
    return realdatapath

datapath2 = pathfinder3() # json에서 빼온 5426개 이미지 경로. 이미지 자체는 1494장이 있음.


def img_crop():
    k = 0

    for i in range(len(datapath2)):
        l = datapath2[i]
        img = Image.open(l)
        img_title = l.split("\\")[-1]

        j = df.iloc[i]
        bbox = j[-1]
        bbox = bbox[1:-1].split(",")
        bbox = [int(coord) for coord in bbox]

        try:
            x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]

            cropped_img = img.crop((x, y, x+w, y+h))

            newtitle = img_title.replace('.png','')
            # part = newtitle[-19:]

            fname = f"{newtitle}-{j[1]}-{k}.png"
            savepath = "drug\\cropped\\"+ fname
            cropped_img.save(savepath)

            k += 1

        except:
            print(j[0])
# img_crop()

img_path = 'drug\\cropped\\'
imgs = glob.glob(img_path+'*.png')

def train():
    x_data = []
    y_data = []

    for path in imgs:
        
        img = Image.open(path)

        img = img.convert('RGB')
        img = img.resize((64,64))
        np_img = np.array(img)

        x_data.append(np_img)

        path = path.split("\\")[-1]
        path = path.split("-")
        fname, dcode = path[:-3], path[-3:-1]
        fname, dcode = '-'.join(fname)+'.png', '-'.join(dcode)

        # condition = ((df['file_name']==fname) & (df['dl_mapping_code']==dcode))
        # dname = df['dl_name'].values[df.index[condition][0]]
        # y_data.append(dname)

    x_data = np.array(x_data)    
    y_data = pd.get_dummies(df['dl_name'], drop_first=False) # one-hot-encoding
    # y_data = np.array(y_data)

    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2)
    x_train, x_test = x_train, x_test

    # ---------------
    # ---------------

    # Build CNN model
    # model=Sequential()
    # model.add(Conv2D(6, kernel_size=3, input_shape=(64, 64,3), activation='relu', padding='same'))
    # model.add(MaxPool2D(2))
    # model.add(Conv2D(12, kernel_size=3, activation='relu', padding='same'))
    # model.add(Flatten())
    # model.add(Dense(y_train.columns.size, activation='softmax'))
    # model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    from keras.applications import ResNet50
    from keras.layers import GlobalAveragePooling2D, Dense
    from keras.models import Model
    from keras.optimizers import Adam
    model = ResNet50(input_shape=(64, 64, 3), include_top=False, weights='imagenet')
    output = model.output
    model.trainable = False

    x = GlobalAveragePooling2D()(output)
    x = Dense(1000, activation='relu')(x)
    output = Dense(65, activation='softmax', name='output')(x)

    model = Model(inputs=model.input, outputs=output)
    # Train
    model.compile(optimizer=Adam(0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    training = model.fit(x_train, y_train, batch_size=60
                            ,epochs=20
                            ,validation_data=(x_test, y_test) 
                            ,steps_per_epoch=70)

    model.save("drug_model2.h5")

train()