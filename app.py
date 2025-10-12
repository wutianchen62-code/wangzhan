from flask import Flask, request, jsonify, render_template_string
import json
import random
from datetime import datetime

app = Flask(__name__)

class PosterGenerator:
    def __init__(self):
        self.animation_styles = {
            'pulse': 'animation: pulse 2s infinite;',
            'bounce': 'animation: bounce 2s infinite;',
            'fade': 'animation: fade 2s infinite;',
            'slide': 'animation: slide 3s infinite;',
            'rotate': 'animation: rotate 10s infinite linear;'
        }
        
        self.color_themes = {
            'gradient-blue': 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);',
            'gradient-purple': 'background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);',
            'gradient-sunset': 'background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);',
            'gradient-forest': 'background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);',
            'gradient-ocean': 'background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);'
        }
        
        self.decorative_elements = [
            '✨', '🌟', '💫', '🎯', '🎨', '🎭', '🎪', '🎨', '⭐', '🌈',
            '🔥', '⚡', '💎', '💡', '🚀', '🌙', '☀️', '🌺', '🦋', '🐉'
        ]
        
        # Coding Agent 预设模板
        self.animation_templates = {
            'slide_bounce': {
                'name': 'slide_bounce',
                'css': '''
@keyframes slide_bounce {
    0% { transform: translateX(-100px) scale(0.8); opacity: 0; }
    60% { transform: translateX(20px) scale(1.1); opacity: 1; }
    80% { transform: translateX(-10px) scale(1.05); }
    100% { transform: translateX(0) scale(1); opacity: 1; }
}
.animation-slide_bounce { animation: slide_bounce 1.5s ease-out; }'''
            },
            'fade_scale': {
                'name': 'fade_scale',
                'css': '''
@keyframes fade_scale {
    0% { transform: scale(0.5); opacity: 0; }
    50% { transform: scale(1.1); opacity: 0.8; }
    100% { transform: scale(1); opacity: 1; }
}
.animation-fade_scale { animation: fade_scale 2s ease-in-out; }'''
            }
        }

    def generate_poster_html(self, title, content, animation, color_theme):
        """生成动态海报HTML"""
        
        # 添加装饰元素
        decorations = self.generate_decorations()
        
        # 生成CSS样式
        css_style = self.generate_css(animation, color_theme)
        
        # 创建HTML结构
        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                {css_style}
            </style>
        </head>
        <body>
            <div class="poster-main">
                {decorations}
                <div class="poster-content">
                    <h1 class="poster-title">{title}</h1>
                    <p class="poster-text">{content}</p>
                    <div class="poster-footer">
                        <span class="timestamp">{datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
                        <span class="ai-badge">AI生成</span>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content

    def generate_custom_poster_html(self, title, content, custom_animation, color_theme):
        """生成包含自定义动画的动态海报HTML"""
        
        # 添加装饰元素
        decorations = self.generate_decorations()
        
        # 生成包含自定义动画的CSS样式
        css_style = self.generate_custom_css(custom_animation, color_theme)
        
        # 创建HTML结构
        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                {css_style}
            </style>
        </head>
        <body>
            <div class="poster-main animation-{custom_animation['name']}">
                {decorations}
                <div class="poster-content">
                    <h1 class="poster-title">{title}</h1>
                    <p class="poster-text">{content}</p>
                    <div class="poster-footer">
                        <span class="timestamp">{datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
                        <span class="ai-badge">AI生成</span>
                        <span class="animation-badge">{custom_animation['name']}</span>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content

    def generate_css(self, animation, color_theme):
        """生成CSS样式"""
        base_animation = self.animation_styles.get(animation, '')
        base_color = self.color_themes.get(color_theme, self.color_themes['gradient-blue'])
        
        css = f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', 'Microsoft YaHei', sans-serif;
            overflow: hidden;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .poster-main {{
            {base_color}
            width: 80%;
            max-width: 800px;
            height: 500px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
            {base_animation}
        }}
        
        .poster-content {{
            position: relative;
            z-index: 10;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 40px;
            color: white;
        }}
        
        .poster-title {{
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            animation: titleGlow 3s ease-in-out infinite alternate;
        }}
        
        .poster-text {{
            font-size: 1.5em;
            line-height: 1.6;
            margin-bottom: 40px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            max-width: 80%;
        }}
        
        .poster-footer {{
            position: absolute;
            bottom: 20px;
            right: 30px;
            display: flex;
            gap: 15px;
            align-items: center;
        }}
        
        .timestamp {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .ai-badge {{
            background: rgba(255,255,255,0.2);
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        .animation-badge {{
            background: rgba(255,255,255,0.3);
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.7em;
            font-family: monospace;
        }}
        
        /* 装饰元素 */
        .decoration {{
            position: absolute;
            font-size: 2em;
            opacity: 0.6;
            animation: float 6s ease-in-out infinite;
        }}
        
        .decoration:nth-child(1) {{ top: 10%; left: 10%; animation-delay: 0s; }}
        .decoration:nth-child(2) {{ top: 20%; right: 15%; animation-delay: 1s; }}
        .decoration:nth-child(3) {{ bottom: 20%; left: 20%; animation-delay: 2s; }}
        .decoration:nth-child(4) {{ bottom: 10%; right: 10%; animation-delay: 3s; }}
        
        /* 动画定义 */
        @keyframes titleGlow {{
            from {{ text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }}
            to {{ text-shadow: 2px 2px 20px rgba(255,255,255,0.5), 0 0 30px rgba(255,255,255,0.3); }}
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-20px) rotate(180deg); }}
        }}
        
        {self.generate_animation_keyframes(animation)}
        """
        
        return css

    def generate_custom_css(self, custom_animation, color_theme):
        """生成包含自定义动画的CSS样式"""
        base_color = self.color_themes.get(color_theme, self.color_themes['gradient-blue'])
        
        css = f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', 'Microsoft YaHei', sans-serif;
            overflow: hidden;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .poster-main {{
            {base_color}
            width: 80%;
            max-width: 800px;
            height: 500px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }}
        
        .poster-content {{
            position: relative;
            z-index: 10;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 40px;
            color: white;
        }}
        
        .poster-title {{
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            animation: titleGlow 3s ease-in-out infinite alternate;
        }}
        
        .poster-text {{
            font-size: 1.5em;
            line-height: 1.6;
            margin-bottom: 40px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            max-width: 80%;
        }}
        
        .poster-footer {{
            position: absolute;
            bottom: 20px;
            right: 30px;
            display: flex;
            gap: 15px;
            align-items: center;
        }}
        
        .timestamp {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .ai-badge {{
            background: rgba(255,255,255,0.2);
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        .animation-badge {{
            background: rgba(255,255,255,0.3);
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.7em;
            font-family: monospace;
        }}
        
        /* 装饰元素 */
        .decoration {{
            position: absolute;
            font-size: 2em;
            opacity: 0.6;
            animation: float 6s ease-in-out infinite;
        }}
        
        .decoration:nth-child(1) {{ top: 10%; left: 10%; animation-delay: 0s; }}
        .decoration:nth-child(2) {{ top: 20%; right: 15%; animation-delay: 1s; }}
        .decoration:nth-child(3) {{ bottom: 20%; left: 20%; animation-delay: 2s; }}
        .decoration:nth-child(4) {{ bottom: 10%; right: 10%; animation-delay: 3s; }}
        
        /* 动画定义 */
        @keyframes titleGlow {{
            from {{ text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }}
            to {{ text-shadow: 2px 2px 20px rgba(255,255,255,0.5), 0 0 30px rgba(255,255,255,0.3); }}
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-20px) rotate(180deg); }}
        }}
        
        {custom_animation['css']}
        """
        
        return css

    def generate_animation_keyframes(self, animation):
        """生成动画关键帧"""
        if animation == 'pulse':
            return """
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            """
        elif animation == 'bounce':
            return """
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                40% { transform: translateY(-10px); }
                60% { transform: translateY(-5px); }
            }
            """
        elif animation == 'fade':
            return """
            @keyframes fade {
                0% { opacity: 0.8; }
                50% { opacity: 1; }
                100% { opacity: 0.8; }
            }
            """
        elif animation == 'slide':
            return """
            @keyframes slide {
                0% { transform: translateX(-10px); }
                50% { transform: translateX(10px); }
                100% { transform: translateX(-10px); }
            }
            """
        elif animation == 'rotate':
            return """
            @keyframes rotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            """
        return ""

    def generate_decorations(self):
        """生成装饰元素"""
        decorations = ""
        num_decorations = random.randint(2, 5)
        
        for i in range(num_decorations):
            element = random.choice(self.decorative_elements)
            decorations += f'<div class="decoration">{element}</div>'
        
        return decorations

    def enhance_content(self, content):
        """使用AI增强内容（模拟）"""
        enhancements = [
            "🌟 精彩内容，不容错过！",
            "🎯 专为您的需求定制",
            "✨ 独特设计，彰显个性",
            "🚀 创新理念，引领未来",
            "💡 智慧之选，品质保证"
        ]
        
        if len(content) < 20:
            content += " " + random.choice(enhancements)
        
        return content

    def coding_agent_generate_animation(self, description):
        """Coding Agent：根据用户描述生成自定义动画代码"""
        
        # 分析用户描述，提取关键信息
        keywords = self.analyze_animation_description(description)
        
        # 根据关键词生成对应的动画代码
        animation_code = self.generate_custom_animation(keywords)
        
        return animation_code

    def analyze_animation_description(self, description):
        """分析动画描述，提取关键特征"""
        keywords = {
            'movement': [],
            'timing': '2s',
            'easing': 'ease',
            'effects': []
        }
        
        description_lower = description.lower()
        
        # 检测运动类型
        if any(word in description_lower for word in ['滑动', '滑入', 'slide', 'move']):
            keywords['movement'].append('slide')
        if any(word in description_lower for word in ['弹跳', 'bounce', '跳跃']):
            keywords['movement'].append('bounce')
        if any(word in description_lower for word in ['淡入', '淡出', 'fade', '透明']):
            keywords['movement'].append('fade')
        if any(word in description_lower for word in ['旋转', 'rotate', '转动']):
            keywords['movement'].append('rotate')
        if any(word in description_lower for word in ['缩放', '放大', '缩小', 'scale']):
            keywords['movement'].append('scale')
        if any(word in description_lower for word in ['脉冲', 'pulse', '心跳']):
            keywords['movement'].append('pulse')
        
        # 检测时间参数
        if '快速' in description_lower or 'fast' in description_lower:
            keywords['timing'] = '1s'
        elif '慢速' in description_lower or 'slow' in description_lower:
            keywords['timing'] = '3s'
        
        # 检测缓动函数
        if '线性' in description_lower or 'linear' in description_lower:
            keywords['easing'] = 'linear'
        elif '弹性' in description_lower or 'elastic' in description_lower:
            keywords['easing'] = 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
        elif '弹跳' in description_lower or 'bounce' in description_lower:
            keywords['easing'] = 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
        
        # 检测特殊效果
        if any(word in description_lower for word in ['无限', '循环', 'infinite', 'loop']):
            keywords['effects'].append('infinite')
        if any(word in description_lower for word in ['交替', 'alternate', '来回']):
            keywords['effects'].append('alternate')
        
        return keywords

    def generate_custom_animation(self, keywords):
        """根据关键词生成自定义动画代码"""
        
        animation_name = 'custom_' + '_'.join(keywords['movement'])
        timing = keywords['timing']
        easing = keywords['easing']
        effects = ' '.join(keywords['effects'])
        
        # 生成关键帧动画
        keyframes = self.generate_keyframes(keywords['movement'])
        
        css_code = f"""
@keyframes {animation_name} {{
{keyframes}
}}
.animation-{animation_name} {{ 
    animation: {animation_name} {timing} {easing} {effects}; 
}}
        """
        
        return {
            'name': animation_name,
            'css': css_code.strip(),
            'keywords': keywords
        }

    def generate_keyframes(self, movements):
        """根据运动类型生成关键帧"""
        keyframes = []
        
        # 基础关键帧
        base_frames = {
            0: {},
            50: {},
            100: {}
        }
        
        for movement in movements:
            if movement == 'slide':
                base_frames[0]['transform'] = 'translateX(-100px)'
                base_frames[0]['opacity'] = '0'
                base_frames[100]['transform'] = 'translateX(0)'
                base_frames[100]['opacity'] = '1'
            elif movement == 'bounce':
                base_frames[20]['transform'] = 'translateY(-10px)'
                base_frames[40]['transform'] = 'translateY(0)'
                base_frames[60]['transform'] = 'translateY(-5px)'
                base_frames[80]['transform'] = 'translateY(0)'
            elif movement == 'fade':
                base_frames[0]['opacity'] = '0'
                base_frames[100]['opacity'] = '1'
            elif movement == 'rotate':
                base_frames[0]['transform'] = 'rotate(0deg)'
                base_frames[100]['transform'] = 'rotate(360deg)'
            elif movement == 'scale':
                base_frames[0]['transform'] = 'scale(0.5)'
                base_frames[50]['transform'] = 'scale(1.2)'
                base_frames[100]['transform'] = 'scale(1)'
            elif movement == 'pulse':
                base_frames[0]['transform'] = 'scale(1)'
                base_frames[50]['transform'] = 'scale(1.1)'
                base_frames[100]['transform'] = 'scale(1)'
        
        # 合并关键帧属性
        frames = {}
        for percentage, properties in base_frames.items():
            if percentage not in frames:
                frames[percentage] = {}
            frames[percentage].update(properties)
        
        # 生成CSS代码
        css_lines = []
        for percentage in sorted(frames.keys()):
            properties = frames[percentage]
            if properties:
                prop_str = '; '.join([f'{k}: {v}' for k, v in properties.items()])
                css_lines.append(f'    {percentage}% {{ {prop_str}; }}')
        
        return '\n'.join(css_lines)

# 初始化生成器
poster_generator = PosterGenerator()

@app.route('/')
def index():
    """主页面"""
    return render_template_string(open('index.html', encoding='utf-8').read())

@app.route('/<path:filename>')
def serve_static(filename):
    """静态文件服务"""
    import os
    from flask import send_from_directory
    
    # 允许的文件类型
    allowed_extensions = {'.css', '.js', '.html', '.png', '.jpg', '.jpeg', '.gif', '.ico'}
    
    # 检查文件是否存在且类型允许
    if os.path.isfile(filename) and any(filename.endswith(ext) for ext in allowed_extensions):
        return send_from_directory('.', filename)
    
    # 如果请求的是根目录下的文件，尝试直接返回
    return send_from_directory('.', filename) if os.path.isfile(filename) else 'File not found', 404

@app.route('/style.css')
def style_css():
    return open('style.css', 'r', encoding='utf-8').read(), 200, {'Content-Type': 'text/css'}

@app.route('/script.js')
def script_js():
    return open('script.js', 'r', encoding='utf-8').read(), 200, {'Content-Type': 'application/javascript'}

@app.route('/generate_poster', methods=['POST'])
def generate_poster():
    try:
        data = request.json
        title = data.get('title', '动态海报')
        content = data.get('content', '这是一个动态海报')
        animation_type = data.get('animation_type', 'preset')
        animation = data.get('animation', 'pulse')
        animation_description = data.get('animation_description', '')
        color_theme = data.get('color', 'gradient-blue')
        
        # 使用AI增强内容
        enhanced_content = poster_generator.enhance_content(content)
        
        # 根据动画类型处理
        if animation_type == 'custom' and animation_description.strip():
            # 使用Coding Agent生成自定义动画
            custom_animation = poster_generator.coding_agent_generate_animation(animation_description)
            
            # 生成包含自定义动画的海报HTML
            poster_html = poster_generator.generate_custom_poster_html(
                title, enhanced_content, custom_animation, color_theme
            )
            
            return jsonify({
                'success': True,
                'poster_html': poster_html,
                'animation_info': {
                    'type': 'custom',
                    'name': custom_animation['name'],
                    'keywords': custom_animation['keywords']
                },
                'message': f'自定义动画生成成功！动画名称: {custom_animation["name"]}'
            })
        else:
            # 使用预设动画
            poster_html = poster_generator.generate_poster_html(
                title, enhanced_content, animation, color_theme
            )
            
            return jsonify({
                'success': True,
                'poster_html': poster_html,
                'animation_info': {
                    'type': 'preset',
                    'name': animation
                },
                'message': '海报生成成功！'
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '海报生成失败，请重试！'
        })

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    """提供AI建议"""
    try:
        data = request.json
        user_input = data.get('input', '')
        
        # 模拟AI建议
        suggestions = {
            'titles': [
                '✨ 精彩动态海报',
                '🎯 专业设计展示',
                '🚀 创新视觉体验',
                '🎨 艺术创作空间',
                '💡 智慧视觉设计'
            ],
            'contents': [
                '探索无限可能，创造独特价值，让您的想法成为现实',
                '专业团队精心打造，为您提供最优质的视觉体验',
                '融合创新理念与美学设计，呈现令人印象深刻的作品',
                '每一个细节都经过精心雕琢，展现完美的视觉效果',
                '用创意点亮生活，让设计传递价值，成就您的品牌'
            ],
            'animations': ['pulse', 'bounce', 'fade', 'slide', 'rotate'],
            'colors': ['gradient-blue', 'gradient-purple', 'gradient-sunset', 'gradient-forest', 'gradient-ocean']
        }
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🎨 AI动态海报生成器启动中...")
    print("📱 访问 http://localhost:5000 查看应用")
    app.run(debug=True, port=5000, host='0.0.0.0')