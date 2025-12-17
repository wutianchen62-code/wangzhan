import json

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
            
            # 模拟海报生成（返回前端期望的格式）
            poster_code = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI生成海报</title>
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            color: white;
        }}
        .poster {{
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        p {{
            font-size: 1.2rem;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="poster">
        <h1>🎨 AI海报生成器</h1>
        <p>基于您的描述生成的海报预览</p>
        <p style="margin-top: 20px; font-size: 1rem; opacity: 0.8;">
            描述：{data.get('description', '')[:100]}...
        </p>
    </div>
</body>
</html>
            '''
            
            response.status_code = 200
            response.body = json.dumps({
                'success': True,
                'poster_code': poster_code,
                'message': '海报生成成功'
            }).encode('utf-8')
            
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