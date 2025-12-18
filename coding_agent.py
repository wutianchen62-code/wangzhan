from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import re
import os
import time

app = Flask(__name__)
# 启用CORS支持，允许所有域名访问
CORS(app, resources={r"/*": {"origins": "*"}})

# Vercel环境检测
IS_VERCEL = 'VERCEL' in os.environ

# 设置静态文件路径
if IS_VERCEL:
    app.static_folder = 'templates'
    app.template_folder = 'templates'

class PosterCodingAgent:
    def __init__(self, api_url, api_key, model_name="deepseek-v3_2"):
        self.api_url = api_url
        self.api_key = api_key
        self.model_name = model_name
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.api_key}"
        }
    
    def generate_poster_code(self, description):
        """调用AI API生成海报代码"""
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                # 构建提示词
                prompt = f"""
你是一个专业的前端开发工程师，擅长创建动态海报。请根据以下自然语言描述生成完整的HTML海报代码：

{description}

要求：
1. 生成完整的HTML代码，包括HTML、CSS和JavaScript
2. 确保动画效果流畅自然
3. 使用现代CSS技术实现动画效果
4. 代码结构清晰，易于理解
5. 包含适当的注释
6. 确保在浏览器中能直接运行

请只返回HTML代码，不要包含任何解释或说明。
"""
                
                # OpenAI兼容API格式
                data = {
                    'model': self.model_name,
                    'messages': [
                        {'role': 'system', 'content': '你是一个专业的前端开发工程师，擅长创建动态海报。'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'max_tokens': 4000,
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'stream': False
                }
                
                # 发送请求
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=data,
                    timeout=600  # 增加超时时间到120秒
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 解析DeepSeek API响应格式
                    if 'choices' in result and len(result['choices']) > 0:
                        html_code = result['choices'][0]['message']['content'].strip()
                        
                        # 清理AI返回的代码
                        html_code = re.sub(r'```html\n?|```', '', html_code)
                        html_code = html_code.strip()
                        
                        return html_code
                    else:
                        raise Exception(f"API响应格式错误: {result}")
                else:
                    raise Exception(f"API请求失败: {response.status_code} - {response.text}")
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"第{attempt + 1}次请求超时，{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 指数退避
                    continue
                else:
                    raise Exception(f"API请求超时，已重试{max_retries}次")
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"第{attempt + 1}次请求失败，{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    raise Exception(f"生成海报代码失败: {str(e)}")

# 全局配置
DEFAULT_API_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'

# 主页路由 - 显示前端界面
@app.route('/')
def index():
    """显示海报生成器主页"""
    if IS_VERCEL:
        # 在Vercel环境下，直接返回HTML内容
        try:
            with open('templates/index.html', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            # 如果文件不存在，返回简单的HTML
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>AI海报生成器</title>
                <meta charset="utf-8">
            </head>
            <body>
                <h1>AI海报生成器</h1>
                <p>应用正在启动中...</p>
            </body>
            </html>
            """
    else:
        return render_template('index.html')

# 生成海报API路由
@app.route('/api/generate_poster', methods=['POST'])
def generate_poster():
    """生成海报API"""
    try:
        data = request.get_json()
        
        api_url = data.get('api_url', DEFAULT_API_URL)
        api_key = data.get('api_key')
        description = data.get('description')
        model_name = data.get('model', 'deepseek-v3_2')
        
        if not api_key or not description:
            return jsonify({
                'success': False,
                'error': '请提供API密钥和海报描述'
            })
        
        # 创建Coding Agent实例
        coding_agent = PosterCodingAgent(api_url, api_key, model_name)
        
        # 生成海报代码
        html_code = coding_agent.generate_poster_code(description)
        
        return jsonify({
            'success': True,
            'poster_code': html_code
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# 只在本地开发时启动Flask服务器
if __name__ == '__main__' and not IS_VERCEL:
    app.run(debug=True, host='0.0.0.0', port=5001)