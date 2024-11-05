FROM python:3.9.20-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# 创建日志目录
RUN mkdir -p /app/Log

# 启动 ImageProduce.py 应用
CMD ["uvicorn", "poll:app", "--host", "0.0.0.0", "--port", "8000"]