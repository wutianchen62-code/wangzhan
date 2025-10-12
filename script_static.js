class PosterGenerator {
    constructor() {
        this.initEventListeners();
        this.setupAnimationTypeToggle();
        this.setupRealTimePreview();
    }

    initEventListeners() {
        const generateBtn = document.getElementById('generate-btn');
        generateBtn.addEventListener('click', () => this.generatePoster());
    }

    setupAnimationTypeToggle() {
        const animationTypeSelect = document.getElementById('animation-type');
        const presetGroup = document.getElementById('preset-animation-group');
        const customGroup = document.getElementById('custom-animation-group');

        animationTypeSelect.addEventListener('change', (e) => {
            if (e.target.value === 'preset') {
                presetGroup.style.display = 'block';
                customGroup.style.display = 'none';
            } else {
                presetGroup.style.display = 'none';
                customGroup.style.display = 'block';
            }
        });
    }

    setupRealTimePreview() {
        const inputs = ['title', 'content', 'animation', 'color'];
        inputs.forEach(inputId => {
            const element = document.getElementById(inputId);
            if (element) {
                element.addEventListener('input', () => this.updatePreview());
                element.addEventListener('change', () => this.updatePreview());
            }
        });
    }

    updatePreview() {
        const title = document.getElementById('title').value || '动态海报';
        const content = document.getElementById('content').value || '这是您的动态海报内容';
        const animation = document.getElementById('animation').value;
        const color = document.getElementById('color').value;

        if (title || content) {
            const posterHtml = this.generateStaticPoster(title, content, animation, color);
            this.displayPreview(posterHtml);
        }
    }

    generateStaticPoster(title, content, animation, color) {
        const animationCSS = this.getAnimationCSS(animation);
        const colorCSS = this.getColorCSS(color);

        return `
            <div class="poster ${color} ${animation}" style="${colorCSS}">
                <div class="poster-content">
                    <h2 class="poster-title">${title}</h2>
                    <p class="poster-text">${content}</p>
                </div>
                <style>
                    .poster { ${animationCSS} }
                </style>
            </div>
        `;
    }

    getAnimationCSS(animation) {
        const animations = {
            'pulse': `
                animation: pulse 2s ease-in-out infinite;
            `,
            'bounce': `
                animation: bounce 1s ease-in-out infinite;
            `,
            'fade': `
                animation: fade 3s ease-in-out infinite;
            `,
            'slide': `
                animation: slide 2s ease-in-out infinite;
            `,
            'rotate': `
                animation: rotate 4s linear infinite;
            `
        };

        return animations[animation] || animations['pulse'];
    }

    getColorCSS(color) {
        const colors = {
            'gradient-blue': `
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            `,
            'gradient-purple': `
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            `,
            'gradient-green': `
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
            `,
            'gradient-orange': `
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                color: white;
            `,
            'gradient-red': `
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                color: white;
            `
        };

        return colors[color] || colors['gradient-blue'];
    }

    displayPreview(html) {
        const container = document.getElementById('poster-container');
        container.innerHTML = html;
    }

    async generatePoster() {
        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;
        const animationType = document.getElementById('animation-type').value;
        const animation = document.getElementById('animation').value;
        const animationDescription = document.getElementById('animation-description').value;
        const color = document.getElementById('color').value;

        if (!title || !content) {
            this.showMessage('请输入标题和内容', 'error');
            return;
        }

        // 如果是自定义动画类型，需要检查描述
        if (animationType === 'custom' && !animationDescription.trim()) {
            this.showMessage('请输入自定义动画描述', 'error');
            return;
        }

        this.showLoading();

        try {
            // 尝试调用后端API
            const response = await fetch('/api/generate_poster', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: title,
                    text: content,
                    animation: animation,
                    color_theme: color,
                    animation_type: animationType,
                    animation_description: animationDescription
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                if (result.success) {
                    this.displayGeneratedPoster(result.poster_html);
                    let message = '海报生成成功！';
                    if (result.animation_info) {
                        message += ` 动画类型：${result.animation_info.type}`;
                        if (result.animation_info.name) {
                            message += `，名称：${result.animation_info.name}`;
                        }
                    }
                    this.showMessage(message, 'success');
                } else {
                    throw new Error(result.error || '生成失败');
                }
            } else {
                // 如果后端API不可用，使用本地生成
                await new Promise(resolve => setTimeout(resolve, 1000));
                const posterHtml = this.generateStaticPoster(title, content, animation, color);
                this.displayGeneratedPoster(posterHtml);
                this.showMessage('海报生成成功！（本地模式）', 'success');
            }
            
        } catch (error) {
            console.error('生成失败:', error);
            // 如果网络请求失败，使用本地生成
            await new Promise(resolve => setTimeout(resolve, 1000));
            const posterHtml = this.generateStaticPoster(title, content, animation, color);
            this.displayGeneratedPoster(posterHtml);
            this.showMessage('海报生成成功！（本地模式）', 'success');
        } finally {
            this.hideLoading();
        }
    }

    displayGeneratedPoster(html) {
        const container = document.getElementById('poster-container');
        container.innerHTML = html;
        
        // 添加下载按钮
        const downloadBtn = document.createElement('button');
        downloadBtn.className = 'download-btn';
        downloadBtn.innerHTML = '📥 下载海报';
        downloadBtn.onclick = () => this.downloadPoster();
        
        container.appendChild(downloadBtn);
    }

    downloadPoster() {
        this.showMessage('下载功能在静态版本中不可用', 'info');
    }

    showLoading() {
        const btn = document.getElementById('generate-btn');
        const btnText = btn.querySelector('.btn-text');
        const loading = btn.querySelector('.loading');
        
        btnText.style.display = 'none';
        loading.style.display = 'inline-block';
        btn.disabled = true;
    }

    hideLoading() {
        const btn = document.getElementById('generate-btn');
        const btnText = btn.querySelector('.btn-text');
        const loading = btn.querySelector('.loading');
        
        btnText.style.display = 'inline-block';
        loading.style.display = 'none';
        btn.disabled = false;
    }

    showMessage(message, type = 'info') {
        // 移除现有消息
        const existingMessage = document.querySelector('.message-popup');
        if (existingMessage) {
            existingMessage.remove();
        }

        // 创建新消息
        const messageDiv = document.createElement('div');
        messageDiv.className = `message-popup ${type}`;
        messageDiv.innerHTML = `
            <span class="message-icon">${this.getMessageIcon(type)}</span>
            <span class="message-text">${message}</span>
        `;

        // 添加到页面
        document.body.appendChild(messageDiv);

        // 显示动画
        setTimeout(() => {
            messageDiv.classList.add('show');
        }, 10);

        // 3秒后自动消失
        setTimeout(() => {
            messageDiv.classList.remove('show');
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.parentNode.removeChild(messageDiv);
                }
            }, 300);
        }, 3000);
    }

    getMessageIcon(type) {
        const icons = {
            'success': '✅',
            'error': '❌',
            'info': 'ℹ️',
            'warning': '⚠️'
        };
        return icons[type] || icons['info'];
    }
}

// 添加消息样式
const messageStyles = `
    .message-popup {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-left: 4px solid #007bff;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        z-index: 1000;
        max-width: 300px;
    }
    
    .message-popup.show {
        transform: translateX(0);
    }
    
    .message-popup.success {
        border-left-color: #28a745;
    }
    
    .message-popup.error {
        border-left-color: #dc3545;
    }
    
    .message-popup.info {
        border-left-color: #007bff;
    }
    
    .message-popup.warning {
        border-left-color: #ffc107;
    }
    
    .message-icon {
        margin-right: 10px;
        font-size: 16px;
    }
    
    .message-text {
        font-size: 14px;
        color: #333;
    }
    
    .download-btn {
        background: #28a745;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 15px;
        font-size: 14px;
    }
    
    .download-btn:hover {
        background: #218838;
    }
`;

// 添加样式到页面
const styleSheet = document.createElement('style');
styleSheet.textContent = messageStyles;
document.head.appendChild(styleSheet);

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new PosterGenerator();
});