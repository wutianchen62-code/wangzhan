import sys
import os
import json
import requests
# api/index.py
from flask import Flask, jsonify

print(f"Python version: {sys.version}", file=sys.stderr)
print(f"Flask import successful: {__name__}", file=sys.stderr)
# 创建 Flask 应用实例
app = Flask(__name__)
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from coding_agent import PosterCodingAgent

# 从coding_agent.py导入默认API URL
from coding_agent import DEFAULT_API_URL

# 使用Vercel期望的函数格式  
def handler(event, context):
    # 解析事件数据
    path = event.get('path', '')
    method = event.get('httpMethod', '')
    body = event.get('body', '{}')
    
    # 设置CORS头
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # 处理预检请求
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'success': True})
        }
    
    # 只处理 /api/generate_poster 路径的POST请求
    if path == '/api/generate_poster' and method == 'POST':
        try:
            # 解析请求体
            data = json.loads(body)
            
            # 验证必需字段
            if not data.get('api_key') or not data.get('description'):
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'success': False,
                        'error': '缺少必需参数：api_key 或 description'
                    })
                }
            
            # 直接使用PosterCodingAgent生成海报
            agent = PosterCodingAgent(

                api_url=data.get('api_url', DEFAULT_API_URL),
                api_key=data.get('api_key'),
                model=data.get('model', 'deepseek-v3_2')
            )
            
            # 生成海报代码
            poster_code = agent.generate_poster_code(data.get('description'))
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'success': True,
                    'poster_code': poster_code,
                    'message': '海报生成成功'
                })
            }
                
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': '无效的JSON格式'
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': f'服务器错误: {str(e)}'
                })
            }
    
    else:
        # 对于其他路径，返回404
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': '接口不存在'
            })
        }

# Vercel Python函数需要导出handler函数
if __name__ == '__main__':
    # 本地测试代码
    pass