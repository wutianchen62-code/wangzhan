from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# 导入海报生成器
from app import poster_generator

@app.route('/')
def index():
    """主页面"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """静态文件服务"""
    return send_from_directory('.', path)

@app.route('/generate_poster', methods=['POST'])
def generate_poster():
    """生成海报API（用于本地开发）"""
    try:
        data = request.get_json()
        
        # 获取用户输入
        title = data.get('title', '动态海报')
        text = data.get('text', '这是您的动态海报内容')
        animation = data.get('animation', 'pulse')
        color_theme = data.get('color_theme', 'gradient-blue')
        animation_type = data.get('animation_type', 'preset')
        animation_description = data.get('animation_description', '')
        
        # 根据动画类型处理
        if animation_type == 'custom' and animation_description:
            # 使用Coding Agent生成自定义动画
            custom_animation = poster_generator.coding_agent_generate_animation(animation_description)
            poster_html = poster_generator.generate_custom_poster_html(
                title, text, custom_animation, color_theme
            )
            
            return jsonify({
                'success': True,
                'poster_html': poster_html,
                'animation_info': {
                    'type': 'custom',
                    'name': custom_animation['name'],
                    'keywords': custom_animation['keywords']
                }
            })
        else:
            # 使用预设动画
            poster_html = poster_generator.generate_poster_html(title, text, animation, color_theme)
            
            return jsonify({
                'success': True,
                'poster_html': poster_html,
                'animation_info': {
                    'type': 'preset',
                    'name': animation
                }
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)