class PosterGenerator {
    constructor() {
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.titleInput = document.getElementById('title');
        this.contentInput = document.getElementById('content');
        this.animationTypeSelect = document.getElementById('animation-type');
        this.animationSelect = document.getElementById('animation');
        this.animationDescription = document.getElementById('animation-description');
        this.presetAnimationGroup = document.getElementById('preset-animation-group');
        this.customAnimationGroup = document.getElementById('custom-animation-group');
        this.colorSelect = document.getElementById('color');
        this.generateBtn = document.getElementById('generate-btn');
        this.posterContainer = document.getElementById('poster-container');
        this.btnText = this.generateBtn.querySelector('.btn-text');
        this.loadingText = this.generateBtn.querySelector('.loading');
    }

    bindEvents() {
        this.generateBtn.addEventListener('click', () => this.generatePoster());
        
        // 动画类型切换
        this.animationTypeSelect.addEventListener('change', () => this.toggleAnimationType());
        
        // 实时预览功能
        [this.titleInput, this.contentInput, this.animationSelect, this.animationDescription, this.colorSelect].forEach(element => {
            element.addEventListener('input', () => {
                if (this.hasUserInput()) {
                    this.updatePreview();
                }
            });
        });
    }
    
    toggleAnimationType() {
        const type = this.animationTypeSelect.value;
        if (type === 'preset') {
            this.presetAnimationGroup.style.display = 'block';
            this.customAnimationGroup.style.display = 'none';
        } else {
            this.presetAnimationGroup.style.display = 'none';
            this.customAnimationGroup.style.display = 'block';
        }
    }

    hasUserInput() {
        return this.titleInput.value.trim() !== '' || this.contentInput.value.trim() !== '';
    }

