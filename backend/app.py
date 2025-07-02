from flask import Flask, jsonify
from flask_cors import CORS  # 解决跨域问题

app = Flask(__name__)
CORS(app)  # 允许所有跨域请求（开发环境用）

# 接口：返回"你好"
@app.route('/hello', methods=['GET'])
# 定义一个名为hello的函数
def hello():
    # 返回一个json格式的消息
    return jsonify({"message": "你好"})

if __name__ == '__main__':
    # 关键：监听0.0.0.0，允许容器外部访问
    app.run(host='0.0.0.0', port=5000, debug=True)