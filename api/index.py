from flask import Flask, request, jsonify
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import poster_generator, app, generator

# Vercel Serverless函数入口
@app.route('/api/generate_poster', methods=['POST'])
def api_generate_poster():
    """API端点用于生成海报"""
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
            
            # 分析动画描述，获取更详细的动画信息
             keywords = generator.analyze_animation_description(animation_description)
             is_complex = generator.is_complex_description(animation_description)
             
             animation_info = {
                 'type': 'custom',
                 'name': '自定义动画',
                 'keywords': keywords,
                 'description': animation_description,
                 'complex': is_complex,
                 'animation_class': 'animation-custom'
             }
            
            # 根据描述类型设置具体的动画类名
            if '波浪' in animation_description or 'wave' in animation_description.lower():
                animation_info['animation_class'] = 'animation-wave'
            elif '螺旋' in animation_description or 'spiral' in animation_description.lower():
                animation_info['animation_class'] = 'animation-spiral'
            elif '弹跳' in animation_description or 'bounce' in animation_description.lower():
                animation_info['animation_class'] = 'animation-multi-bounce'
            elif '旋转' in animation_description or 'rotate' in animation_description.lower():
                animation_info['animation_class'] = 'animation-rotate3d'
            elif is_complex:
                animation_info['animation_class'] = 'animation-combined'
                
            return jsonify({
                'success': True,
                'poster_html': poster_html,
                'animation_info': animation_info
            })
        else:
            # 使用预设动画
            poster_html = poster_generator.generate_poster_html(title, text, animation, color_theme)
            
            return jsonify({
                'success': True,
                'poster_html': poster_html,
                'animation_info': {
                    'type': 'preset',
                    'name': animation,
                    'animation_class': f'animation-{animation}' if animation != 'none' else ''
                }
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Vercel需要这个handler
handler = app