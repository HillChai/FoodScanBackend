FROM python:3.9.20-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mkdir -p /app/Log

CMD ["uvicorn", "modify:app", "--host", "0.0.0.0", "--port", "8000"]