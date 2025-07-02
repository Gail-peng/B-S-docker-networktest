# 基于Python镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir flask flask-cors

# 复制项目代码
COPY . .

# 暴露5000端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]