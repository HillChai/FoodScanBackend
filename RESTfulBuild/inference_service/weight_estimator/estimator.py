from keras.applications.inception_v3 import InceptionV3
from keras.layers import Dense, Dropout, Flatten, AveragePooling2D, Input
from keras.models import Model
from keras.preprocessing import image
import numpy as np
import json

class WeightEstimator:
    def __init__(self, model_weights, config_file):
        # 加载配置文件

        # 创建模型并加载权重

        # 加载保存的模型权重
        pass
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

    def estimate_weight(self, img):
        # 预处理图像
        img_array = self.preprocess_image(img)
        # 进行预测
        return round(100.00, 2)  # 保留两位小数
