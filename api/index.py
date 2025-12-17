import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from coding_agent import app

# Vercel Serverless函数入口
def handler(request, response):
    # 处理API请求
    if request.path.startswith('/api/'):
        # 调用Flask应用处理API请求
        with app.test_client() as client:
            # 构建Flask请求
            flask_response = client.open(
                path=request.path,
                method=request.method,
                headers=dict(request.headers),
                data=request.body if request.body else None
            )
            
            # 返回Vercel响应
            response.status_code = flask_response.status_code
            response.headers.update(dict(flask_response.headers))
            response.body = flask_response.data
            return response
    
    # 处理前端页面请求
    else:
        # 返回前端HTML页面
        try:
            with open(os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html'), 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            response.status_code = 200
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.body = html_content
            return response
        except FileNotFoundError:
            response.status_code = 200
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.body = '<html><body><h1>AI海报生成器</h1><p>应用正在启动中...</p></body></html>'
            return response