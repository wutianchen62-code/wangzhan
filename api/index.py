import sys
import os
import json
from flask import Flask, request, jsonify

print(f"Python version: {sys.version}", file=sys.stderr)
print(f"Flask import successful: {__name__}", file=sys.stderr)

# 创建 Flask 应用实例
app = Flask(__name__)

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from coding_agent import PosterCodingAgent, DEFAULT_API_URL

# 设置CORS的通用响应头
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# 处理预检请求 (OPTIONS)
@app.route('/api/generate_poster', methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path=None):
    response = jsonify({'success': True})
    return add_cors_headers(response)

# 处理生成海报的POST请求
@app.route('/api/generate_poster', methods=['POST'])
def generate_poster():
    try:
        # 解析请求体
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '无效的JSON格式或请求体为空'
            }), 400

        # 验证必需字段
        if not data.get('api_key') or not data.get('description'):
            return jsonify({
                'success': False,
                'error': '缺少必需参数：api_key 或 description'
            }), 400

        # 直接使用PosterCodingAgent生成海报
        agent = PosterCodingAgent(
            api_url=data.get('api_url', DEFAULT_API_URL),
            api_key=data.get('api_key'),
            model=data.get('model', 'deepseek-v3_2')
        )
        
        # 生成海报代码
        poster_code = agent.generate_poster_code(data.get('description'))
        
        response = jsonify({
            'success': True,
            'poster_code': poster_code,
            'message': '海报生成成功'
        })
        return add_cors_headers(response)

    except json.JSONDecodeError:
        return jsonify({
            'success': False,
            'error': '无效的JSON格式'
        }), 400
    except Exception as e:
        print(f"服务器内部错误: {str(e)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}'
        }), 500

# 处理根路径和其他未匹配路由，返回一个简单提示或您的首页
@app.route('/')
@app.route('/<path:path>')
def catch_all(path=None):
    # 这里可以返回您的 index.html，或者一个API提示信息
    # 如果前端是单独的静态站点，这里可以返回重定向或提示
    response = jsonify({
        'success': False,
        'error': '接口不存在，请访问 /api/generate_poster (POST)',
        'available_endpoint': {
            'path': '/api/generate_poster',
            'method': 'POST',
            'description': '生成海报代码'
        }
    })
    response.status_code = 404
    return add_cors_headers(response)

# Vercel需要导出一个名为 `app` 的WSGI应用实例
# 确保这个变量名与创建的应用实例名称一致