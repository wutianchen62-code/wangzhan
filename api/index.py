import json
import os
from flask import Flask, request as flask_request, jsonify

app = Flask(__name__)

# 允许跨域请求
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# API路由 - 海报生成
@app.route('/api/generate_poster', methods=['POST'])
def generate_poster():
    try:
        data = flask_request.get_json()
        
        # 这里应该调用AI API生成海报
        # 暂时返回模拟数据
        return jsonify({
            'success': True,
            'poster_url': 'https://example.com/poster.png',
            'message': '海报生成成功（模拟数据）'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Vercel Serverless函数入口
def handler(req, res):
    # 将Vercel请求转换为Flask请求
    with app.test_request_context(
        path=req.path,
        method=req.method,
        headers=dict(req.headers),
        data=req.body if hasattr(req, 'body') and req.body else None
    ):
        try:
            # 处理请求
            flask_response = app.full_dispatch_request()
            
            # 构建响应
            res.status_code = flask_response.status_code
            
            # 设置响应头
            for header, value in flask_response.headers:
                res.headers[header] = value
            
            # 设置响应体
            if isinstance(flask_response.response, list):
                res.body = b''.join(flask_response.response)
            else:
                res.body = flask_response.data
                
        except Exception as e:
            # 错误处理
            res.status_code = 500
            res.headers['Content-Type'] = 'application/json'
            res.body = json.dumps({
                'success': False,
                'error': f'服务器错误: {str(e)}'
            }).encode('utf-8')
    
    return res