# AI海报生成器 - 支持多种OpenAI兼容API

🎨 一个基于AI的智能海报代码生成器，支持多种OpenAI兼容的API服务，用户可以输入描述生成美观的HTML海报代码。

## ✨ 功能特点

### 核心功能
- **智能海报生成**：输入描述内容，AI自动生成完整的HTML海报代码
- **多模型支持**：支持DeepSeek、GPT、Claude等OpenAI兼容API
- **实时预览**：生成后立即预览海报效果
- **源代码查看**：查看和复制生成的HTML/CSS/JavaScript代码
- **响应式设计**：适配桌面和移动设备

### 技术特色
- **通用API兼容**：支持所有OpenAI兼容的API服务
- **模型自定义**：可自由输入任意模型名称
- **Web界面**：现代化美观的用户界面
- **一键部署**：支持Vercel无服务器部署
- **错误处理**：完善的错误提示和重试机制

## 📁 项目结构

```
AI海报生成器/
├── api/
│   └── index.py              # Vercel无服务器函数入口
├── templates/
│   └── index.html            # 前端界面（HTML/CSS/JS）
├── coding_agent.py           # 主应用逻辑（Flask后端）
├── requirements.txt          # Python依赖列表
├── vercel.json              # Vercel部署配置
├── DEPLOYMENT.md            # 详细部署指南
└── README.md                # 项目说明文档
```

## 🚀 快速开始

### 本地开发

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **启动服务**：
   ```bash
   python coding_agent.py
   ```

3. **访问应用**：
   ```
   http://localhost:5001
   ```

### Vercel部署

1. **查看部署指南**：
   - 详细步骤请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

2. **一键部署**：
   - 支持GitHub集成部署
   - 或使用Vercel CLI部署

3. **访问地址**：
   ```
   https://your-project.vercel.app
   ```

## 📝 使用说明

### 1. 配置API设置
- **API密钥**：输入您的OpenAI兼容API密钥
- **模型名称**：输入要使用的AI模型名称（如：deepseek-v3_2、gpt-4等）
- **API地址**：可选，默认使用DeepSeek API

### 2. 描述海报需求
- **详细描述**：用中文或英文描述您想要的海报效果
- **风格要求**：可以指定颜色、布局、动画效果等
- **内容要素**：包含标题、正文、图片等需求

### 3. 生成海报
- 点击"� 生成海报"按钮
- AI将根据描述生成完整的HTML海报代码
- 生成结果包含预览和源代码两个标签页

### 4. 查看结果
- **预览标签页**：实时查看生成的海报效果
- **源代码标签页**：查看和复制HTML/CSS/JavaScript代码
- **复制功能**：一键复制代码到剪贴板

## 🛠️ 技术架构

### 前端技术栈
- **HTML5/CSS3/JavaScript**：现代化Web技术
- **响应式设计**：适配各种屏幕尺寸
- **异步通信**：Fetch API与后端交互
- **实时预览**：动态iframe内容加载

### 后端技术栈
- **Flask**：轻量级Python Web框架
- **Flask-CORS**：跨域请求支持
- **Requests**：HTTP客户端库
- **JSON API**：RESTful接口设计

### AI集成
- **OpenAI兼容API**：支持多种AI服务提供商
- **模型自定义**：可配置任意模型名称
- **智能提示工程**：优化的AI生成提示词
- **错误重试机制**：网络异常自动重试

## 🔧 自定义开发

### 添加新的AI模型支持
1. 在 `templates/index.html` 中更新模型名称提示
2. 确保模型支持OpenAI兼容的API格式
3. 测试模型响应格式是否兼容

### 修改默认配置
1. **默认API地址**：修改 `coding_agent.py` 中的 `DEFAULT_API_URL`
2. **默认模型**：修改 `coding_agent.py` 中的默认模型名称
3. **界面样式**：修改 `templates/index.html` 中的CSS样式

### 扩展功能
1. **添加新的生成类型**：在 `PosterCodingAgent` 类中添加新方法
2. **自定义提示词**：修改AI生成提示词模板
3. **添加导出功能**：实现海报代码下载功能

## 🌐 浏览器兼容性

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 🐛 故障排除

### 常见问题

**Q: 海报生成失败怎么办？**
A: 检查API密钥是否正确，模型名称是否有效，网络连接是否正常。

**Q: 预览无法显示？**
A: 检查浏览器是否支持iframe，尝试刷新页面或清除缓存。

**Q: 如何获取API密钥？**
A: 需要注册DeepSeek、OpenAI或其他兼容的AI服务提供商账户。

**Q: Vercel部署失败？**
A: 检查 `requirements.txt` 依赖是否正确，查看Vercel部署日志。

### 开发调试
- 打开浏览器开发者工具查看控制台输出
- 检查网络请求状态和响应内容
- 验证API端点是否正确响应
- 查看Vercel函数日志

## 📈 版本历史

### v2.0.0 (当前版本)
- ✅ 支持多种OpenAI兼容API
- ✅ 模型名称自定义输入
- ✅ Vercel无服务器部署支持
- ✅ 现代化Web界面设计
- ✅ 实时预览和源代码查看
- ✅ 错误处理和重试机制

### v1.0.0 (初始版本)
- ✅ 基础海报生成功能
- ✅ DeepSeek API集成
- ✅ Flask本地开发环境

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License

---

**项目维护**：AI助手  
**技术支持**：通过GitHub Issues  
**最后更新**：2025年12月  
**部署状态**：✅ Vercel就绪