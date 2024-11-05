import logging
import os
from minio import Minio
from image_classifier import ImageClassifier
from weight_estimator import WeightEstimator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("/app/Log/app.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(pathname)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 读取环境变量

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
BUCKET_NAME = os.getenv("BUCKET_NAME", "photos")

IMAGE_TOPIC = os.getenv("IMAGE_TOPIC", "image_topic")
HISTORY_TOPIC = os.getenv("HISTORY_TOPIC", "history_topic")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio123")

# 初始化 MinIO 客户端
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key="minioadmin",
    secret_key="minio123",
    secure=False
)

# 初始化 ImageClassifier
classifier = ImageClassifier(model_weights='models/model_epoch_05_val_loss_0.63.hdf5', class_file='models/classes.txt')
weight_estimator = WeightEstimator(model_weights='models/weight_model.hdf5', config_file='models/weight_config.json')

# 过期时间单位(秒)
expiration_time = 600