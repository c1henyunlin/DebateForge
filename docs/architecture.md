# 架构说明

## 技术栈
- 前端：Vue.js 3 + Element Plus + Vite
- 后端：Python FastAPI
- AI：阿里云通义千问 (qwen-plus)
- 数据库：SQLite (开发) / PostgreSQL (生产)

## 项目结构
debateforge/
├── src/
│   ├── frontend/    # Vue前端
│   └── backend/     # FastAPI后端
├── prompts/         # Prompt模板
└── docs/            # 文档