    async generatePoster() {
        if (!this.hasUserInput()) {
            alert('请输入标题或内容！');
            return;
        }

        // 如果是自定义动画类型，需要检查描述
        if (this.animationTypeSelect.value === 'custom' && !this.animationDescription.value.trim()) {
            alert('请输入自定义动画描述！');
            return;
        }

        this.showLoading();
        
        try {
            // 获取用户输入
            const title = this.titleInput.value.trim() || '动态海报';
            const content = this.contentInput.value.trim() || '这是您的动态海报内容';
            const animationType = this.animationTypeSelect.value;
            const animation = this.animationSelect.value;
            const animationDescription = this.animationDescription.value.trim();
            const color = this.colorSelect.value;
            
            // 发送到后端生成
            const apiUrl = window.location.hostname === 'localhost' ? '/generate_poster' : '/api/generate_poster';
            const response = await fetch(apiUrl, {
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
            
            const result = await response.json();
            
            if (result.success) {
                // 显示生成的海报
                this.displayGeneratedPoster(result.poster_html);
                let successMessage = '海报生成成功！';
                if (result.animation_info) {
                    successMessage += ` 动画类型：${result.animation_info.type}，名称：${result.animation_info.name}`;
                }
                this.showSuccessMessage(successMessage);
            } else {
                // 如果后端失败，使用本地生成
                this.createPoster();
            }
            
        } catch (error) {
            console.error('生成海报失败:', error);
            // 如果网络请求失败，使用本地生成
            this.createPoster();
        } finally {
            this.hideLoading();
        }
    }
    
    displayGeneratedPoster(posterHtml) {
        // 创建iframe来显示生成的HTML
        const iframe = document.createElement('iframe');
        iframe.style.cssText = `
            width: 100%;
            height: 400px;
            border: none;
            border-radius: 15px;
            background: white;
        `;
        
        this.posterContainer.innerHTML = '';
        this.posterContainer.appendChild(iframe);
        
        // 写入HTML内容
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        iframeDoc.open();
        iframeDoc.write(posterHtml);
        iframeDoc.close();
        
        // 添加生成动画
        iframe.style.opacity = '0';
        iframe.style.transform = 'scale(0.9)';
        
        setTimeout(() => {
            iframe.style.transition = 'all 0.6s ease';
            iframe.style.opacity = '1';
            iframe.style.transform = 'scale(1)';
        }, 100);
    }

    updatePreview() {
        if (this.hasUserInput()) {
            this.createPoster();
        }
    }

    createPoster() {
        const title = this.titleInput.value.trim() || '动态海报';
        const content = this.contentInput.value.trim() || '这是您的动态海报内容';
        const animation = this.animationSelect.value;
        const color = this.colorSelect.value;

        const posterHTML = this.generatePosterHTML(title, content, animation, color);
        this.posterContainer.innerHTML = posterHTML;
        
        // 添加生成动画
        this.animatePosterCreation();
    }

    generatePosterHTML(title, content, animation, color) {
        return `
            <div class="generated-poster ${color} ${animation === 'none' ? '' : 'animation-' + animation}">
                <h2 class="poster-title">${this.escapeHtml(title)}</h2>
                <p class="poster-content">${this.escapeHtml(content)}</p>
            </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    animatePosterCreation() {
        const poster = this.posterContainer.querySelector('.generated-poster');
        if (poster) {
            poster.style.opacity = '0';
            poster.style.transform = 'scale(0.8) translateY(20px)';
            
            setTimeout(() => {
                poster.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
                poster.style.opacity = '1';
                poster.style.transform = 'scale(1) translateY(0)';
            }, 50);
        }
    }

    showLoading() {
        this.generateBtn.disabled = true;
        this.btnText.style.display = 'none';
        this.loadingText.style.display = 'inline';
        this.generateBtn.classList.add('loading');
    }

    hideLoading() {
        this.generateBtn.disabled = false;
        this.btnText.style.display = 'inline';
        this.loadingText.style.display = 'none';
        this.generateBtn.classList.remove('loading');
    }

    showSuccessMessage(message) {
        this.showMessage(message, 'success');
    }

    showErrorMessage(message) {
        this.showMessage(message, 'error');
    }

    showMessage(message, type) {
        // 移除现有的消息
        const existingMessage = document.querySelector('.message-toast');
        if (existingMessage) {
            existingMessage.remove();
        }

        // 创建消息元素
        const messageElement = document.createElement('div');
        messageElement.className = `message-toast ${type}`;
        messageElement.textContent = message;
        
        // 样式设置
        messageElement.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transform: translateX(100%);
            opacity: 0;
            transition: all 0.3s ease;
            max-width: 300px;
            word-wrap: break-word;
        `;

        // 根据类型设置背景色
        if (type === 'success') {
            messageElement.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        } else {
            messageElement.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
        }

        document.body.appendChild(messageElement);

        // 显示动画
        setTimeout(() => {
            messageElement.style.transform = 'translateX(0)';
            messageElement.style.opacity = '1';
        }, 100);

        // 3秒后自动消失
        setTimeout(() => {
            messageElement.style.transform = 'translateX(100%)';
            messageElement.style.opacity = '0';
            
            setTimeout(() => {
                if (messageElement.parentNode) {
                    messageElement.remove();
                }
            }, 300);
        }, 3000);
    }
}

// 高级动画效果类
class AnimationEffects {
    static createParticleEffect(container) {
        const particles = [];
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'];
        
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                border-radius: 50%;
                pointer-events: none;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: particleFloat ${2 + Math.random() * 3}s infinite;
            `;
            container.appendChild(particle);
            particles.push(particle);
        }
        
        return particles;
    }

    static createRippleEffect(element, x, y) {
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: translate(-50%, -50%);
            pointer-events: none;
            left: ${x}px;
            top: ${y}px;
            animation: rippleEffect 0.6s ease-out;
        `;
        
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
}

// 添加粒子动画CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes particleFloat {
        0% { transform: translateY(0px) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
    }
    
    @keyframes rippleEffect {
        0% { width: 0; height: 0; opacity: 1; }
        100% { width: 100px; height: 100px; opacity: 0; }
    }
`;
document.head.appendChild(style);

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new PosterGenerator();
    
    // 添加一些交互增强
    const posterContainer = document.getElementById('poster-container');
    posterContainer.addEventListener('click', (e) => {
        if (e.target.closest('.generated-poster')) {
            const rect = e.target.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            AnimationEffects.createRippleEffect(e.target.closest('.generated-poster'), x, y);
        }
    });
});

// 导出功能（可选）
function exportPoster() {
    const poster = document.querySelector('.generated-poster');
    if (!poster) {
        alert('请先生成海报！');
        return;
    }
    
    // 这里可以添加导出为图片的功能
    alert('导出功能开发中...');
}

// 保存模板功能（可选）
function saveTemplate() {
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const animation = document.getElementById('animation').value;
    const color = document.getElementById('color').value;
    
    const template = { title, content, animation, color };
    localStorage.setItem('posterTemplate', JSON.stringify(template));
    alert('模板已保存！');
}

// 加载模板功能（可选）
function loadTemplate() {
    const saved = localStorage.getItem('posterTemplate');
    if (saved) {
        const template = JSON.parse(saved);
        document.getElementById('title').value = template.title;
        document.getElementById('content').value = template.content;
        document.getElementById('animation').value = template.animation;
        document.getElementById('color').value = template.color;
        alert('模板已加载！');
    } else {
        alert('没有找到保存的模板！');
    }
}