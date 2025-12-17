import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from coding_agent import app

def handler(request, response):
    # 设置CORS头
    response.headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # 处理预检请求
    if request.method == 'OPTIONS':
        response.status_code = 200
        response.body = json.dumps({'success': True}).encode('utf-8')
        return response
    
    # 只处理 /api/generate_poster 路径的POST请求
    if request.path == '/api/generate_poster' and request.method == 'POST':
        try:
            # 解析请求体
            body = request.body.decode('utf-8') if request.body else '{}'
            data = json.loads(body)
            
            # 验证必需字段
            if not data.get('api_key') or not data.get('description'):
                response.status_code = 400
                response.body = json.dumps({
                    'success': False,
                    'error': '缺少必需参数：api_key 或 description'
                }).encode('utf-8')
                return response
            
            # 使用Flask应用处理请求
            with app.test_client() as client:
                flask_response = client.post(
                    '/api/generate_poster',
                    json=data,
                    headers={'Content-Type': 'application/json'}
                )
                
                # 返回Flask响应
                response.status_code = flask_response.status_code
                response.body = flask_response.data
                
        except json.JSONDecodeError:
            response.status_code = 400
            response.body = json.dumps({
                'success': False,
                'error': '无效的JSON格式'
            }).encode('utf-8')
        except Exception as e:
            response.status_code = 500
            response.body = json.dumps({
                'success': False,
                'error': f'服务器错误: {str(e)}'
            }).encode('utf-8')
    
    else:
        # 对于其他路径，返回404
        response.status_code = 404
        response.body = json.dumps({
            'success': False,
            'error': '接口不存在'
        }).encode('utf-8')
    
    return response