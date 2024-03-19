# 以python 3.10 官方 image 作為基底
FROM python:3.10

# 指定工作的起始資料夾在 /app/
WORKDIR /app

# 當前寫好的程式碼複製到 Docker Image 中的 /app/
COPY . /app/

# 使用 pip 安裝所需的 python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 打開 8080 端口
EXPOSE 8080

# 容器啟動時執行的命令
CMD ["python", "main.py"]