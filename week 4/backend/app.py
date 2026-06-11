from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/api/test_get', methods=['GET'])
def test_get():
    user_input = request.args.get('param1', '空')
    return jsonify({
        "status": "success",
        "result": f"参数是{user_input}"
    })


@app.route('/api/test_post', methods=['POST'])
def test_post():
    param_data = request.args.get('my_param', '空')
    
    body_data = "空"
    if request.is_json:
        body_data = request.json.get('my_body', '空') 
        
    # 在后端终端里打印出隐藏在 Body 里的数据
    print(f"\n [探针] 收到了 POST 强信号 Body 数据是: {body_data}，URL 参数是: {param_data}\n")
        
    return jsonify({
        "status": "success",
        "result": f"body中的参数是{body_data}，param中的参数是{param_data}"
    })

if __name__ == '__main__':
    print(" Flask 启动，监听端口: 5000")
    app.run(debug=True, port=5000)