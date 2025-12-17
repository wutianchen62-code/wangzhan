# AI海报生成器 - Vercel部署指南

## 📋 项目概述

这是一个基于Flask的AI海报生成器，支持多种OpenAI兼容的API服务，可以生成美观的HTML海报代码。

## 🚀 部署到Vercel

### 方法一：通过GitHub部署（推荐）

1. **创建GitHub仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI Poster Generator"
   git branch -M main
   git remote add origin https://github.com/yourusername/ai-poster-generator.git
   git push -u origin main
   ```

2. **连接Vercel**
   - 访问 [Vercel官网](https://vercel.com)
   - 使用GitHub账号登录
   - 点击"New Project"
   - 选择你的GitHub仓库
   - 保持默认配置，点击"Deploy"

### 方法二：通过Vercel CLI部署

1. **安装Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **部署项目**
   ```bash
   vercel
   ```
   - 按照提示完成配置
   - 选择默认选项即可

## ⚙️ 环境配置

### 必需文件
- `vercel.json` - Vercel配置文件
- `api/index.py` - 无服务器函数入口
- `requirements.txt` - Python依赖
- `templates/index.html` - 前端界面

### 项目结构
```
├── api/
│   └── index.py          # Vercel函数入口
├── templates/
│   └── index.html       # 前端界面
├── coding_agent.py      # 主应用逻辑
├── requirements.txt     # Python依赖
├── vercel.json         # Vercel配置
└── DEPLOYMENT.md       # 部署说明
```

## 🔧 自定义配置

### 修改默认API设置
在 `coding_agent.py` 中修改：
```python
DEFAULT_API_URL = "https://api.deepseek.com/v1/chat/completions"
```

### 添加环境变量（可选）
在Vercel项目设置中添加：
- `DEFAULT_API_URL` - 默认API地址
- `DEFAULT_MODEL` - 默认模型名称

## 🌐 访问应用

部署成功后，Vercel会提供一个类似以下的URL：
```
https://your-project-name.vercel.app
```

## 🛠️ 本地开发

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python coding_agent.py
```

### 访问地址
```
http://localhost:5001
```

## 📱 功能特性

- ✅ 支持多种OpenAI兼容API
- ✅ 模型名称自定义输入
- ✅ 实时预览生成的海报
- ✅ 源代码查看和复制功能
- ✅ 响应式设计，支持移动端
- ✅ 错误处理和重试机制

## 🔒 安全注意事项

1. **API密钥安全**
   - 不要在代码中硬编码API密钥
   - 使用环境变量或Vercel的环境配置
   - 前端输入的API密钥不会存储在服务器

2. **CORS配置**
   - 已配置允许所有来源访问
   - 生产环境可限制为特定域名

## 🐛 故障排除

### 常见问题

1. **部署失败**
   - 检查 `requirements.txt` 依赖是否正确
   - 确认 `vercel.json` 配置无误

2. **API调用失败**
   - 验证API密钥是否正确
   - 检查API服务是否可用
   - 确认模型名称输入正确

3. **静态文件无法加载**
   - 确认 `templates` 目录存在
   - 检查Vercel的路由配置

### 日志查看
在Vercel控制台的"Functions"标签中查看部署日志。

## 📞 技术支持

如有问题，请检查：
1. Vercel部署日志
2. 浏览器开发者工具控制台
3. 网络请求状态

---

**部署愉快！** 🎉