from PIL import Image
import os, glob
import numpy as np

classes = ["monkey","boar","crow"]
num_classes = len(classes)
image_size = 50
num_testdata = 100

#画像の読み込み
X_train = []
X_test = []
y_train = []
y_test = []

for index,class_rabel in enumerate(classes):
    photos_dir = "./" + "images" + "/" + class_rabel
    files = glob.glob(photos_dir + "/*.jpg")
    for i ,file in enumerate(files):
        if i >= 200:
            break
        else:
            image = Image.open(file)
            image = image.convert("RGB")
            image = image.resize((image_size,image_size))
            data = np.asarray(image)

            if i < num_testdata:
                X_test.append(data)
                y_test.append(index)
            else:
                for angle in range(-20,20,5):
                    #画像の回転
                    img_r = image.rotate(angle)
                    data = np.asarray(img_r)
                    X_train.append(data)
                    y_train.append(index)
                    #画像の反転
                    img_trans = image.transpose(Image.FLIP_LEFT_RIGHT)
                    data = np.asarray(img_r)
                    X_train.append(data)
                    y_train.append(index)                    

X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

Xy = (X_train,X_test,y_train,y_test)
np.save("./data_aug.npy",Xy)