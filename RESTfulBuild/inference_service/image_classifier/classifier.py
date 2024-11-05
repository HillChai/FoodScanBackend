from keras.applications.inception_v3 import InceptionV3
from keras.layers import Dense, Dropout, Flatten, AveragePooling2D, Input
from keras.models import Model
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

class ImageClassifier:
    def __init__(self, model_weights, class_file):
        # 定义类别映射
        self.class_to_ix = {}
        self.ix_to_class = {}
        with open(class_file, 'r') as txt:
            classes = [l.strip() for l in txt.readlines()]
            self.class_to_ix = dict(zip(classes, range(len(classes))))
            self.ix_to_class = dict(zip(range(len(classes)), classes))

        # 创建模型并加载权重
        base_model = InceptionV3(weights=None, include_top=False, input_tensor=Input(shape=(299, 299, 3)))
        x = base_model.output
        x = AveragePooling2D(pool_size=(8, 8))(x)
        x = Dropout(0.4)(x)
        x = Flatten()(x)
        predictions = Dense(len(self.class_to_ix), activation='softmax')(x)  # 动态设置类别数
        self.model = Model(inputs=base_model.input, outputs=predictions)

        # 加载保存的模型权重
        self.model.load_weights(model_weights)

    def preprocess_image(self, img):
        # 加载图像并调整大小
        img = img.resize((299, 299))
        # 将图像转换为数组
        img_array = image.img_to_array(img)
        # 扩展维度，以适应模型输入
        img_array = np.expand_dims(img_array, axis=0)
        # 进行与训练相同的归一化
        img_array /= 255.0
        return img_array

    def predict_image(self, img):
        # 预处理图像
        img_array = self.preprocess_image(img)
        # 进行预测
        preds = self.model.predict(img_array)
        # 获取预测类别的索引
        pred_class_idx = np.argmax(preds, axis=1)[0]
        # 将索引转换为类别名称
        pred_class_name = self.ix_to_class[pred_class_idx]
        return pred_class_name

    def display_image_with_prediction(self, img_path, prediction):
        # 加载原始图像
        img = image.load_img(img_path)
        plt.imshow(img)
        plt.axis('off')
        # 显示预测结果
        plt.title(f'Predicted Class: {prediction}', fontsize=16, color='blue')
        plt.show()
