import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from coding_agent import app

# Vercel需要这个handler来处理请求
if __name__ == "__main__":
    # 本地开发环境
    app.run(host='0.0.0.0', port=5001, debug=True)
else:
    # Vercel生产环境
    handler = app